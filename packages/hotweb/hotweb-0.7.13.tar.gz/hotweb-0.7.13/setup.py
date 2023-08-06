from setuptools import setup, find_packages

def readme():
    with open("readme.md","r") as f:
        info = f.read()
        return info
setup(
    name="hotweb",
    version="0.7.13",
    license="MIT",
    author = "Real Manlow,aka ManlowCharumbira",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author_email="realmanlow20@gmail.com",
    packages=find_packages("hotweb"),
    package_dir = {'':'hotweb'},
    include_package_data = True,
    keywords = "hotweb python-web-framework python web framework fast light secure",
    install_requires = [
        "parse","waitress","webob","requests",
    ]
)