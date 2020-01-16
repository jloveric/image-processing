
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snovalleyai_image_processing",
    version="1.0.4",
    author="John Loverich",
    author_email="john.loverich@gmail.com",
    description="Research tool in image processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jloveric/image-processing",
    packages=setuptools.find_packages(),
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
