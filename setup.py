from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = ''
readme_path = this_directory / 'README.md'
if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')

setup(
    name='finverse-python-sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.20.0',
    ],
    author='Kevin Go',
    author_email='gojohnkevin@gmail.com',
    description='A community-driven Python SDK for the Finverse API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/es-kevingo/finverse-python-sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.7',
)