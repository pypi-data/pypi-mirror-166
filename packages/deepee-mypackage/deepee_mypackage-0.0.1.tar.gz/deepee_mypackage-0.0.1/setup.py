import setuptools

with open(r"C:\Users\Admin\Documents\myApp\deepee_mypackage\readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepee_mypackage",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Mine",                     # Full name of the author
    description="Quicksample Test Package for Student and teacher details",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["deepee_mypackage"],             # Name of the python package
    package_dir={'':r'C:\Users\Admin\Documents\myApp\deepee_mypackage\src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)
