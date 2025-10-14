import pandas as pd
from check_inconsistencies import check_inconsistencies
from synonym_map import synonym_map
from models.question import Question
from models.answer import Answer
from question_process import QuestionProcessor
from answer_process import AnswerProcessor

QueProcessor = QuestionProcessor(synonym_map)
AnsProcessor = AnswerProcessor()


def generate_new_data(data, synonym_map):
    print("Starting to generate new data...")
    new_data = []
    matched_columns = {}  # Eşleşen başlıkları önbelleğe almak için bir sözlük oluşturuyoruz

    # Tüm başlıklar için eşleşmeleri önceden bul
    for col in data.columns:
        matched_column = QueProcessor.find_best_match(col)
        matched_columns[col] = matched_column  # Başlık eşleşmesini saklıyoruz

    # Eşleşmeleri bulduktan sonra, her satırda bu eşleşmeleri kullanarak işlem yapalım
    for _, row in data.iterrows():
        new_row = {}
        for col in row.keys():
            matched_column = matched_columns.get(col, col)  # Eğer eşleşme bulduysak, onu kullanıyoruz
            value = row[col]  # cevabı al
            if matched_column.is_matched == True:
                value = AnsProcessor.normalize_answer_sentiment(matched_column.best_match, value)  # Sentiment analizi yap
            new_row[matched_column.best_match] = value  # Eşleşen sütunu yeni satıra ekliyoruz
        new_data.append(new_row)

    # Yeni veriyi DataFrame'e dönüştürüp CSV olarak kaydedebiliriz
    new_df = pd.DataFrame(new_data)
    new_df.to_csv('data/new_data.csv', index=False)
    print("Yeni CSV dosyası 'data/new_data.csv' olarak kaydedildi.")

    return new_df


def check_all_inconsistencies(data):
    for index, row in data.iterrows():
        issues = check_inconsistencies(row)
        if issues:
            print(f"Satır {index + 1} - Tutarsızlıklar: {issues}")
        else:
            print(f"Satır {index + 1} - Tutarsızlık yok")
