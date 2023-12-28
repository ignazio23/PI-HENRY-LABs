## Introducción ##

En el presente documento se deja registro y código del proyecto solicitado donde se busca simular un ambiente de trabajo para la plataforma STEAM, la cual necesita un sistema de recomendación de videojuegos.

Se desarrolla el sistema de recomendación mediante la realización de un completo análisis; desde la generación de un ETL, la gráficación de data con el uso de un EDA, el entrenamiento mediante ML y el despliegue del modelo de API diseñado. Los datos brindados fueron sometidos una gran carga de trabajo para poder usarlos en el modelo generado.

## Objetivos Principales ##

- Analizar y depurar los datos que nos fueron brindados para que de esta forma, mediante el uso de ciertas API, las cuales se desplegaran en un sitio web, se nos permite el consumo de estos datos.
- Desarrollar el sistema de recomendación de videojuegos solicitado.

## Objetivos Principales ##
- Interiorizar y asimilar los diferentes conceptos y metodologías visualadas a lo largo del curso.
- Llevar a cabo una comprensión del alcance y capacidades de lo aprendido, retroalimentar lo visualizado, y complementar conceptos mediante la búsqueda por mano propia.

## Paso a Paso ##

Aquí iremos describiendo cada uno de los pasos realizados, y veremos enseguida de cada título la carpeta donde se encuentra cada paso desarrollado.

1. Depuración de Data - ETL
    - Frente a la documentación presentada, nos vimos frente a ciertas dificultades las cuales fuimos solventando y corrigiendo durante el desarrollo.
    - Se realizó la extracción de datos, su transformación y su correcta limpieza, para su posterior uso.
    - Los archivos fueron depurados, y los mismos se utilizaron unicamente en la instancia de ETL, ya que esta sobre su finalización genera nuevos archivos para el mejor uso de la data.

2. Graficación y Exploración de Data - EDA
    - Se llevó a cabo la generación de diferentes gráficas las cuales nos brindan un mayor conocimiento de la data que estamos manipulando.
      
3. Machine Learning - ML
    - Se llevó a cabo un análisis exploratorio de datos, entender qué dicen las columnas de los datos y tomar desiciones sobre las columnas necesarias para el entrenamiento del modelo.
    - Se entrenaron modelos en un notebook para luego mandarlo al archivo notebook de API.
    
4. Generación de Comandos - API
    - Se generó un conjunto de comandos y funciones que nos permiten el acceso y la consulta de los datos.
    - Se llevó a cabo la prueba de las API generadas para que luego puedan ser consumidas desde un sitio web.

5. Despliegue del Desarrollo - Ejecutable
    - Se llevó a cabo el despliegue de la estructura generada en el archivo `main.py`, el cual toma las anteriores API desarrolladas para poder visualizar las consultas de datos desde un sitio web.
  
## Tecnología y Herramientas ##

1. En mayor parte se utiliza el lenguaje Python, el cual se implemento casi en su totalidad mediante interfaces Notebook.
2. Se realizó la instalación, carga y uso de diferente librerias y utilidades las cuales se podrán apreciar en las primeras líneas de código de cada apartado.

## API ##

Se desarrolla la estructura de diversas API las cuales nos brindan la posibilidad de consultar cierta información en base a la data ya depurada. Se lleva a cabo la creación de 6 endpoints, los cuales se encuentran en fase de pruebas en el apartado API, y prontos para su despligue en el archivo `main.py` - https://github.com/ignazio23/PI-HENRY-LABs/blob/main/Ejecutable/main.py

Las API desarrollas fueron:
- `PlayTimeGenre(genre)` Devuelve el año con más horas jugadas para el género de entrada.
- `UserForGenre(genre)` Devuelve el usuario con mas horas jugadas para el género de entrada.
- `UserRecommend(year)` Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año de entrada.
- `UsersNotRecommend(year)` Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año de entrada.
- `sentiment_analysis(year)` Según el año de entrada, devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
- `recommend_games_by_games(item_id)` Se ingresa el id de un producto y retorna una lista con 5 juegos recomendados similares al ingresado.

## Modelo ML ##

Se desarrolló un sistema de recomendaciones utilizando cierto contenido perteneciente a la librería `Scikit-Learn`. 

Con esta libreria implementamos diversas funciones a las columnas de categorización ('genre', 'tags' y 'specs'), para luego poder representar en forma de vectores el resultado obtenido, teniendo valor "1" la posición indicada y valor "0" las otras.

Además, se utilizaron funciones para poder calcular la similitud entre cada par de vectores.

## Despliegue ##

Para poder realizar el despliegue de las API generadas, con las cuales obtendremos en base a las consultas realizadas, la data indicada, llevamos a cabo la implementación de comandos pertenecientes a `FastAPI`.

Para poder visualizar el sitio web y probar las API diseñadas, deberemos estar ubicamos desde nuestra terminal (CMD) en la ubicación del apartado 'Ejecutable', una vez allí ejecutando el siguiente código, podremos acceder al link web designado.

    uvicorn main:app --port 8000
    
## Video de Demostración ##

Aquí les dejaré adjunto un link a un drive donde cargaré el video de demostración de lo desarrollado:

    https://drive.google.com/drive/folders/1go50jrYtdgrH5CTFMTgqiisGVdnO5OMH?usp=sharing

