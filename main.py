from fastapi import FastAPI
import pandas as pd
app = FastAPI()
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from typing import List
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


df1 = pd.read_csv('https://github.com/Bearodriguez2022/FastApi_PI1/blob/master/Data1.2/df1.csv')
# Convertir el DataFrame a una cadena JSON y guardarla en un archivo
df1.to_json('archivo.json', orient='records')


@app.get("/")
def read_root():
    return {"Hola henries, este es mi PI1"}


#1
@app.get('/get_max_duration/{año}/{plataforma}/duration_type')
def get_max_duration(release_year: int, plataforma: str, duration_type: str):
   # Filtramos las películas del año, plataforma y tipo de duración específicos
    filtered_df = df1[(df1['tipo'] == 'movie') & (df1['año_realiacion'] == release_year) & 
                            (df1['plataforma'] == plataforma) & (df1['duration_type'] == duration_type)]
    
    # Ordenamos por duración de mayor a menor y seleccionamos el primer título (el de mayor duración)
    max_duration_movie = filtered_df.sort_values(by='duration_int', ascending=False).iloc[0]['titulo']
    respuesta = max_duration_movie

    return {'pelicula':respuesta}

#2    
@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
   
    pelis_por_puntaje = df1[(df1["plataforma"] == plataforma) & (df1["puntuacion"] >= scored) & (df1["tipo"] == "movie") & (df1["año_realiacion"] == anio)]
    
    # contar la cantidad de películas
    count = len(pelis_por_puntaje)
    respuesta = count
    return {
        'plataforma': plataforma,
        'cantidad': respuesta,
        'anio': anio,
        'score': scored
    }

#3
@app.get('/get_count_platform/{plataforma}')
def get_count_platform(plataforma: str):
     # Filtrar solo películas
    df_movies = df1.loc[df1['tipo'] == 'movie']

    # Filtrar por plataforma
    df_filtered = df_movies.query("plataforma == @plataforma")

    # Contar el número de películas resultantes
    count = len(df_filtered)

    respuesta = count
    return {'plataforma': plataforma, 'peliculas': respuesta}
#4
@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):
    platforms = ["amazon", "disney", "hulu", "netflix"]
    if plataforma not in platforms:
        return ("Plataforma incorrecta! Debe ingresar una de las siguientes: amazon, disney, hulu, netflix")
    # Verificar que el año esté dentro del rango válido
    if anio is not None and anio < 1916:
        raise ValueError("El año debe de ser mayor a 1920")
    # Filtrar las películas para la plataforma y año especificado
    df_filtered = df1[(df1.plataforma == plataforma) & (df1.año_realiacion == anio)]
         # Poner el cast en un array para poder hacer el recorrido
    df_cast_filtered= df_filtered.assign(actor=df_filtered.elenco.str.split(',')).explode('elenco')
    # Contar la cantidad de apariciones de cada actor
    actor_count = df_cast_filtered.elenco.value_counts()
    # Obtener el actor que más se repite y su cantidad de apariciones
    max_actor = actor_count.index[0]
    max_count = int(actor_count.iloc[0])
    actor = dict({'actor': max_actor, 'count': max_count})
    respuesta = max_actor
    respuesta1 = max_count
    return {
        'plataforma': plataforma,
        'anio': anio,
        'actor': respuesta,
        'apariciones': respuesta1
    }


#5
@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    df_filt = df1[(df1['tipo'] == tipo) & (df1['pais'] == pais) & (df1['año_realiacion'] == anio)]
    
    # Contar la cantidad de productos
    num_prods = len(df_filt)
    
    # Crear un diccionario con el resultado
    respuesta = {'pais': pais, 'anio': anio, 'contenido': num_prods} 
    
    return {'pais': pais, 'anio': anio, 'contenido': respuesta}

#6
@app.get('/get_contents/{rating}')
def get_contents(rating: str):
     # Contar cuántas veces aparece cada rating de audiencia
    rating_counts = df1['clasificacion'].value_counts()
    
    # Filtrar el DataFrame por el rating de audiencia deseado
    filtered_df = df1[df1['clasificacion'] == rating]
    
    # Contar cuántas filas quedan
    respuesta= len(filtered_df)
    
    
    return {'rating': rating, 'contenido': respuesta} 



le = LabelEncoder()
df1['elenco_encoded'] = le.fit_transform(df1['elenco']) 
df1['titulo_encoded'] = le.fit_transform(df1['titulo'])

scl = StandardScaler()
X = df1[['titulo_encoded', 'puntuacion','elenco_encoded']]
y = df1[ 'puntuacion']
X = scl.fit_transform(X)
features_mean = ['titulo_encoded', 'elenco_encoded', 'puntuacion']
df_train = df1[features_mean]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X = df_train[['titulo_encoded', 'puntuacion','elenco_encoded']]
y = df_train[ 'puntuacion']

k = 5
knn = KNeighborsRegressor(n_neighbors=k)
knn.fit(X_train, y_train)
X = df1[['titulo_encoded', 'puntuacion', 'elenco_encoded']].values

# Escalar los datos
scl = StandardScaler()
X = scl.fit_transform(X)

# Entrenar el modelo de vecinos cercanos
knn_model = NearestNeighbors(metric='cosine', algorithm='auto')
knn_model.fit(X)



@app.get('/get_recomendation/{title}')
def get_recomendation(title:str):
    # Obtener el índice de la película seleccionada
    idx = df1[df1['titulo'] == title].index[0]

    # Obtener los vecinos cercanos a la película seleccionada
    distances, indices = knn_model.kneighbors(X[idx].reshape(1, -1), n_neighbors=6)

    # Obtener los títulos de las películas recomendadas
    recommended_movies = df1.iloc[indices[0][1:]]['titulo'].tolist()

    respuesta = recommended_movies 
    return {'recomendacion':respuesta}
