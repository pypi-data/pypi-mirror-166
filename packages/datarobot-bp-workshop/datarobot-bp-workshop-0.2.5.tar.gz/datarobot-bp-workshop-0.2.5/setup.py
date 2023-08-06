"""DataRobot Blueprint Workshop
================================

The Blueprint Workshop is built to ensure that constructing and modifying DataRobot blueprints
through a programmatic interface is idiomatic, convenient, and powerful.

This library requires a `DataRobot`_ account.

The easiest way to get started is by reading the
`Documentation`_.

This package is covered under the DataRobot Tool and Utility Agreement, which can be
read on our `Legal`_ page, along with our privacy policy and more.

Prerequisites
-----------------
Python >= 3.7

Ensure your DataRobot account has enabled:

- Show Uncensored Blueprints
- Enable Customizable Blueprints

Installation
-----------------
Optionally, create a virtual environment

::

    $ mkvirtualenv -p python3.7 blueprint-workshop


Install Graphviz on Linux (to render blueprints):

::

    $ sudo apt-get install graphviz


Install Graphviz on Mac (to render blueprints):

::

    $ brew install graphviz


Install the library!

::

    $ pip install datarobot-bp-workshop


Recommended:

::

    $ pip install jupyterlab


From a folder where you'd like to save your scripts:

::

    $ jupyter-lab .

.. _datarobot: https://datarobot.com
.. _documentation: https://blueprint-workshop.datarobot.com
.. _legal: https://www.datarobot.com/legal/
"""

import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


with open("datarobot_bp_workshop/_version.py") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

# Should match lint-requirements.txt
lint_require = [
    "black==22.6.0",
    "isort==5.10.1",
    "flake8==4.0.1",
]

tests_require = [
    "pytest-mock==3.5.1",
    "pytest==6.1.2",
    "pytest-check==1.0.1",
    "pytest-cov==2.12.1",
]

# Should match docs-requirements.txt
docs_require = [
    "Jinja2<3.1",
    "markupsafe==2.0.1",
    "Sphinx==3.5.4",
    "sphinx_rtd_theme==0.5.2",
    "numpydoc>=0.6.0",
    "nbsphinx>=0.8.5,<1",
    "sphinx-tabs==3.1.0",
    "sphinx-rtd-dark-mode==1.2.2",
    "ipython==7.25.0",
]

dev_require = tests_require + lint_require + docs_require + ["twine==1.6.5"]

release_require = ["zest.releaser[recommended]==6.22.0"]

setup(
    name="datarobot-bp-workshop",
    version=version,
    description="This client library is designed to support building DataRobot blueprints.",
    author="datarobot",
    author_email="support@datarobot.com",
    maintainer="datarobot",
    maintainer_email="info@datarobot.com",
    url="https://blueprint-workshop.datarobot.com",
    license="DataRobot Tool and Utility Agreement",
    packages=find_packages("."),
    long_description=__doc__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=["datarobot>=2.27.0,<3", "networkx>=2.2", "graphviz>=0.16,<1"],
    tests_require=tests_require,
    extras_require={
        "dev": dev_require,
        "docs": docs_require,
        "release": release_require,
        "lint": lint_require,
    },
    cmdclass={"test": PyTest},
)
