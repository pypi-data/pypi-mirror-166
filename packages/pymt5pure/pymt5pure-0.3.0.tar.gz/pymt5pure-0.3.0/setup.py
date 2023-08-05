from setuptools import setup, find_packages


def read_version(module_name):
    from re import match, S
    from os.path import join, dirname

    with open(join(dirname(__file__), module_name, "__init__.py")) as f:
        return match(r".*__version__.*('|\")(.*?)('|\")", f.read(), S).group(2)


setup(
    name="pymt5pure",
    version=read_version("pymt5pure"),
    description="MetaTrader 5 WebAPI implementation in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/meyt/pymt5pure",
    author="Meyti",
    license="MIT",
    keywords="web tool-chain",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=["pycryptodome >= 3.15.0"],
)
