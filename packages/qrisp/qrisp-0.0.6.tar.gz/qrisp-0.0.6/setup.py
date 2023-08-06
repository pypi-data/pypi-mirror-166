import setuptools


try:
    with open("requirements.txt") as f:
        REQUIREMENTS = f.read().splitlines()
except FileNotFoundError:
    REQUIREMENTS = []



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qrisp",
    version="0.0.6",
    author="Raphael Seidel",
    author_email="raphael.seidel@fokus.fraunhofer.de",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)