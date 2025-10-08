def check_inconsistencies(row):
    issues = []
    
    # Yaş < 18 ve Çalışıyor = Evet
    if "yaş" in row and "çalışıyor musunuz?" in row:  # Sütunlar varsa kontrol et
        print("girdi")
        if int(row["yaş"]) < 18 and row["çalışıyor musunuz?"] == "evet":
            issues.append("18 yaş altı çalışıyor")
    
    # Kadın ve Askerlik yaptı = Evet
    if "cinsiyet" in row and "  askerlik yaptı mı?  " in row:  # Sütunlar varsa kontrol et
        if row["cinsiyet"] == "kadın" and row["  askerlik yaptı mı?  "] == "evet":
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
