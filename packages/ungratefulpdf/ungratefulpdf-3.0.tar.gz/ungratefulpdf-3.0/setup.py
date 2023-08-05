from pathlib import Path
import setuptools


setuptools.setup(
    name="ungratefulpdf",
    version=3.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
