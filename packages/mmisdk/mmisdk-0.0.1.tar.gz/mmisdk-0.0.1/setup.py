"""The setup.py file for MMI SDK Python."""

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mmisdk',  # Name in pypi, to use when a developer runs "pip install"
    version='0.0.1',
    author='Xavier Brochard',
    author_email='xavier.brochard@consensys.net',
    description="A Python library to create and submit EVM transactions to custodians connected with MetaMask Institutional.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://consensys.gitlab.io/codefi/products/mmi/mmi-sdk-py/sdk-python/',
    py_modules=["mmisdk"],
    package_dir={'': 'src'},
    # packages=find_packages(exclude=('tests')),
    # license='', # TODO
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    keywords='python sdk custodian interact get create transaction',
    # packages=['fire', 'fire.console'],
    install_requires=[
        'pydantic>=1.10.1',
        'requests>=2.28.1',
    ],
    extras_require={
        "dev": [
            "arrow==1.2.2",
            "attrs==22.1.0",
            "autopep8==1.7.0",
            "binaryornot==0.4.4",
            "certifi==2022.6.15",
            "chardet==5.0.0",
            "charset-normalizer==2.1.1",
            "click==8.1.3",
            "cookiecutter==2.1.1",
            "idna==3.3",
            "iniconfig==1.1.1",
            "Jinja2==3.1.2",
            "jinja2-time==0.2.0",
            "MarkupSafe==2.1.1",
            "packaging==21.3",
            "pluggy==1.0.0",
            "py==1.11.0",
            "pycodestyle==2.9.1",
            "pyparsing==3.0.9",
            "pytest==7.1.3",
            "python-dateutil==2.8.2",
            "python-slugify==6.1.2",
            "PyYAML==6.0",
            "six==1.16.0",
            "text-unidecode==1.3",
            "toml==0.10.2",
            "tomli==2.0.1",
            "typing_extensions==4.3.0",
            "urllib3==1.26.12",
        ]
    }
)
