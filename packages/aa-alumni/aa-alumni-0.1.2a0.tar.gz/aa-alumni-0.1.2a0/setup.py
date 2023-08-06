import os

from setuptools import find_packages, setup

from alumni import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='aa-alumni',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description='Alliance Auth Plugin',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/tactical-supremacy/aa-alumni',
    author='Joel Falknau',
    author_email='joel.falknau@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='~=3.7',
    install_requires=[
        "allianceauth>=2.9.0",
    ],

)
