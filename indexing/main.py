# now i should learn about bm25 and how can i use it.
# TODO: Ranks documents based on query-term matches, rarity, frequency, and document length.

from rank_bm25 import BM25Okapi

corpus = [
    "The cat sat on the mat",
    "Dogs are great pets and love to play",
    "The cat chased the mouse around the house",
    # "Python is a popular programming language",
]

token_from_corpus = []

for doc in corpus:
    token_from_corpus.append(doc.lower().split())

bm25 = BM25Okapi(token_from_corpus)

word = "the cat"

token_word = word.lower().split()
score = bm25.get_scores(token_word)

print(score)
top_docs = bm25.get_top_n(token_word, corpus, n=2)

print(top_docs)
