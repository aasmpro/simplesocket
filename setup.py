import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleSocket",
    version="0.2.5.1",
    author="Abolfazl Amiri",
    author_email="aa.smpro@gmail.com",
    description="simple implementation of python socket for creating server/client based programs supporting threading.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aasmpro/simplesocket",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP"
    ],
)
