import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyserverless",
    version="0.0.6dev1",  # Latest version .
    author="slipper",
    author_email="r2fscg@gmail.com",
    description="ok",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/uuidentifier",
    packages=setuptools.find_packages(),
    install_requires=['codefast', 'authc', 'jieba',
                      'expiringdict', 'redis', 'pika', 'hashids'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
