from data_processing import load_data
from data_processing import convert_data
from rule_checking import check_all_inconsistencies
from rule_checking import generate_new_data
from synonym_map import synonym_map


# Veriyi yükle
file_path = 'data/responses.csv'  # Google Form yanıtları
data = load_data(file_path)
data = convert_data(data)


if data is not None:
    data = generate_new_data(data, synonym_map)
    # Yanıtları kontrol et
    check_all_inconsistencies(data)