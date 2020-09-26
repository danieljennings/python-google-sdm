import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("version", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="google-sdm",
    version=version,
    author="Jacob McSwain",
    author_email="pypi@mcswain.dev",
    description="Google's Smart Device Management (SDM) API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/USA-RedDragon/python-google-sdm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)
