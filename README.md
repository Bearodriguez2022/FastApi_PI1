# FastApi_PI1

Proyecto Individual1 Henry

Este es Primer Trabajo Final de la carrera Data Science de la Academia Henry.

#  Objetivos:

*Realizar un EDA con 4 csv de Plataformas de streaming y 8 csv de Rating, en los cuales hay que realiza:

  1-Generar campo id: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = as123)
  
  2-Los valores nulos del campo rating deberán reemplazarse por el string “G” (corresponde al maturity rating: “general for all audiences”)
  
  3-De haber fechas, deberán tener el formato AAAA-mm-dd.
  
  4-Los campos de texto deberán estar en minúsculas, sin excepciones.
  
  5-El campo duration debe convertirse en dos campos: duration_int y duration_type. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas).Este paso lo realice en cada df por separado.

Adema realizo cambios que creo convenientes para que la data quede limpia y creo nuevo df llamado df1 con el cual hare las consultas en la Api.Esta tarea la realizo en colab ya que manejo csv muy extensos.
 
 * Desarrolo de una Api con FASTAPI
 
 Una vez que los datos estan listos para ser consultados utilizo visual studio code, alli hice la api de la siguiente manera:


Desde la consola de Visual:
git init
pip install uvicorn
pip install fastapi
pip install pandas

 Una vez que ya están todas las librerías descargadas en nuestro entorno virtual, podemos hacer el freeze de los requirements.
 
Es importante no abusar de demasiadas dependencias, porque en algunos casos, luego las aplicaciones no pueden deployar nuestros modelos.
pip freeze > requirements.txt
Si luego necesito instalar otra librería más, se vuelve a ejecutar este comando.
Cualquier persona que quiera usar nuestro código, va a poder instalar lo mismo que instalamos nosotros.

Las Consultas a realizar a la api son:
(primero cree las funciones en colab para probarlas y luego pasarlas a Fastapi)


1)Película (sólo película, no serie, etc) con mayor duración según año, plataforma y tipo de duración. La función debe llamarse get_max_duration(year, platform, duration_type) y debe devolver sólo el string del nombre de la película.

2)Cantidad de películas (sólo películas, no series, etc) según plataforma, con un puntaje mayor a XX en determinado año. La función debe llamarse get_score_count(platform, scored, year) y debe devolver un int, con el total de películas que cumplen lo solicitado.

3)Cantidad de películas (sólo películas, no series, etc) según plataforma. La función debe llamarse get_count_platform(platform) y debe devolver un int, con el número total de películas de esa plataforma. Las plataformas deben llamarse amazon, netflix, hulu, disney.

4)Actor que más se repite según plataforma y año. La función debe llamarse get_actor(platform, year) y debe devolver sólo el string con el nombre del actor que más se repite según la plataforma y el año dado.

5)La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año. La función debe llamarse prod_per_county(tipo,pais,anio) deberia devolver la cantidada de contenidos/productos segun el tipo de contenido (pelicula,serie) por pais y año en un diccionario con las variables llamadas 'pais' (nombre del pais), 'anio' (año), 'pelicula' (cantidad de contenidos/productos).

6)La cantidad total de contenidos/productos (todo lo disponible en streaming, series, peliculas, etc) según el rating de audiencia dado (para que publico fue clasificada la pelicula). La función debe llamarse get_contents(rating) y debe devolver el numero total de contenido con ese rating de audiencias.


Por útlimo realizo el ETL y modelo de recomedación de peliculas, mi criterio para elegir fue implementar Modelo de vecinos Cercanos.

1-Realice analisis con librerias recomendas.

2-Normalización de datos.

3-Entrenamiento.

4-Realiación Modelo.

5-Calculo de efectividad.

6- realizción de Modelo para ser consumido por Api.


video explictivo https://reccloud.com/es/u/urs30wm
render  https://fastapi-pi1.onrender.com 
