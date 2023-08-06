# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botdoc",
    version="100",
    url="https://github.com/bthate/botdoc",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="The Python3 bot Namespace",
    install_requires=["oplib", "runlib", "botlib", "botd"],
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["botdoc"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
