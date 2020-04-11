# stdlib modules
import os
import sys
from setuptools import setup
from setuptools import find_packages

# tool modules
f = os.path.abspath(__file__)
package_dir = os.path.join(os.path.dirname(f), "python")
sys.path.insert(0, package_dir)
from workoutbuddy import __version__  # noqa

requirements_install = ["SQLAlchemy==1.3.*",
                        "matplotlib==3.2.*",
                        "pandas==1.0.*",
                        "PySide2==5.14.*"]
requirements_dev = ["flake8==3.7.*", "radon==4.1.*"]


setup(name="workoutbuddy",
      version=__version__,
      description="Workout database and plotting tool.",
      license="GPLv3",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/workoutbuddy",
      packages=find_packages(where="python"),
      package_dir={"": "python"},
      scripts=["bin/workoutbuddy-cli"],
      install_requires=requirements_install,
      extras_require={"dev": requirements_dev},
      data_files=[(os.path.expanduser("~/.workoutbuddy"), [])])
