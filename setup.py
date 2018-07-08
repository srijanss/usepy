import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='usepy',
    version='0.0.1',
    author='Srijan Manandhar',
    author_email='srijan.manandhar@gmail.com',
    description='Python cli to run commands like copy, delete, mv, rename etc.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ),
)