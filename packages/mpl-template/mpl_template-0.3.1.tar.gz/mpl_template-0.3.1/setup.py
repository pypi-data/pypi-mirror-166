import os
from pathlib import Path
from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open(os.path.join("mpl_template", "__init__.py")) as info_file:
    version = author = email = ""
    for line in info_file:
        if line.startswith("__version__"):
            version = line.split("=")[1].replace('"', "").strip()
        elif line.startswith("__author__"):
            author = line.strip().split("=")[1].replace('"', "").strip()
        elif line.startswith("__email__"):
            email = line.strip().split("=")[1].replace('"', "").strip()


DESCRIPTION = "mpl-template: matplotlib report template constructor"
LONG_DESCRIPTION = DESCRIPTION
NAME = "mpl_template"
VERSION = version
AUTHOR = author
AUTHOR_EMAIL = email
URL = "https://austinorr.github.io/mpl-template"
DOWNLOAD_URL = "https://github.com/austinorr/mpl-template.git"
LICENSE = "BSD 3-clause"
PACKAGES = find_packages()
PLATFORMS = "Python 3.8+."
CLASSIFIERS = [
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Intended Audience :: Science/Research",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3.8",
]
INSTALL_REQUIRES = ["matplotlib"]
PACKAGE_DATA = {
    "mpl_template.tests.baseline_images": ["*png"],
    "mpl_template.tests.img": ["*png"],
}

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
)
