from sklearn.feature_extraction.text import CountVectorizer

# Example text
text = ["hello", "world"]

# Generate character-level n-grams (2 to 3 characters)
vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
ngrams = vectorizer.fit_transform(text)

# Output feature names
print(vectorizer.get_feature_names_out())
