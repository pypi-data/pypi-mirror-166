import setuptools
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Image2Story", # Replace with your own username
    version="0.0.6",
    license='MIT',
    author="Falahgs.G.Saleih",
    author_email="falahgs07@gmail.com",
    description="Create Short Story from image caption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/falahgs/",
    packages=find_packages(),
    keywords = ['CLIP', 'GPT3', 'BLIP'],   # Keywords that define your package best
    install_requires=[ 'timm==0.4.12','fairscale==0.4.4','transformers','gitpython','pycocoevalcap','openai','googletrans==3.1.0a0'],
    classifiers=["Programming Language :: Python :: 3","License :: OSI Approved :: MIT License","Operating System :: OS Independent",],
    python_requires='>=3.6',)