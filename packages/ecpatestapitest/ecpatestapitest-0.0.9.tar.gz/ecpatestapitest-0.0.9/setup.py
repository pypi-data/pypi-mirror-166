import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name="ecpatestapitest",
  version="0.0.9",
  author="Ecowitt_1",
  author_email="369532361@qq.com",
  description="Ecowitt get data",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)