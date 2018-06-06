from setuptools import setup

setup(name="seoulai-gym",
      version="0.1",
      description="The Seoul AI Gym: Seoul AI Gym is a toolkit for developing AI algorithms.",
      url="https://github.com/seoulai/gym",
      author="Seoul AI",
      author_email="martin@seoulai.com",
      license="The MIT License",
      packages=["seoulai_gym"],
      zip_safe=False,
      install_requires=[
          "pygame>=1.9.3",
          "numpy>=1.14.2",
          "pytest>=3.6.0",
      ],
      tests_require=["pytest"],
      include_package_data=True,
      keywords = ["gym", "ai", "machine-learning", "artificial-intelligence"],
      )
