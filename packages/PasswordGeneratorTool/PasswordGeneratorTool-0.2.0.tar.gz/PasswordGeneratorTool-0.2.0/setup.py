from setuptools import find_packages, setup
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='PasswordGeneratorTool',
    version='0.2.0',
    author='Daniel Czarnecki',
    author_email='Daniel.Czarnecki.94@wp.pl',
    packages=find_packages(),
    include_package_data=True,
    description='Tool that will generate password from given length',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown'
)
