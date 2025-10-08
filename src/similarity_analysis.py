import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Türkçe dil modeli
nlp = spacy.load("tr_core_news_sm")

def preprocess_text(text):
    """Metin üzerinde temel ön işleme yapar (stop words, noktalama işaretleri vb.)."""
    doc = nlp(text)
    return " ".join([token.text for token in doc if not token.is_stop and not token.is_punct])

def text_similarity(texts):
    """Türkçe metinler arasındaki cosine similarity'yi hesaplar."""
    processed_texts = [preprocess_text(text) for text in texts]
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(processed_texts)
    cosine_similarities = cosine_similarity(X)
    
    return cosine_similarities

# Örnek metinler
texts = [
    "Kadın hakları çok önemli bir konu.",
    "Kadınların eşit haklara sahip olması gerektiğini düşünüyorum.",
    "Erkeklerin de eşit hakları olmalı."
]

similarities = text_similarity(texts)
print(similarities)
