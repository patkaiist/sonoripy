# Syllabipy

A Python package for syllabifying International Phonetic Alphabet (IPA) transcriptions based on sonority principles.

## Installation

```bash
pip install syllabipy
```

## Usage

```python
from syllabipy import syllabify

# Syllabify an IPA string
result = syllabify("tʃɛʃcɪna")
print(result)  # Output: tʃɛʃ.cɪ.na
