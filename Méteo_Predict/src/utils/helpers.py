def clean_data(data):
    # Exemple de nettoyage de données
    return data.dropna()  # Enlève les valeurs manquantes

def save_to_csv(data, file_path):
    data.to_csv(file_path, index=False)
