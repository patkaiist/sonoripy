from syllabipy import syllabify

if __name__ == "__main__":
    # Test the syllabify function
    test_cases = [
        "tʃɛʃcɪna",
        "hɛloʊ",
        "kæt", 
        "strɪŋ",
        "ɪmpɔrtənt",
        "fɪlɒsəfi"
    ]
    
    for test in test_cases:
        result = syllabify(test)
        print(f"Input: {test} → Output: {result}")