from fastapi import FastAPI
import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "Projecto/cache")

dataset = os.path.join(CACHE_DIR, 'stream-data.csv')


app = FastAPI()


# ///////////////////////////////////////////////////////////

@app.get('/')
def read_root():
    return {"Hello": "World"}


@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    df = pd.read_csv(dataset)
    df = df[(df['platform']==plataforma) & (df['release_year']==anio) & (df['duration_type']==dtype) & (df['type']=='movie')].sort_values(by=['duration_int', 'title']).iloc[-1]
    return {'pelicula': df["title"]}



@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
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
    df = pd.read_csv(dataset)
    df = df[(df['platform']==plataforma) & (df['type']=='movie')]
    return {'plataforma': plataforma, 'peliculas': len(df)}

@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):
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
    df = pd.read_csv(dataset)
    df = df[(df['type']==tipo) & (df['country']==pais) & (df['release_year']==anio)]
    return {'pais': pais, 'anio': anio, 'peliculas': len(df)}

@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    df = pd.read_csv(dataset)
    df = df[(df['rating']==rating)]
    return {'rating': rating, 'contenido': len(df)}


# ///////////////////////////////////////////////////////////
'''



@app.get('/get_recomendation/{title}')
def get_recomendation(title,):
    
    return {'recomendacion':respuesta}'''
