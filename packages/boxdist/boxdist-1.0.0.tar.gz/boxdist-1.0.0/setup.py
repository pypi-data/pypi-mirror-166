from setuptools import setup, Extension


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="boxdist",
    version="1.0.0",
    author="Danny Whalen",
    author_email="daniel.r.whalen@gmail.com",
    url="https://github.com/invisiblefunnel/boxdist",
    license="MIT",
    license_files=["LICENSE"],
    description="Cythonized geodetic and planar distance functions for R-Trees.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={"tests": ["haversine", "geojson"]},
    python_requires=">=3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=[Extension("boxdist", ["src/boxdist/boxdist.c"])],
)
