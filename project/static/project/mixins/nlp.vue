<script>
export default {
    methods: {
        range(min, max) {
            // Returns an array with range [min, max]
            return Array.from(new Array(max - min), (x, i) => i + min);
        },
        flatten(arr) {
            // Flattens an array
            return arr.reduce((acc, val) => acc.concat(val), []);
        },
        bagify(doc) {
            // Baggify document into a list of words
            // Implement stopword removal here
            return doc.toLowerCase().split(" ");
        },
        ngrams(doc, n) {
            // Generate ngrams from document
            n = n ? n : 1;
            let words = this.bagify(doc),
                grams = [];

            for (let i = 0; i < words.length; i++) {
                if (i + n > words.length) break;
                let min = i,
                    max = i + n;
                grams.push(words.slice(min, max).join(" "));
            }
            return grams;
        },
        rangeNgrams(doc, minGram, maxGram) {
            // Generates a flat list with all ngrams from a document
            minGram = minGram ? minGram : 1;
            maxGram = maxGram ? maxGram : 3;
            let rangegrams = this.range(minGram, maxGram + 1);
            return this.flatten(rangegrams.map(n => this.ngrams(doc, n)));
        },
        corpusNgrams(corpus, n) {
            // Generates a flat list with all ngrams from a corpus
            return this.flatten(corpus.map(doc => this.ngrams(doc, n)));
        },
        corpusRangeNgrams(corpus, minGram, maxGram) {
            // Generates a flat list with all ngramns in the given range for a corpus
            minGram = minGram ? minGram : 1;
            maxGram = maxGram ? maxGram : 3;
            let rangegrams = this.range(minGram, maxGram + 1);
            return this.flatten(
                rangegrams.map(n => this.corpusNgrams(corpus, n))
            );
        },
        countVectorizeArray(arr, extra) {
            // count vectorizes a generic array
            let countVector = {};
            for (let vector in arr) {
                let term = arr[vector];
                if (countVector[term] === undefined) countVector[term] = 1;
                else countVector[term]++;
            }
            if (extra)
                for (let vector in extra) {
                    let term = extra[vector];
                    if (countVector[term] === undefined) countVector[term] = 0;
                }
            return countVector;
        },
        countVector(doc, n, ngrams) {
            // Create a count vector with ngrams from a document
            ngrams = ngrams ? ngrams : this.ngrams(doc, n);
            return this.countVectorizeArray(ngrams);
        },
        countVectorRangeGrams(doc, minGram, maxGram, extraNgrams) {
            // Generates a count vector of all ngrams in a given range for a document
            // also takes extra ngrams that are set to 0 if not found
            let ngrams = this.rangeNgrams(doc, minGram, maxGram);
            return this.countVectorizeArray(ngrams, extraNgrams);
        },
        corpusCountVector(corpus, n, ngrams) {
            // Create a list of count vectors from a corpus
            return corpus.map(doc => this.countVector(doc, n, ngrams));
        },
        corpusCountVectorRangeGrams(corpus, minGram, maxGram, ngrams) {
            ngrams = ngrams
                ? ngrams
                : this.corpusRangeNgrams(corpus, minGram, maxGram);
            return corpus.map(doc =>
                this.countVectorRangeGrams(doc, minGram, maxGram, ngrams)
            );
        },
        naiveTermFrequency(doc, term) {
            // Iteratively calculate the term frequency of a term in a document
            let n = term.split(" ").length,
                grams = this.ngrams(doc, n);
            term = term.toLowerCase();
            return (
                grams.reduce((acc, val) => {
                    return acc + (val === term);
                }, 0) / grams.length
            );
        },
        termFrequency(doc, term, countVector) {
            // Uses a pre calculated count vector to get the term frequency in a document
            if (countVector) {
                let v = countVector[term.toLowerCase()];
                return (
                    (v ? v : 0) /
                    Object.keys(countVector).reduce(
                        (acc, val) => acc + countVector[val],
                        0
                    )
                );
            } else {
                return this.naiveTermFrequency(doc, term);
            }
        },
        naiveInverseDocumentFrequency(corpus, term) {
            // Interatively calculate the inverse document frequency of a term in a corpus
            return Math.log(
                corpus.length /
                    corpus
                        .map(doc =>
                            doc.toLowerCase().includes(term.toLowerCase())
                        )
                        .reduce((acc, val) => acc + val, 0)
            );
        },
        inverseDocumentFrequency(corpus, term, corpusCountVector) {
            // Uses a pre calculated corpus count vector to get the inverse document frequency of a term in a corpus
            if (corpusCountVector) {
                return Math.log(
                    corpusCountVector.length /
                        corpusCountVector.reduce(
                            (acc, val) => acc + (val[term] ? 1 : 0),
                            0
                        )
                );
            } else {
                return this.naiveInverseDocumentFrequency(corpus, term);
            }
        },
        tfidf(corpus, doc, term, corpusCountVector, docIdx) {
            // Calculates the inverse document frequency for a term, given a document, in a corpus
            // Accepts pre calculated corpus count vector
            corpusCountVector = corpusCountVector
                ? corpusCountVector
                : this.corpusCountVector(corpus, term.split(" ").length);
            let countVector =
                corpusCountVector && docIdx
                    ? corpusCountVector[docIdx]
                    : undefined;
            let tf = this.termFrequency(doc, term, countVector),
                idf = this.inverseDocumentFrequency(
                    corpus,
                    term,
                    corpusCountVector
                );
            return tf * idf;
        },
        tfidfAllDocs(corpus, term, corpusCountVector) {
            // Generates all tfidf values for a term in a corpus
            corpusCountVector = corpusCountVector
                ? corpusCountVector
                : this.corpusCountVector(corpus, term.split(" ").length);
            return corpus.map((doc, idx) =>
                this.tfidf(corpus, doc, term, corpusCountVector, idx)
            );
        },
        tfidfAllTerms(corpus, minGram, maxGram) {
            // Generates all tfidf values for all terms in a corpus
            let ngrams = this.corpusRangeNgrams(corpus, minGram, maxGram);
            let corpusCountVector = this.corpusCountVectorRangeGrams(
                corpus,
                minGram,
                maxGram,
                ngrams
            );
            let terms = Array.from(new Set(ngrams)),
                res = {};
            for (let i = 0; i < terms.length; i++) {
                res[terms[i]] = this.tfidfAllDocs(
                    corpus,
                    terms[i],
                    corpusCountVector
                );
            }
            return res;
        }
    }
};
</script>
