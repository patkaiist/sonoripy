function syllabify(ipa) {
  let disallowOnsetClusters = true;
  let disallowCodaClusters = true;
  let disallowedClustersSet = [];
  ipa = ipa
    .replace(/kʰ/g, "ㅋ")
    .replace(/tʰ/g, "ㅌ")
    .replace(/pʰ/g, "ㅍ")
    .replace(/tʃ/g, "ʧ")
    .replace(/ʧʰ/g, "ㅊ")
    .replace(/ts/g, "ʦ")
    .replace(/ʦʰ/g, "ㅈ")
    .replace(/dz/g, "ʣ")
    .replace(/dʒ/g, "ʤ")
    .replace(/tɕ/g, "ʨ")
    .replace(/\./g, "")
    .trim();
  const sonority = {
    a: 11,
    ɑ: 11,
    ɒ: 11,
    æ: 11,
    ɐ: 11,
    e: 10,
    ɛ: 10,
    ə: 10,
    o: 10,
    ɔ: 10,
    ʌ: 10,
    i: 9,
    ɪ: 9,
    u: 9,
    ʊ: 9,
    y: 9,
    j: 8,
    w: 8,
    ɾ: 7,
    r: 7,
    l: 6,
    ɭ: 6,
    m: 5,
    n: 5,
    ŋ: 5,
    ɲ: 5,
    v: 4,
    z: 4,
    ʒ: 4,
    ð: 4,
    ɣ: 4,
    f: 3,
    s: 3,
    ʃ: 3,
    θ: 3,
    x: 3,
    h: 3,
    ʧ: 2,
    ʨ: 2,
    ㅊ: 2,
    ㅈ: 2,
    ʦ: 2,
    ʤ: 2,
    ʣ: 2,
    b: 1,
    d: 1,
    g: 1,
    ɖ: 1,
    p: 0,
    ㅋ: 0,
    ㅍ: 0,
    ㅌ: 0,
    t: 0,
    k: 0,
    ʈ: 0,
    q: 0,
  };

  const phones = ipa.split("");
  const sonorityValues = phones.map((p) => sonority[p] ?? -1);
  const isVowel = (index) => sonorityValues[index] >= 8;
  const vowelIndices = [];
  for (let i = 0; i < sonorityValues.length; i++) {
    if (isVowel(i)) vowelIndices.push(i);
  }
  if (vowelIndices.length <= 1) return ipa;
  const boundaries = [];
  for (let i = 0; i < vowelIndices.length - 1; i++) {
    const v1 = vowelIndices[i];
    const v2 = vowelIndices[i + 1];

    if (v2 === v1 + 1) continue;

    const start = v1 + 1;
    const end = v2;
    const cluster = phones.slice(start, end);
    const clusterSonority = sonorityValues.slice(start, end);

    let split = 0;

    for (let j = clusterSonority.length - 1; j > 0; j--) {
      if (clusterSonority[j - 1] < clusterSonority[j]) {
        split = j;
        break;
      }
    }

    let codaIndex = start + split - 1;
    while (codaIndex >= start) {
      const codaPhone = phones[codaIndex];
    }

    if (split < 0) split = 0;

    if (disallowCodaClusters && split > 1) {
      split = 1;
    }

    if (split > 0) {
      const codaCluster = phones.slice(start, start + split).join("");
      if (disallowedClustersSet.has(codaCluster)) {
        split = 0;
      }
    }

    boundaries.push(start + split);
  }

  let syllables = [];
  let prev = 0;
  for (const boundary of boundaries) {
    syllables.push(phones.slice(prev, boundary));
    prev = boundary;
  }
  syllables.push(phones.slice(prev));

  if (disallowOnsetClusters) {
    for (let i = 1; i < syllables.length; i++) {
      const syll = syllables[i];
      let vowelPos = -1;
      for (let j = 0; j < syll.length; j++) {
        if (sonority[syll[j]] >= 8) {
          vowelPos = j;
          break;
        }
      }
      if (vowelPos > 0) {
        const excessOnset = syll.splice(0, vowelPos - 1);
        syllables[i - 1] = syllables[i - 1].concat(excessOnset);
      }
    }
  }

  for (let i = 1; i < syllables.length; i++) {
    const syll = syllables[i];
    let vowelPos = -1;
    for (let j = 0; j < syll.length; j++) {
      if (sonority[syll[j]] >= 8) {
        vowelPos = j;
        break;
      }
    }
    if (vowelPos > 0) {
      const onsetCluster = syll.slice(0, vowelPos).join("");
    }
  }
  const resultSyllables = syllables.map((syl) => syl.join(""));
  return resultSyllables.join(".");
}
