from setuptools import setup,find_packages

def load_requirements(path="requirements.txt"):
    """Load requirements but ignore editable/local entries and comments.

    Editable installs like '-e .' or local paths are valid in requirements.txt
    for pip, but are not valid values for setuptools' install_requires. Filter
    them out so setup() receives only proper package specifiers.
    """
    reqs = []
    with open(path) as f:
        for raw in f.read().splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            # skip pip options and local/editable entries
            if line.startswith("-e ") or line.startswith("-r ") or line.startswith("--") or line.startswith("git+"):
                continue
            if line.startswith("./") or line.startswith("../") or line.startswith("file:"):
                continue
            reqs.append(line)
    return reqs


requirements = load_requirements()

setup(
    name="Ryte-Robo",
    version="0.1",
    author="Kabya",
    packages=find_packages(),
    install_requires=requirements,
)