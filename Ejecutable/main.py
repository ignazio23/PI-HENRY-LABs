# Desarrollo API: se disponibilizan los datos de la empresa usando el framework FastAPI. 
# Se crean  6 funciones para los endpoints que se consumirán en la API,con un decorador por cada una (@app.get(‘/’))

# Se importan las librerias a utilizar
import numpy as np
import pandas as pd

from fastapi import FastAPI

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Link para API y nombramiento de la visualización web.
app = FastAPI(title='STEAM', description='Revisa los datos de interés sobre esos videojuegos que quieres adquirir o aquellos a los que tanto juegas desde reseñas de usuarios y recomendaciones, hasta horas jugadas por otros usuarios')    

#http://192.168.1.10:8000

# Importamos el primer DF
df_items_games = pd.read_parquet('items_games.parquet')

# Importamos el segundo DF
df_items_games_API = pd.read_parquet('items_games_API.parquet')

# Importamos el tercer DF
df_reviews_games_API = pd.read_parquet('reviews_games_API.parquet')

# Importamos el cuarto DF
df_games_API = pd.read_parquet('games_API.parquet')

#Función de Bienvenida.
@app.get("/")
async def index():
    mensaje = 'Bienvenidos STEAM Gaming Consult, donde podrás ver reseñas de usuarios y recomendaciones de los mismos publicadas en la plataforma'
    return {'Mensaje': mensaje}

#Función PlayTimeGenre - Total de horas jugadas en determinado género por año.
# Creamos una API para la Función PlayTimeGenre
@app.get("/PlayTimeGenre/{genre}")
def PlayTimeGenre(genre: str):
    '''
    Mediante esta función podremos observar el año con mas horas jugadas para el género ingresado.
    '''
    # Convertimos la entrada a minúsculas
    genre = genre.lower()

    # Filtramos el dataframe 'df_items_games_API' respecto al parámetro 'genre'
    genre_data = df_items_games_API[df_items_games_API['game_genre'] == genre]

    if genre_data.empty:
        return {"genre": genre, "most_played_year": None}

    # Agrupamos respecto a los años y suma de tiempo de juego
    year_playtime = genre_data.groupby('year_release')['playtime_forever'].sum()
    most_played_year = year_playtime.idxmax()

    return {"Total de horas jugadas en el género ingresado por año:"}, {"Género": genre}, {"Año con mayor horas jugadas": int(most_played_year)}


#Función UserForGenre - Total de horas en juego para el usuario con mayor cantidad de horas jugadas en determinado género.
# Creamos una API para la Función UserForGenre
@app.get("/UsersForGenre/{genre}")
def UserForGenre(genre: str):
    '''
    Mediante esta función podremos observar el usuario con la mayor cantidad de horas jugadas para el género ingresado.
    '''
    # Convertimos la entrada a minúsculas
    genre = genre.lower()

    # Filtramos el dataframe 'df_items_games_API' respecto al parámetro 'genre'
    genre_data = df_items_games_API[df_items_games_API['game_genre']== genre]

    # Agrupamos el dataframe anterior por 'user_id', por la suma del tiempo de juego y ordenamos
    group = genre_data.groupby('user_id')['playtime_forever'].sum().sort_values(ascending=False)

    # Reindexamos a valor máximo a [0]
    user = group.index[0]

    # Tomamos las filas del dataframe que contengan 'user_id'
    user_genre = genre_data[genre_data['user_id']==user]

    # Agrupamos respecto a los años y suma de tiempo de juego
    played_hours = round(user_genre.groupby('year_release')['playtime_forever'].sum(), 3)

    # Guardamos la serie 'played_hours' en una lista para su uso posterior
    total_hours_played = [f'Año: {int(anio)}, Horas: {horas}' for anio, horas in played_hours.items()]

    return {f"Usuario con más horas jugadas para género, {genre}": user, "Horas jugadas": total_hours_played}


# Función UsersRecommend - Usuarios Recomiendan
# Creamos una API para la Función UsersRecommend
@app.get("/UsersRecommend/{year}")
def UsersRecommend(year: int):
    '''
    Mediante esta función podremos observar la totalidad de recomendaciones positivas de usuarios para el año ingresado.
    '''
    # Filtramos el dataframe 'df_reviews_games_API' en base al 'year_posted' y al 'analisis_sentimiento' positivo
    filter = df_reviews_games_API[(df_reviews_games_API['recommend'] == True) & (df_reviews_games_API['analisis_sentimiento'] >= 1) & ((df_reviews_games_API['year_posted']) == year)]

    if filter.empty:
        return {"error": "No recommended games found for the given year"}

    # Agrupamos por 'game_name' y calculamos el número de recomendaciones
    recommendations = filter.groupby('game_name')['recommend'].sum()

    if recommendations.empty:
        return {"error": "No recommended games found for the given year"}

    # Ordenamos los juegos por recomendaciones positivas
    order = recommendations.sort_values(ascending=False)

    # Tomamos el top 3
    top_3 = order.head(3)

    # Creamos el resultado por posiciones
    result = [{"Top 3 Juegos Recomendados por Usuarios:"}, {"1st Place": top_3.index[0]}, {"2nd Place": top_3.index[1]}, {"3rd Place": top_3.index[2]}]

    return result


