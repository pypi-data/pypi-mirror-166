from setuptools import setup, find_packages


setup(
    name="hotweb",
    version="0.6",
    license="MIT",
    author = "Real Manlow,aka ManlowCharumbira",
    author_email="realmanlow20@gmail.com",
    packages=["src"],
    #package_dir = {'':''},
    keywords = "hotweb python-web-framework python web framework fast light secure",
    install_requires = [
        "parse","waitress","webob","requests",
    ]
)