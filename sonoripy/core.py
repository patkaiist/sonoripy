def syllabify(inputstring):
    """
    Syllabify an IPA string based on sonority principles.

    Args:
        ipa (str): The IPA string to syllabify

    Returns:
        str: The syllabified string with syllable boundaries marked by dots

    Example:
        >>> from syllabipy import syllabify
        >>> syllabify("tʃɛʃcɪna")
        'tʃɛʃ.cɪ.na'
    """
    disallowOnsetClusters = True
    disallowCodaClusters = True

    ipa = (
        inputstring.replace("kʰ", "ㅋ")
        .replace("tʰ", "ㅌ")
        .replace("pʰ", "ㅍ")
        .replace("tʃ", "ʧ")
        .replace("ʈʃ", "ꭧ")
        .replace("ʈʃʰ", "ƈ")
        .replace("ʧʰ", "ㅊ")
        .replace("bʰ", "в")
        .replace("ɡ", "g")
        .replace("gʰ", "г")
        .replace("ts", "ʦ")
        .replace("ʦʰ", "ㅈ")
        .replace("dz", "ʣ")
        .replace("dʒ", "ʤ")
        .replace("tɕ", "ʨ")
        .replace("p'", "п")
        .replace("t'", "т")
        .replace("k'", "к")
        .replace(".", "")
        .strip()
    )
    
    # These are the default values. You may need to change this for language-specific hierarchies.
    sonority = [
        ["ㅋ", "ㅍ", "ㅌ", "p", "t", "k", "ʈ", "q", "c", "п", "т", "к"], # voiceless plosives
        ["ɠ", "ɗ", "ɓ"], # implosives
        ["b", "d", "g", "ɖ", "ɖ", "ɟ", "ɢ", "в"], # voiced plosives
        ["ʧ", "ʨ", "ㅊ", "ㅈ", "ʦ", "ʤ", "ʣ", "ꭧ", "ƈ"], # affricates
        ["ç","ʂ", "f", "s", "ʃ", "θ", "x", "χ", "h", "ɸ", "ʕ", "ħ", "ɮ"], # voiceless fricatives
        ["ʝ","ʐ", "v", "z", "ʒ", "ð", "ɣ", "ʁ", "ɦ", "β", "ɬ", "ʢ"], # voiced fricatives
        ["m", "n", "ŋ", "ɲ", "ɴ", "ɱ"], # nasals
        ["l", "ɭ", "ʎ", "ɹ"], # liquids
        ["j", "w", "ɥ"], # glides
        ["ɾ", "ɽ"], # taps
        ["r", "ʀ", "ʙ"], # trills
        ["i", "ɪ", "u", "ʊ", "y", "ɨ", "ɯ"], # high vowels
        ["e", "ɛ", "ə", "o", "ɔ", "ʌ", "ø", "œ"], # mis vowels
        ["a", "ɑ", "ɒ", "æ", "ɐ"] # low vowels
    ]

    def get_sonority(phoneme):
        for index, phonemes in enumerate(sonority):
            if phoneme in phonemes:
                return index
        return -1

    phones = list(ipa)
    sonorityValues = [get_sonority(p) for p in phones]
    isVowel = lambda index: sonorityValues[index] >= 8
    vowelIndices = [i for i in range(len(sonorityValues)) if isVowel(i)]

    if len(vowelIndices) <= 1:
        return inputstring

    boundaries = []
    disallowedClustersSet = set()

    for i in range(len(vowelIndices) - 1):
        v1 = vowelIndices[i]
        v2 = vowelIndices[i + 1]

        if v2 == v1 + 1:
            continue

        start = v1 + 1
        end = v2
        cluster = phones[start:end]
        clusterSonority = sonorityValues[start:end]

        split = 0
        for j in range(len(clusterSonority) - 1, 0, -1):
            if clusterSonority[j - 1] < clusterSonority[j]:
                split = j
                break

        codaIndex = start + split - 1
        while codaIndex >= start:
            codaPhone = phones[codaIndex]
            codaIndex -= 1

        if split < 0:
            split = 0

        if disallowCodaClusters and split > 1:
            split = 1

        if split > 0:
            codaCluster = "".join(phones[start : start + split])
            if codaCluster in disallowedClustersSet:
                split = 0

        boundaries.append(start + split)

    syllables = []
    prev = 0
    for boundary in boundaries:
        syllables.append(phones[prev:boundary])
        prev = boundary
    syllables.append(phones[prev:])

    if disallowOnsetClusters:
        for i in range(1, len(syllables)):
            syll = syllables[i]
            vowelPos = -1
            for j in range(len(syll)):
                if get_sonority(syll[j]) >= 8:
                    vowelPos = j
                    break
            if vowelPos > 0:
                excessOnset = syll[: vowelPos - 1]
                syllables[i - 1].extend(excessOnset)
                del syll[: vowelPos - 1]

    for i in range(1, len(syllables)):
        syll = syllables[i]
        vowelPos = -1
        for j in range(len(syll)):
            if get_sonority(syll[j]) >= 8:
                vowelPos = j
                break
        if vowelPos > 0:
            onsetCluster = "".join(syll[:vowelPos])

    resultSyllables = ["".join(syl) for syl in syllables]
    result = ".".join(resultSyllables)
    result = (
        result.replace("ㅋ", "kʰ")
        .replace("ㅌ", "tʰ")
        .replace("ㅍ", "pʰ")
        .replace("ρ", "rʰ")
        .replace("ꭧ", "ʈʃ")
        .replace("ƈ", "ʈʃʰ")
        .replace("ㅈ", "ʦʰ")
        .replace("ξ", "ks")
        .replace("ζ", "tz")
        .replace("ㅊ", "ʧʰ")
        .replace("в", "bʰ")
        .replace("г", "gʰ")
        .replace("п", "p'")
        .replace("т", "t'")
        .replace("к", "k'")
        .replace("-", ".")
        .replace(" ", ".")
        .replace(")", " ) ")
        .replace("(", " ( ")
        .replace(". ", " ")
        .replace(" .", " ")
        .replace("..", ".")
    )

    return result