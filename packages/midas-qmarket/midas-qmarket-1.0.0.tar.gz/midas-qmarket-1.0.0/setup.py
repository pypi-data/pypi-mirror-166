import setuptools

with open("VERSION") as freader:
    VERSION = freader.readline().strip()

with open("README.md") as freader:
    README = freader.read()

install_requirements = [
    "midas-util",
    "mosaik_api",
    "pandapower",
    "natsort",
    "numpy",
    "scipy",
]

development_requirements = [
    "flake8",
    "pytest",
    "coverage",
    "black==22.3.0",
    "setuptools",
    "twine",
    "wheel",
]

extras = {"dev": development_requirements}

setuptools.setup(
    name="midas-qmarket",
    version=VERSION,
    description="A simulator for a reactive power market.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Thomas Wolgast",
    author_email="thomas.wolgast@offis.de",
    url="https://gitlab.com/midas-mosaik/midas-qmarket",
    packages=[
        "midas.modules.qmarket",
    ],
    # include_package_data=True,
    install_requires=install_requirements,
    extras_require=extras,
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)
