from fastapi import FastAPI
from typing import Union
import pandas as pd
app = FastAPI()
df1 = pd.read_csv('F:\FA_Data1.2-20230415T170142Z-001\Data1.2\df1.csv')
@app.get("/")
def read_root():
    return {"Hola henries, este es mi PI1"}


#1
@app.get('/get_max_duration/{año}/{plataforma}/duration_type')
def get_max_duration(release_year: int, platform: str, duration_type: str):
   # Filtramos las películas del año, plataforma y tipo de duración específicos
    filtered_df = df1[(df1['tipo'] == 'movie') & (df1['año_realiacion'] == release_year) & 
                            (df1['plataforma'] == platform) & (df1['duration_type'] == duration_type)]
    
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

    df1 = pd.read_csv('Data1.2\df1 (1).csv')

# Convertir la columna "elenco" en filas separadas
    df1 = df1.assign(elenco=df1['elenco'].str.split(','))

# Convertir la columna "elenco" en filas separadas
    df1 = df1.explode('elenco')

# Contar cuántas veces aparece cada actor en la columna "elenco"
    actor_counts = df1['elenco'].value_counts()

# Encontrar el actor que aparece con mayor frecuencia
    respuesta = actor_counts.idxmax()

# Encontrar la fila correspondiente en el DataFrame original
    respuesta1 = df1.loc[df1['elenco'] == actor_counts.idxmax()]

    return {
        'plataforma': plataforma,
        'anio': anio,
        'actor': respuesta,
        #'apariciones': respuesta1
    }


#5
@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    df_filt = df1[(df1['tipo'] == tipo) & (df1['pais'] == pais) & (df1['año_realiacion'] == anio)]
    
    # Contar la cantidad de productos
    num_prods = len(df_filt)
    
    # Crear un diccionario con el resultado
    respuesta = {'pais': pais, 'anio': anio, 'pelicula': num_prods} 
    
    return {'pais': pais, 'anio': anio, 'peliculas': respuesta}

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