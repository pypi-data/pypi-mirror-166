import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jutool",
    version="0.1.8",
    author="Ke",
    author_email="jiangke1207@icloud.com",
    description="Some base methods for developing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.example.com/~cschultz/bvote/",
    packages=setuptools.find_packages(),
    install_requires=['progressbar2==4.0.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
