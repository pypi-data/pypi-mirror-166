from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "ReadMe.md").read_text()

setup(
    name='vulnman_default_templates',
    version='0.1.1',
    packages=find_packages(),
    url='',
    license='',
    author='user',
    author_email='',
    include_package_data=True,
    description='Default vulnman templates',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
