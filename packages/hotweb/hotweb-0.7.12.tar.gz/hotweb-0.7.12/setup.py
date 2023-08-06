from setuptools import setup, find_packages


setup(
    name="hotweb",
    version="0.7.12",
    license="MIT",
    author = "Real Manlow,aka ManlowCharumbira",
    author_email="realmanlow20@gmail.com",
    packages=["hotweb"],
    #package_dir = {'':'hotweb'},
    keywords = "hotweb python-web-framework python web framework fast light secure",
    install_requires = [
        "parse","waitress","webob","requests",
    ]
)