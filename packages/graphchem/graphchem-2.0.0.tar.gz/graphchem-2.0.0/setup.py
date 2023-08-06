from setuptools import find_packages, setup
import os


def get_version():

    fp = os.path.join('graphchem', '__init__.py')
    vars = {}
    with open(fp, 'r') as f:
        exec(f.read(), vars)
    return vars['__version__']


setup(
    name='graphchem',
    version=get_version(),
    description='Graph-based models for chemical property prediction',
    url='https://github.com/ecrl/graphchem',
    author='Travis Kessler',
    author_email='Travis_Kessler@student.uml.edu',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'torch==1.10.2',
        'pytorch-nlp==0.5.0',
        'torch-scatter==2.0.9',
        'torch-sparse==0.6.12',
        'torch-geometric==2.0.3'
    ],
    package_data={
        'graphchem': [
            'datasets/static/*'
        ]
    },
    zip_safe=False
)
