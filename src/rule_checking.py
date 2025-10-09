from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from synonym_map import synonym_map



def find_best_match(query, synonym_map):
    best_match = None
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
        
        # Eğer score düşükse, synonym'lerle karşılaştır
        if best_score < 70:
            print(f"Synonymler kontrol ediliyor: {key}")
            for synonym in synonyms:
                synonym_words = synonym.lower().split()  # synonym'i kelimelere ayır
                score = fuzz.token_set_ratio(" ".join(query_words), " ".join(synonym_words))
                print(f"Comparing with synonym: {synonym} | Score: {score}")
                if score > best_score:
                    best_score = score
                    best_match = synonym  # Burada synonym kaydedeceğiz

    if best_score < 70:
        print("Eşleşme Bulunamadı")
        return None
    
    print(f"En iyi eşleşme '{query}': {best_match} şu skorla: {best_score}")
    return best_match


def generate_new_data(data, synonym_map):
    print("Starting to generate new data...")
    new_data = []
    for _, row in data.iterrows():
        new_row = {}
        for col in row.keys():
            print(f"Başlık kontrol ediliyor: {col}")
            matched_column = find_best_match(col, synonym_map)
            if matched_column:
                print(f"Eşleşme Bulundu '{col}': {matched_column}")
                print("\n\n")
                new_row[matched_column] = row[col]  # Eşleşen sütunu yeni satıra ekliyoruz
        new_data.append(new_row)

    # Yeni veriyi DataFrame'e dönüştürüp CSV olarak kaydedebiliriz
    new_df = pd.DataFrame(new_data)
    new_df.to_csv('data/new_data.csv', index=False)
    print("Yeni CSV dosyası 'data/new_data.csv' olarak kaydedildi.")
    return new_df

def check_inconsistencies(row):
    issues = []
    
    # Yaş < 18 ve Çalışıyor = Evet
    if "yaş" in row and "çalışıyor musunuz?" in row:  # Sütunlar varsa kontrol et
        if int(row["yaş"]) < 18 and row["çalışıyor musunuz?"] == "evet":
            issues.append("18 yaş altı çalışıyor")
    
    # Kadın ve Askerlik yaptı = Evet
    if "cinsiyet" in row and "askerlik yaptı mı?" in row:  # Sütunlar varsa kontrol et
        print("girdi")
        if row["cinsiyet"] == "kadın" and row["askerlik yaptı mı?"] == "evet":
            issues.append("Kadın askerlik yaptı")
    
    # Eğitim seviyesi = Üniversite, yaş < 15 (eğitim seviyesi verisi yoksa bu kural atlanır)
    if "eğitim seviyesi" in row and "yaş" in row:  # Eğitim seviyesi sütunu varsa
        if row["eğitim seviyesi"] == "üniversite" and int(row["yaş"]) < 15:
            issues.append("Üniversite öğrencisi ama yaş 15'ten küçük")
    
    # Evli = Hayır, Çocuk var = Evet
    if "evli" in row and "çocuk Var" in row:
        if row["evli"] == "hayır" and row["çocuk var"] == "evet":
            issues.append("Evli değil ama çocuk var")
    
    # Gelir = 0, Harcamalar = 5000 TL
    if "gelir" in row and "harcamalar" in row:  # Harcamalar sütunu varsa
        if int(row["gelir"]) == 0 and int(row["harcamalar"]) > 3000:
            issues.append("Gelir 0, harcama 3000 TL'den fazla")
    
    return issues


def check_all_inconsistencies(data):
    for index, row in data.iterrows():
        issues = check_inconsistencies(row)
        if issues:
            print(f"Satır {index + 1} - Tutarsızlıklar: {issues}")
        else:
            print(f"Satır {index + 1} - Tutarsızlık yok")
