import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def train_model(data):
    # Supposons que `data` est un DataFrame pandas
    X = data.drop('target_column', axis=1)  # Remplace par le nom de ta colonne cible
    y = data['target_column']  # Remplace par le nom de ta colonne cible

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    return model

if __name__ == "__main__":
    # Charger les données prétraitées ici (ex: depuis processed_data)
    data = pd.read_csv('../data/processed_data/your_processed_data.csv')  # Remplace par le bon chemin
    model = train_model(data)
    print("Modèle entraîné.")
