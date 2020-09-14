import setuptools

requirements = None
with open("requirements") as stream:
    requirements = stream.readlines()


setuptools.setup(
    name = "persim",
    version = "2.0.0",
    author = "Zero <dakoolstwunn@gmail.com>",
    description = "A tool for generating API docs",
    licence = "AGPLv3",
    packages = setuptools.find_packages(),
    install_requires = requirements,
    zip_safe = False,
    entry_points = {
        "console_scripts": ["persim = persim.main:main"],
    },
)
