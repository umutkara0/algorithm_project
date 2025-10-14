class Answer:
    def __init__(self, answer):
        self.answer = answer  # Yanıt (örneğin, evet/hayır)

    def __str__(self):
        return f"Answer(answer: {self.answer}, is_transformed: {self.is_transformed})"
    

