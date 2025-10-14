class Question:
    def __init__(self, query):
        self.query = query  # Sorgu (örneğin, anket sorusu)
        self.best_match = None  # En iyi eşleşme
        self.real_match = None  # Gerçek eşleşme
        self.best_score = 0  # Eşleşme skoru
        self.is_matched = False

    def set_match(self, best_match, real_match, best_score, is_matched):
        self.best_match = best_match
        self.real_match = real_match
        self.best_score = best_score
        self.is_matched = is_matched

    def __str__(self):
        return f"En iyi eşleşme(Soru: {self.query}, best_match: {self.best_match}, real_match: {self.real_match}, best_score: {self.best_score})" #print(obje) yaptığında bu fonk #çalışıyor ve yazdırıyor
    

    
