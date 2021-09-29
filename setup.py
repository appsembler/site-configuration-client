from setuptools import setup, find_packages

setup(
    name='site-configuration-client',
    version='0.1.0',
    description='Python client library for Site Configuration API',
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0",
    ],
    url="https://github.com/appsembler/site-configuration-client"
)
