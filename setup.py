import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="itfproject-workshops-api",
    version="2019.01b0",
    author="Lander Visterin",
    author_email="landervisterin@outlook.com",
    description="API for workshops webapp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages()
)
