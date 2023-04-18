# Importamos las librerias con la que vamos a trabajar

import os
import pandas as pd
from fastapi import FastAPI


# Establecemos directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "files/cache")
# Establecemos el dataset
dataset = os.path.join(CACHE_DIR, 'stream-data.csv')

app = FastAPI()

# Mensaje por defecto
@app.get('/')
def read_root():
    return {"Hola": "Bienvenido a mi API :)... dirigirse a /docs"}


@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    '''
    Funcion para devolver pelicula con mayor duracion segun año, plataforma y tipo de duracion.

    anio: Año de lanzamiento de la pelicula. 
    EX: 2018

    plataforma: Nombre de la plataforma .
    EX: netflix

    dtype: tipo de duracion. 
    EX: min
    '''
    df = pd.read_csv(dataset)
    df = df[(df['platform']==plataforma) & (df['release_year']==anio) & (df['duration_type']==dtype) & (df['type']=='movie')].sort_values(by=['duration_int', 'title']).iloc[-1]
    return {'pelicula': df["title"]}



@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
    '''
    Funcion para devolver cantidad de peliculas segun plataforma, con un puntaje mayor a XX en determinado año.

    plataforma: Nombre de la plataforma.
    EX: netflix

    scored: Puntaje de la pelicula.
    EX: 3.5

    anio: Año de lanzamiento de la pelicula.
    EX: 2018
    '''
    df = pd.read_csv(dataset)
    df = df[(df['platform']==plataforma) & (df['score']>=scored) & (df['release_year']==anio) & (df['type']=='movie')]
    return {
        'plataforma': plataforma,
        'cantidad': len(df),
        'anio': anio,
        'score': scored
    }


@app.get('/get_count_platform/{plataforma}')
def get_count_platform(plataforma: str):
    '''
    Funcion para devolver cantidad de peliculas totales segun plataforma.

    plataforma: Nombre de la plataforma.
    EX: netflix
    '''
    df = pd.read_csv(dataset)
    df = df[(df['platform']==plataforma) & (df['type']=='movie')]
    return {'plataforma': plataforma, 'peliculas': len(df)}

@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):
    '''
    Funcion para devolver actor que mas se repite segun plataforma y año.

    plataforma: Nombre de la plataforma.
    EX: netflix

    anio: Año de lanzamiento de la pelicula.
    EX: 2018
    '''
    df = pd.read_csv(dataset)
    df = df[(df['platform']==plataforma) & (df['release_year']==anio)]
    df['cast'] = df['cast'].str.split(',')
    df = df.explode('cast')
    return {
        'plataforma': plataforma,
        'anio': anio,
        'actor': df["cast"].value_counts().index.tolist()[0],
        'apariciones': df["cast"].value_counts().values.tolist()[0]
    }


@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    '''
    Funcion para devolver cantidad de contenidos/productos disponibles que se publico segun pais y año.

    tipo: Tipo de contenido.
    EX: movie

    pais: Nombre del pais de origen.
    EX: canada

    anio: Año de lanzamiento de la pelicula.
    EX: 2018
    '''
    df = pd.read_csv(dataset)
    df = df[(df['type']==tipo) & (df['country']==pais) & (df['release_year']==anio)]
    return {'pais': pais, 'anio': anio, 'peliculas': len(df)}

@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    '''
    Funcion para devolver cantidad de contenidos/productos disponibles segun clasificacion por edades.

    rating: Clasificacion por edades.
    EX: 13+
    '''
    df = pd.read_csv(dataset)
    df = df[(df['rating']==rating)]
    return {'rating': rating, 'contenido': len(df)}


@app.get('/get_recomendation/{title}')
def get_recomendation(title):
    '''
    Funcion para devolver una lista de Python con 5 peliculas/series recomendadas a partir del nombre
    '''
    # Para el sistema de recomendacion, vamos a utilizar el contenido de la pelicula/show para encontrar similitudes
    # y dar la recomendacion en base a cuales son los mas similares
    df = pd.read_csv(dataset)

    # utilizamos solo el primer valor den la columna "listed_in"
    df['listed_in'] = df['listed_in'].apply(lambda x: x.split(",")[0])
    df = df.dropna(how='any', subset=['cast', 'director'])
    # creamos una mascara con los siguientes datos
    features=['director' , 'cast', 'description', 'title']
    filters = df[features]

    # Creamos columna de metadatos 'soup' para que el vectorizador lo utilice 
    def create_soup(x):
        return x['director'] + ' ' + x['cast'] + ' ' + x['description']
    filters['soup'] = filters.apply(create_soup, axis=1)

    # Importamos CountVectorizer y creamos el conteo de la matriz
    from sklearn.feature_extraction.text import CountVectorizer

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(filters['soup'])

    # Importamos cosine_similarity para calcular la similaridad de los cosenos basados en count_matrix
    from sklearn.metrics.pairwise import cosine_similarity

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # Restablecemos los indices y constriumos un mapeo inverso
    filters = filters.reset_index()
    indices = pd.Series(filters.index, index=filters['title'])

    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:6]

    movie_indices = [i[0] for i in sim_scores]

    
    return {'recomendacion': df['title'].iloc[movie_indices]}


