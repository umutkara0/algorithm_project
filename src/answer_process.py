from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from check_inconsistencies import except_sentiment_analyzer
from models.answer import Answer

model = AutoModelForSequenceClassification.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
sentiment_analyzer = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model)

class AnswerProcessor:

    def normalize_answer_sentiment(self,question, query):
        answer = Answer(query)
        if question in except_sentiment_analyzer:
            return query
        print("bert-base-turk çalıştı")
        text = str(answer.answer).strip().lower()
        try:
            #geçici
            if answer.answer == "evliyim":
                return "evet"
            result = sentiment_analyzer(text)[0]["label"]
            print("returnden önce")
            if result == "positive":
                answer.answer = "evet"
            elif result == "negative":
                answer.answer = "hayır"
            else:
                answer.answer =  "unknown"  # unknown label
            return answer.answer
        except Exception as e:
            print(f"Sentiment analizi hatası: {e}")
            return text  # hata varsa orijinalini döndür