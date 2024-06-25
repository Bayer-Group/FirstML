import os
import sys

from setuptools import find_packages, setup


REQUIRED_MAJOR = 3
REQUIRED_MINOR = 8

if sys.version_info < (REQUIRED_MAJOR, REQUIRED_MINOR):
    error = (
        "Your version of python ({major}.{minor}) is too old. You need python >= {required_major}.{required_minor}."
    ).format(
        major=sys.version_info.major,
        minor=sys.version_info.minor,
        required_minor=REQUIRED_MINOR,
        required_major=REQUIRED_MAJOR,
    )
    sys.exit(error)


DESCRIPTION = "Transform your Jupyter notebooks into a pipeline of nodebooks."

# use conda or provide c++ compiler for pygraphviz
INSTALL_REQUIRES = [
    "pandas",
    "numpy",
    "papermill~=2.4.0",
    "black",
    "ipython",
    "ipykernel",
    "PyYAML~=6.0",
    # for graph processing
    "networkx~=2.8.6",
    # for graph visualization
    "matplotlib~=3.6.0",
    "pydot",
    #"pygraphviz",
    # for mlflow experiment tracking
    "mlflow",
    "s3fs",
    "fsspec",
    "python-dotenv",
    "openpyxl",
    "ipywidgets",
    "widgetsnbextension"
]

IO_PREREQUIRES=[
    "cmake",
    "pyarrow~=3.0.0",
]

IO_REQUIRES = [
    # for presto
    "presto-python-client",
    "oauth_keys2",
    # for snowflake
    "snowflake-connector-python[pandas]~=2.9.0",
    "pyopenssl~=22.1.0",
    "cryptography~=38.0.4", 
    "urllib3~=1.24.3",
    "botocore~=1.13.50",
    "s3fs~=0.4.2"
]

DEV_REQUIRES = [
    # for test nodebook
    "scikit-learn",
]

root_dir = os.path.dirname(__file__)

# Use README.md as the long description
with open(os.path.join(root_dir, "README.md"), "r", encoding="utf8") as file:
    long_description = file.read()

setup(
    name="firstml",
    description=DESCRIPTION,
    author="Digital Health Data Science",
    author_email="daniele.sacco@bayer.com",
    url="https://github.com/bayer-int/firstml-example",
    version="0.1.0",
    python_requires=">=3.8",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "io": IO_REQUIRES,
        "dev": DEV_REQUIRES,
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # https://pypi.org/classifiers/
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    entry_points={
        "console_scripts": ["firstml=firstml.cli:cmd_router"],
    },
)
