import pathlib
from setuptools import setup, find_namespace_packages

# The text of the README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

# Setup configuration
setup(
    name='genepy3d',
    version='0.2.2',
    description=(
      "Python Library for 3D Quantitative Geometry in Computation Microscopy"
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    author='genepy3d-team',
    url='https://gitlab.com/genepy3d/genepy3d',
    license="BSD-3-Clause",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    package_dir={'':'src'},
    packages=find_namespace_packages(where="src"),
    include_package_data=False,
    python_requires=">=3.6",
    install_requires=[
        "scikit-learn>=0.24.2",
		"scikit-image>=0.17.2",
        "pandas>=1.1.5",
        "seaborn>=0.11.2",
        "requests>=2.27.1",
        "tables>=3.7.0",
        "numpy-stl>=2.17.1",
        "vtk>=9.1.0",
        "pyevtk>=1.5.0",
        "pathos>=0.2.8",
        "pillow>=8.4.0",
        "pynrrd>=0.4.3",
        "anytree>=2.8.0",
        "trimesh>=3.14.1",
        "PyAstronomy>=0.18.0",
        "matplotlib>=3.3.4",
    ]
)

