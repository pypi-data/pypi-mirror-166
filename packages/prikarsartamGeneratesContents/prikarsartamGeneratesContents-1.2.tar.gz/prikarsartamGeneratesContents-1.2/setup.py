from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2'
DESCRIPTION = 'for generating contents on the basis of provided prompts and input lengths'
LONG_DESCRIPTION = 'A package that uses pretrained abstractive models from huggingface models for text generation and gives a rather simple way to have the result downloaded into the local directory directly from google colab'

# Setting up
setup(
    name="prikarsartamGeneratesContents",
    version=VERSION,
    author="Pritam Darkar <prikarsartam.ml>",
    author_email="<prikarsartam@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['transformers', 'torch', 'os', 'google-colab'],
    keywords=['large language model', 'text generation', 'pretrained content creation', 'AutoCausalModelforBloomLM', 'Natural Language Processing', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
