import setuptools

with open("./README.md", "r") as readme:
    describe_package = readme.read()

setuptools.setup(
    name = "tektology",
    version = "0",
    author = "",
    author_email = "",
    description = "create tektology communication system",
    long_description = describe_package,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3",
    install_requires = ["gitpython"],
    keywords = "tektology communication system",
    entry_points = {
    "console_scripts": [
        'tektology=tektology.__main__:main',
        'tek=tek.__main__:main',
    ]
    }
)
