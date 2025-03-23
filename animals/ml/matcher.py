import pandas as pd
from sklearn.neighbors import NearestNeighbors
from animals.models import Animal

def suggest_animals(user_preferences, k=3):
    # Example user_preferences = {"species": "Dog", "age": 2, "temperament": "Active"}

    # Get all animals
    animals = Animal.objects.all().values('id', 'species', 'age', 'temperament')

    if not animals:
        return []

    df = pd.DataFrame(list(animals))

    # Map categories to numeric for ML
    df['species_encoded'] = df['species'].astype('category').cat.codes
    df['temperament_encoded'] = df['temperament'].astype('category').cat.codes

    # Prepare the features
    features = df[['species_encoded', 'age', 'temperament_encoded']]

    # Encode user input
    user_df = pd.DataFrame([{
        'species_encoded': pd.Series(user_preferences['species']).astype('category').cat.codes.values[0],
        'age': user_preferences['age'],
        'temperament_encoded': pd.Series(user_preferences['temperament']).astype('category').cat.codes.values[0],
    }])

    # KNN matching
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(features)

    distances, indices = knn.kneighbors(user_df)
    matched_ids = df.iloc[indices[0]]['id'].tolist()

    return matched_ids