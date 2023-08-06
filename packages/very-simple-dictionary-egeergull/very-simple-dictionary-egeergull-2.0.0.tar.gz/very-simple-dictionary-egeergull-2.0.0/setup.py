from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    # TODO: Write a globally unique name which will be listed on PyPI
    name="very-simple-dictionary-egeergull",
    author="Ege Ergül",  # TODO: Write your name
    version="2.0.0",
    packages=["dictionary"],
    description = "short package description",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)

