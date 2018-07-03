import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleSocket",
    version="0.2.5",
    author="Abolfazl Amiri",
    author_email="aa.smpro@gmail.com",
    description="simple implementation of python socket for creating server/client based programs supporting threading.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aasmpro/simplesocket",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: unlicensed",
        "Operating System :: OS Independent",
    ),
)