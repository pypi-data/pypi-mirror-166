from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='gver',
    version='0.0.1',
    description='gver',
    url='https://github.com/chunribu/gver',
    author='Jian Jiang',
    author_email='jianjiang.bio@gmail.com',
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={'': ['*.svg']},
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='Manim',
)