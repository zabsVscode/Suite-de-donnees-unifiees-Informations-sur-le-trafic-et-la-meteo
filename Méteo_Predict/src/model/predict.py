import pandas as pd
import joblib

def make_prediction(model, new_data):
    return model.predict(new_data)

if __name__ == "__main__":
    model = joblib.load('../model/trained_model.pkl')  # Assure-toi de sauvegarder ton modèle après l'entraînement
    new_data = pd.read_csv('../data/processed_data/new_data.csv')  # Remplace par les nouvelles données
    predictions = make_prediction(model, new_data)
    print(predictions)
