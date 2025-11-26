import os
# Avoid huggingface/tokenizers parallelism warning when the process is
# forked (e.g. development server reloader or other forks). Set this
# before importing any component that may load tokenizers or use
# parallelism.
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
from app.components.retriever import create_qa_chain
from app.common.logger import get_logger


load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom(24)
load_dotenv()

from markupsafe import Markup
def nl2br(value):
    return Markup(value.replace("\n" , "<br>\n"))

app.jinja_env.filters['nl2br'] = nl2br

# module logger
logger = get_logger(__name__)

@app.route("/" , methods=["GET","POST"])
def index():
    if "messages" not in session:
        session["messages"]=[]

    if request.method=="POST":
        user_input = request.form.get("prompt")

        if user_input:
            messages = session["messages"]
            messages.append({"role" : "user" , "content":user_input})
            session["messages"] = messages

            try:
                qa_chain = create_qa_chain()
                if qa_chain is None:
                    raise Exception("QA chain could not be created (LLM or VectorStore issue)")
                # The QA chain's PromptTemplate expects variables named
                # 'context' and 'question'. Pass the user's text under
                # the 'question' key so the PromptTemplate receives it.
                # Provide both keys: 'input' for retrieval steps that
                # expect it, and 'question' for the PromptTemplate.
                response = qa_chain.invoke({"input": user_input, "question": user_input})

                # Debug/log the raw chain response to understand its shape.
                try:
                    logger.debug("Raw chain response: %s", repr(response))
                except Exception:
                    pass

                # Robust extraction: chains may return a plain string, a dict
                # with various keys, or an object. Check common keys and fall
                # back to str(response) so the UI won't show "No response".
                result = None
                if isinstance(response, str):
                    result = response
                elif isinstance(response, dict):
                    for key in ("result", "output", "answer", "text", "response", "output_text", "final_answer"):
                        if key in response and response[key]:
                            result = response[key]
                            break
                else:
                    # try attribute access
                    try:
                        result = getattr(response, "result", None) or getattr(response, "output", None)
                    except Exception:
                        result = None

                if result is None:
                    # last resort: stringify whatever was returned
                    try:
                        result = str(response)
                    except Exception:
                        result = "No response"

                messages.append({"role" : "assistant" , "content" : result})
                session["messages"] = messages

            except Exception as e:
                error_msg = f"Error : {str(e)}"
                return render_template("index.html" , messages = session["messages"] , error = error_msg)
            
        return redirect(url_for("index"))
    return render_template("index.html" , messages=session.get("messages" , []))

@app.route("/clear")
def clear():
    session.pop("messages" , None)
    return redirect(url_for("index"))

if __name__=="__main__":
    app.run(host="0.0.0.0" , port=5000 , debug=False , use_reloader = False)



