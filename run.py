def syllabify(ipa):
    disallowOnsetClusters = True
    disallowCodaClusters = True

    ipa = (
        ipa.replace("kʰ", "ㅋ")
        .replace("tʰ", "ㅌ")
        .replace("pʰ", "ㅍ")
        .replace("tʃ", "ʧ")
        .replace("ʧʰ", "ㅊ")
        .replace("ts", "ʦ")
        .replace("ʦʰ", "ㅈ")
        .replace("dz", "ʣ")
        .replace("dʒ", "ʤ")
        .replace("tɕ", "ʨ")
        .replace(".", "")
        .strip()
    )

    sonority = {
        "a": 11, "ɑ": 11, "ɒ": 11, "æ": 11, "ɐ": 11,
        "e": 10, "ɛ": 10, "ə": 10, "o": 10, "ɔ": 10, "ʌ": 10,
        "i": 9, "ɪ": 9, "u": 9, "ʊ": 9, "y": 9,
        "j": 8, "w": 8,
        "ɾ": 7, "r": 7,
        "l": 6, "ɭ": 6,
        "m": 5, "n": 5, "ŋ": 5, "ɲ": 5,
        "v": 4, "z": 4, "ʒ": 4, "ð": 4, "ɣ": 4,
        "f": 3, "s": 3, "ʃ": 3, "θ": 3, "x": 3, "h": 3,
        "ʧ": 2, "ʨ": 2, "ㅊ": 2, "ㅈ": 2, "ʦ": 2, "ʤ": 2, "ʣ": 2,
        "b": 1, "d": 1, "g": 1, "ɖ": 1,
        "p": 0, "ㅋ": 0, "ㅍ": 0, "ㅌ": 0, "t": 0, "k": 0, "ʈ": 0, "q": 0
    }

    phones = list(ipa)
    sonorityValues = [sonority.get(p, -1) for p in phones]
    isVowel = lambda index: sonorityValues[index] >= 8

    vowelIndices = [i for i in range(len(sonorityValues)) if isVowel(i)]
    if len(vowelIndices) <= 1:
        return ipa

    boundaries = []
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
            codaCluster = "".join(phones[start:start + split])
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
                if sonority.get(syll[j], -1) >= 8:
                    vowelPos = j
                    break
            if vowelPos > 0:
                excessOnset = syll[:vowelPos - 1]
                syllables[i - 1].extend(excessOnset)
                del syll[:vowelPos - 1]

    for i in range(1, len(syllables)):
        syll = syllables[i]
        vowelPos = -1
        for j in range(len(syll)):
            if sonority.get(syll[j], -1) >= 8:
                vowelPos = j
                break
        if vowelPos > 0:
            onsetCluster = "".join(syll[:vowelPos])

    resultSyllables = ["".join(syl) for syl in syllables]
    return ".".join(resultSyllables)

print(syllabify("tʃɛʃcɪna"))
