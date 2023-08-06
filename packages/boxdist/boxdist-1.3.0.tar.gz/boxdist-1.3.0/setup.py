from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="boxdist",
    version="1.3.0",
    author="Danny Whalen",
    author_email="daniel.r.whalen@gmail.com",
    url="https://github.com/invisiblefunnel/boxdist",
    packages=find_packages(),
    license="MIT",
    license_files=["LICENSE"],
    description="Cythonized geodetic and planar distance functions for R-Trees.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={"tests": ["haversine", "geojson", "mypy"]},
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=cythonize(
        [
            Extension("geodetic", ["boxdist/geodetic.pyx"]),
            Extension("planar", ["boxdist/planar.pyx"]),
        ],
        compiler_directives={
            "language_level": 3,
            "embedsignature": True,
        },
    ),
)
