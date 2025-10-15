"""
sonoriPy: A Python package for IPA syllabification.

This package provides functionality to syllabify International Phonetic Alphabet (IPA)
transcriptions based on sonority principles.
"""

from .core import syllabify

__version__ = "0.0.1"
__author__ = "Kellen Parker van Dam"
__email__ = "kellenparker@gmail.com"

__all__ = ["syllabify"]
