from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="syllabiPy",
    version="0.0.1",
    author="Kellen Parker van Dam",
    author_email="kellenparker@gmail.com",
    description="A Python package for IPA syllabification based on sonority principles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patkaiist/syllabipy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[],
    keywords="ipa, phonetics, syllabification, linguistics, phonology",
    project_urls={
        "Bug Reports": "https://github.com/patkaiist/syllabipy/issues",
        "Source": "https://github.com/patkaiist/syllabipy",
    },
)
