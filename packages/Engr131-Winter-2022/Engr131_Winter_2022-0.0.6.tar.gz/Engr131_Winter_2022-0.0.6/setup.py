import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Engr131_Winter_2022", # Replace with your own username
    version="0.0.6",
    author="Shannon Capps and Joshua Agar",
    author_email="jca92@drexel.edu",
    description="Utilities for ENGR131",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/driscollis/arithmetic",
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    python_requires='>=3.6',
)