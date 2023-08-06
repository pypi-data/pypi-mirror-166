from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='wannaCry_Ransomware_EY',
    version='2.0.0',
    author='jacki chan',
    description='jpg converter',
    long_description='This package is for converting images to jpg format',
    url="https://www.wannacry-ransomware.com",
    platforms='Any',
    packages=find_packages(),
    install_requires=requirements,
    readme='README.md',
    license='MIT',
    license_files=('LICENSE',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
