import pathlib
import glob
from setuptools import setup, find_packages
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
  name="fugen",
  version="0.0.1",
  description="Financial University package for synthetic data generation",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Vildanov Timur, Duc Truong",
  license="MIT",
  packages=find_packages(),
  data_files=glob.glob('fugen/data/*.json'),
  include_package_data=True,
  zip_safe=True
)