import setuptools

with open("README.md") as readme:
    description = readme.read()

setuptools.setup(
    name="superpy_rvb",
    version="0.0.9",
    description="testing cli tool",
    install_requires=["rich", "coloroma"],
    # py_modules=["main.py"],
    keywords="winc superpy",
    package_dir={"": "source"},
    packages=setuptools.find_packages(where="source"),
    python_requires=">=3.9",
    entry_points={"console_scripts": ["superpy = superpy_rvb.main:main"]},
    long_description=description,
    long_description_content_type="text/markdown",
)
