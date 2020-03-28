import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('log4py.py', 'rb') as f:
    rs = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(rs))

setup(
    name='log4py',
    py_modules=["log4py"],
    version=version,
    description='Log For Python',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
    ],
    author='liyatao',
    url='https://github.com/taogeYT/log4py',
    author_email='li_yatao@outlook.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=True,
)
