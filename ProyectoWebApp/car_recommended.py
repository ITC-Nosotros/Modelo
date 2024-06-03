import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import BayesianRidge
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error as MAE,r2_score
import lightgbm as lgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold
import xgboost as xgb
from sklearn.metrics import classification_report

def load_and_prepare_data():
# Cargar la información
    url = "https://raw.githubusercontent.com/ITC-Nosotros/Modelo/main/archivo_modelo.csv"
    cols = ['car_model','price','year_model','kms','colour','fuel_type','location','url_car']
    data = pd.read_csv(url, names=cols , header = 0,encoding='utf-8')

#Eliminar los valores nulos de la columna price
    data['price'] = data['price'].dropna()

# Rreemplazar '.' por valores vacios que no afecten la conversión a numerico.
    data['price'] = data['price'].str.replace('.', '')
    data['kms'] = data['kms'].str.replace('.', '')
    data['price'] = data['price'].str.replace(',', '')
    data['kms'] = data['kms'].str.replace(',', '')

# Convertir a numerico
    data['price'] = pd.to_numeric(data['price'])
    data['kms'] = pd.to_numeric(data['kms'])

# Recorre todas las columnas del DataFrame data que tienen un tipo de datos object y las convierte en categorías utilizando el método astype('category').
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].astype('category')

#eliminará todas las filas que contienen al menos un valor nulo y actualizará el DataFrame original.
    data.dropna(inplace=True)

# Preprocessing
    categorical_features = ['car_model','location']
    numeric_features = ['price','kms','year_model']

    selected_columns = categorical_features + numeric_features
    new_data = data[selected_columns]

# Display the first few rows of the new dataset
    print(new_data.head())

# Standarization (both categorical and numerical variables)
    preprocessor = ColumnTransformer(
    transformers=[
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(), categorical_features)])

# Define pipeline for regression model
    model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
    ])

#Este bloque de código divide los datos en conjuntos de entrenamiento y prueba para su posterior modelado y evaluación
    X = new_data
    y = data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Training the price prediction model (regression)
    model.fit(X_train, y_train)

    return new_data, model

def recommend_and_predict(car_features_df, data, model):

    # Preprocessing
    categorical_features = ['car_model','location']
    numeric_features = ['kms','year_model']
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ],
        remainder='drop'
    )

    # Pipeline to transformed data
    pipe = Pipeline(steps=[('preprocessor', preprocessor)])
    transformed_data = pipe.fit_transform(data.drop(['price'], axis=1))
    transformed_query = pipe.transform(car_features_df)

    # Price prediction
    predicted_price = model.predict(car_features_df)
    print(f"Predicted Price: {predicted_price[0]}")

    # Applying K-Nearest Neighbors for searching similar cars
    n_neighbors = 5
    nn = NearestNeighbors(n_neighbors=n_neighbors)
    nn.fit(transformed_data)

    # Finding the nearest neighbors for the input 'car_features_df'
    distances, indices = nn.kneighbors(transformed_query)

    # Obtaining similar cars
    similar_cars = data.iloc[indices[0]]
    
    return similar_cars, predicted_price[0]