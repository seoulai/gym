from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="seoulai-gym",
      version="0.1.2",
      description="The Seoul AI Gym: Seoul AI Gym is a toolkit for developing AI algorithms.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/seoulai/gym",
      author="Seoul AI",
      author_email="m.kersner@gmail.com",
      license="The MIT License",
      packages=["seoulai_gym"],
      zip_safe=False,
      install_requires=[
          "pygame>=1.9.3",
          "numpy>=1.14.2",
          "pytest>=3.6.0",
          "flake8>=3.5.0",
          "PyQt5>=5",
          "pandas>=0.23.4",
          "matplotlib>=2.2.3",
          "flake8-quotes>=1.0.0"
      ],
      tests_require=["pytest"],
      include_package_data=True,
      keywords=["gym", "ai", "machine-learning", "artificial-intelligence"],
      )
