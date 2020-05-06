from setuptools import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='MARCprototype',
    license='GPL',
    version='0.0.1',
    author_email="grokwithahul@gmail.com",
    description="NYAS COVID-19 Challenge",
    long_description=open("README.md").read(),
    packages=['tools', 'tools.package_tools'],
    project_urls={
        "Source": "https://github.com/Redstomite/MARC-prototype",
    },
    package_dir={'': 'MARC-prototype'},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    author='Rahul Prabhu',
)
