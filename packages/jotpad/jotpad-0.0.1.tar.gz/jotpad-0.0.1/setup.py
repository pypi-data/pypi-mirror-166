import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jotpad",
    version="0.0.1",
    install_requires=[],
    author="Scott Russell",
    author_email="me@scottrussell.net",
    description="A cli tool for managing notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scrussell24/pad",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
