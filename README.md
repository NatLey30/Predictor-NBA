# Predictor-NBA

Este programa ofrece un analizador de las principales estadísticas de un equipo en cada partido hasta el momento para la temporada 2022-2023 y un pronóstico para el próximo partido.

Para ello debes se dispone de dos ETLs. La primera ETL extrae, transforma los datos y guarda un informe de los puntos clave del equipo sacado de una API en formato pdf. La segunda ofrece por pantalla la predicción del equipo para el próximo partido obteniendo y transformando los datos mediante técnicas de webscrapping.

Mediante la primera ETL se ofrece un pdf con las estadísticas en formato de tabla de cada uno de los jugadores de equipo en cuestión en todos los partidos jugados, cada partido es una tabla.

Una vez extraidos los datos de la segunda ETL, para deducir el ganador de el proximo del equipo, nos fijamos en las cuotas. La cuota más baja significa que tiene más probabilidad de ganar.

Web API: https://api-sports.io/documentation/nba/v2

Web pronóstico: https://www.sportytrader.es/cuotas/baloncesto/usa/nba-306/

Los ficheros de entrada son:
- requirements.txt
- config.txt

Los ficheros de salida son:
- reporte.html
- Estadísticas.pdf

Los archivos de transformación:
- etl_estadisticas.py
- etl_predictor.py

Librerías:
- requests
- xhtml2pdf
- webbrowser
- bs4
