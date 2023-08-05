import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(

    name="BMKG-Latest",
    version="0.1",
    author="Firdaus W N",
    author_email="<firdauswnn@gmail.com>",
    description="This package will guide us to receive the latest Earthquake Information from BMKG Indonesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/futagoya/bmkg-latest",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
