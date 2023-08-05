import os

import setuptools  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="unittest-autocomp",
    version='0.0.1',
    author="Leon Morten Richter",
    author_email="misc@leonmortenrichter.de",
    description="Autocompletion for unittest in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/M0r13n/unittest-autocomp",
    license="MIT",
    packages=setuptools.find_packages(exclude=['test*', ]),
    package_data={
        "pyais": ["py.typed"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Typing :: Typed",
    ],
    keywords=["test", "unittest", "autocompletion", ],
    python_requires='>=3.7',
    install_requires=[],
    extras_require={
        'dev': ['mypy', 'flake8', 'coverage', 'twine', ]
    },
    entry_points={
        "console_scripts": [
            'unittest-autocomp=autocomp:run'
        ]
    }
)
