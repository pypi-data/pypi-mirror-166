from setuptools import setup, find_packages
from Cython.Build import cythonize




with open('README.md', 'r') as fl:
    long_des = fl.read()

with open('LICENSE-2.0.txt', 'r') as fil:
    lisen = fil.read()

setup(
    name='SR29',
    version='1.0.2',
    author='Mame29',
    description='The SR29 encode and decode',
    long_description=long_des,
    long_description_content_type="text/markdown",
    ext_modules=cythonize(["sr29/*.c"]),
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'SR29 = sr29.SR29:main'
            ]
        },
    license=lisen,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        ]
)
