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
    
    # Gelir = 0, Harcamalar = 5000 TL
    if "gelir" in row and "harcamalar" in row:  # Harcamalar sütunu varsa
        if int(row["gelir"]) < int(row["harcamalar"]):
            issues.append("Gelir, harcamalardan düşük!")

    if "yaş" in row and "evli" in row:
        if int(row["yaş"]) < 18 and row["evli"] == "evet":
            issues.append("18 yaş altı evli")

    # Yaş < 18 ve Çocuk Durumu = Evet
    if "yaş" in row and "çocuk var" in row:
        if int(row["yaş"]) < 18 and row["çocuk var"] == "evet":
            issues.append("18 yaş altı çocuk sahibi")

    if "yaş" in row and "çalışıyor musunuz?" in row:
        if int(row["yaş"]) > 70 and row["çalışıyor musunuz?"] == "evet":
            issues.append("70 yaş üstü çalışıyor")

    if "gelir" in row and "çalışıyor musunuz?" in row:
        if int(row["gelir"]) == 0 and row["çalışıyor musunuz?"] == "evet":
            issues.append("Gelir sıfır, ancak çalışıyor")
    
    return issues

except_sentiment_analyzer = {"yaş", "gelir", "harcamalar", "cinsiyet", "eğitim seviyesi"} #cevaplarda yaş cinsiyet vs evet/hayıra çevrilmeyecek