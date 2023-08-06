"""
Type this in terminal to upgrade the package. (Write here for remember)
>> python setup.py sdist bdist_wheel
>> twine upload dist/*
"""
from setuptools import find_packages, setup

setup(name="handyscikit",
      version="0.0.8.5",
      description="Add set_point_source_by_coordinate interface.",
      author="Hong Peng",
      python_requires=">=3.7.0",
      url="https://github.com/minho-hong/handyscikit.git",
      package_data={},
      packages=find_packages(),
      install_requires=["cython", "gmsh", "numpy", "vtk"],
      license="GPL")

