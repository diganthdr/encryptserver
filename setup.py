import setuptools
VERSION_FILE = ".version"

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(VERSION_FILE) as fd:
    version = fd.read().strip()

setuptools.setup(
    name="crypto-server",
    version=version,
    author="Diganth D R",
    author_email="diganth.d.r@woven-planet.com",
    description="Package to create crypto-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.9.4',
)
