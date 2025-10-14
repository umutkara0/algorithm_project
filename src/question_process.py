from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from synonym_map import synonym_map
from deneme import temalar
from models.question import Question

class QuestionProcessor:
    def __init__(self, synonym_map):
        self.synonym_map = synonym_map

    def find_best_match(self, query):
        question = Question(query)  # Question modelini kullanıyoruz
        best_match = None
        real_match = None
        best_score = 0
        is_matched = False
        print(f"Finding best match for: {query}")
        query_words = query.lower().split()
        
        for key, synonyms in self.synonym_map.items():
            key_words = key.lower().split()
            score = fuzz.token_set_ratio(" ".join(query_words), " ".join(key_words))
            if score > best_score:
                best_score = score
                best_match = key
                real_match = key
            
            if best_score < 70:
                for synonym in synonyms:
                    synonym_words = synonym.lower().split()
                    score = fuzz.token_set_ratio(" ".join(query_words), " ".join(synonym_words))
                    if score > best_score:
                        best_score = score
                        real_match = synonym
                        best_match = key

        if best_score < 50:
            print("Eşleşme Bulunamadı")
            best_match = query
            real_match = None
        else:
            is_matched = True
            print(f"En iyi eşleşme '{query}': {real_match} şu skorla: {best_score}")
        # Sonuçları Question modeline aktaralım
        question.set_match(best_match, real_match, best_score, is_matched)
        return question
