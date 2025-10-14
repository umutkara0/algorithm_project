from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from synonym_map import synonym_map
from deneme import temalar
from check_inconsistencies import check_inconsistencies
from check_inconsistencies import except_sentiment_analyzer
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Türkçe sentiment analiz modeli (savasy)
model = AutoModelForSequenceClassification.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
sentiment_analyzer = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model)



def find_best_match(query, synonym_map):
    best_match = None
    real_match = None
    best_score = 0
    print(f"Finding best match for: {query}")

    # query'yi küçük harfe çevirip kelimelere ayıralım
    query_words = query.lower().split()

    for key, synonyms in synonym_map.items():
        print(f"Keyler kontrol ediliyor: {key}")
        
        # Key'i kelimelere ayırıp karşılaştırmak için
        key_words = key.lower().split()  # key'yi kelimelere ayır
        score = fuzz.token_set_ratio(" ".join(query_words), " ".join(key_words))  # Kelimelere dayalı karşılaştırma
        print(f"Comparing with key: {key} | Score: {score}")
        
        if score > best_score:
            best_score = score
            best_match = key
            real_match = key
        
        # Eğer score düşükse, synonym'lerle karşılaştır
        if best_score < 70:
            print(f"Synonymler kontrol ediliyor: {key}")
            for synonym in synonyms:
                synonym_words = synonym.lower().split()  # synonym'i kelimelere ayır
                score = fuzz.token_set_ratio(" ".join(query_words), " ".join(synonym_words))
                print(f"Comparing with synonym: {synonym} | Score: {score}")
                if score > best_score:
                    best_score = score
                    real_match = synonym
                    best_match = key  # Burada synonym kaydedeceğiz

    if best_score < 50:
        print("Eşleşme Bulunamadı")
        return None
    
    print(f"En iyi eşleşme '{query}': {real_match} şu skorla: {best_score}")
    print("\n\n\n")
    return best_match

# cevaplar etiketleniyor: evet/hayır
def normalize_answer_sentiment(answer):
    print("bert-base-turk çalıştı")
    text = str(answer).strip().lower()
    try:
        #geçici
        if answer == "evliyim":
            return "evet"
        result = sentiment_analyzer(text)[0]["label"]
        print("returnden önce")
        if result == "positive":
            return "evet"
        elif result == "negative":
            return "hayır"
        else:
            return text  # unknown label
    except Exception as e:
        print(f"Sentiment analizi hatası: {e}")
        return text  # hata varsa orijinalini döndür



def generate_new_data(data, synonym_map):
    print("Starting to generate new data...")
    new_data = []
    matched_columns = {}  # Eşleşen başlıkları önbelleğe almak için bir sözlük oluşturuyoruz

    # Tüm başlıklar için eşleşmeleri önceden bul
    for col in data.columns:
        matched_column = find_best_match(col, synonym_map)
        if matched_column:
            matched_columns[col] = matched_column  # Başlık eşleşmesini saklıyoruz
        else:
            matched_columns[col] = col  # Eşleşme bulunmazsa, orijinal başlık kullanılır

    # Eşleşmeleri bulduktan sonra, her satırda bu eşleşmeleri kullanarak işlem yapalım
    for _, row in data.iterrows():
        new_row = {}
        for col in row.keys():
            matched_column = matched_columns.get(col, col)  # Eğer eşleşme bulduysak, onu kullanıyoruz
            value = row[col]  # cevabı al
            if matched_column.lower() not in except_sentiment_analyzer:
                value = normalize_answer_sentiment(value)  # Sentiment analizi yap
            new_row[matched_column] = value  # Eşleşen sütunu yeni satıra ekliyoruz
        new_data.append(new_row)

    # Yeni veriyi DataFrame'e dönüştürüp CSV olarak kaydedebiliriz
    new_df = pd.DataFrame(new_data)
    new_df.to_csv('data/new_data.csv', index=False)
    print("Yeni CSV dosyası 'data/new_data.csv' olarak kaydedildi.")

    # Test etmek için bazı cümleler
    print(sentiment_analyzer("Kesinlikle yaptım"))
    print(sentiment_analyzer("Yapmadım asla"))
    print(sentiment_analyzer("çalışıyorum"))
    return new_df


def check_all_inconsistencies(data):
    for index, row in data.iterrows():
        issues = check_inconsistencies(row)
        if issues:
            print(f"Satır {index + 1} - Tutarsızlıklar: {issues}")
        else:
            print(f"Satır {index + 1} - Tutarsızlık yok")
