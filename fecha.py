from datetime import datetime
date = datetime.now()
fecha_hoy = date.strftime('%Y%m%d')
url = f"https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20230923&fechaFinInclusiva={fecha_hoy}"
print(url)