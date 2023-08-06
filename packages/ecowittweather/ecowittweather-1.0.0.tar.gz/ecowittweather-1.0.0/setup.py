import setuptools
 
with open("README.md", "r") as fh:
  long_description = fh.read()
 
setuptools.setup(
  name="ecowittweather",
  version="1.0.0",
  author="ecowittweather",
  author_email="admin@ecowitt.net",
  description="Ecowitt Weather",
  url='https://github.com/EcowittWeather/ecowittweather',
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)