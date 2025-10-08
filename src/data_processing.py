import pandas as pd

def load_data(file_path):
    """CSV dosyasını yükler ve DataFrame olarak döndürür."""
    try:
        df = pd.read_csv(file_path)
        print(f"Veri başarıyla yüklendi. Toplam {len(df)} satır var.")
        return df
    except Exception as e:
        print(f"Veri yüklenirken hata oluştu: {e}")
        return None


def convert_data(data):
    data.columns = data.columns.str.strip()
    data.columns = data.columns.str.lower()  #başlıklar küçük harfe dönüştürülde
    data = data.apply(lambda col: col.map(lambda x: x.lower() if isinstance(x, str) else x)) # sütunlar küçük harfe dönüştürüldü
    return data