# Función UsersNotRecommend - Usuarios NO Recomiendan
# Creamos una API para la Función UsersNotRecommend
@app.get("/UsersNotRecommend/{year}")
def UsersNotRecommend(year: int):
    '''
    Mediante esta función podremos observar la totalidad de recomendaciones negativas de usuarios para el año ingresado.
    '''
    # Filtramos el dataframe 'df_reviews_games_API' en base al 'year_posted' y al 'analisis_sentimiento' negativo
    filter = df_reviews_games_API[(df_reviews_games_API['recommend'] == False) & (df_reviews_games_API['analisis_sentimiento'] == 0) & ((df_reviews_games_API['year_posted']) == year)]

    if filter.empty:
        return {"error": "No least recommended games found for the given year"}

    # Agrupamos por 'game_name' y calculamos el número de recomendaciones
    not_recommendations = filter.groupby('game_name')['recommend'].count()

    if not_recommendations.empty:
        return {"error": "No least recommended games found for the given year"}

   # Ordenamos los juegos por recomendaciones negativas
    order = not_recommendations.sort_values(ascending=True)

     # Tomamos el top 3
    top_3 = order.head(3)

    # Creamos el resultado por posiciones
    result = [{"Top 3 Juegos Recomendados NO por Usuarios:"}, {"1st Place": top_3.index[0]}, {"2nd Place": top_3.index[1]}, {"3rd Place": top_3.index[2]}]

    return result


# Función sentiment_analysis - Análisis de Sentimiento
# Creamos una API para el Análisis de Sentimiento
@app.get("/sentiment_analysis/{year}")
def sentiment_analysis(year: int):
    '''
    Mediante esta función podremos observar el Análisis de Sentimiento de los usuarios para el año ingresado.
    '''
    # Filtramos el dataframe 'df_reviews_games_API' respecto al parámetro 'year'
    filter = df_reviews_games_API[(df_reviews_games_API['year_release']) == year]

    if filter.empty:
        return {"error": "No data found for the given year"}

    # Agrupamos por el 'analisis_sentimiento' y calculamos la suma de cada sentimiento
    group_sentiments = filter.groupby(['analisis_sentimiento'])['user_id'].nunique().reset_index()

    # Renombramos alguna columna y mapearemos los valores de sentimientos por niveles 
    group_sentiments.columns = ['Sentiment', 'Count']
    sentiment_labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    group_sentiments['Sentiment'] = group_sentiments['Sentiment'].map(sentiment_labels)

    # Convertimos el DF a un diccionario
    sentiment_counts = group_sentiments.set_index('Sentiment')['Count'].to_dict()

    return sentiment_counts


# Función Recomendacion_Juego - Juego Recomendado por 'itemID'
# Creamos una instancia con: CountVectorizer
vector = CountVectorizer(tokenizer= lambda x: x.split(', '))

# Dividimos cada cadena de descripción en palabras individuales y creamos una matriz de conteo la cual mostrará cada género de cada videojuego.
matriz_description = vector.fit_transform(df_games_API['description'])

# Creamos una API para la recomendación de Juegos en base a otros Juegos, la misma tendrá ML
@app.get("/recommend_games_by_games/{item_id}")
def recomendacion_juego(game_id: int):
    '''
    Mediante esta función podremos observar la recomendación mediante el uso de ML en base a un juego ingresado.
    '''
    # Se ingresa el item_id y retornamos una lista con 5 juegos recomendados similares al ingresado (title)

    if game_id not in df_games_API['item_id'].values:
        return 'El ID no existe, intente con otro'
    else:
        index = df_games_API.index[df_games_API['item_id']==game_id][0]
        description_index = matriz_description[index]

        ''' Calculamos la similitud coseno entre la descripción de entrada y la descripción de las demás filas: cosine_similarity.
            Obtenemos los índices de las mayores similitudes mediante el método argsort() y las similitudes ordenadas de manera descendente.
            Tomamos los índices del 1 al 6 [0, 1:6] ya que el índice 0 es el mismo índice de entrada.
        '''
        
        indices_maximos = np.argsort(-cosine_similarity(description_index, matriz_description))[0, 1:6]

        recomendaciones = []
        for i in indices_maximos:
            recomendaciones.append(df_games_API['game_name'][i])
        
        return recomendaciones