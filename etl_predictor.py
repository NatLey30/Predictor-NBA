from bs4 import BeautifulSoup
import requests

def extract():
    r = requests.get('https://www.sportytrader.es/cuotas/baloncesto/usa/nba-306/')
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    # Pedimos el equipo del que queremos obtener datos
    nombre_equipo = input('¿De qué equipo te gustaría saber?\n')

    tag1 = 'cursor-pointer border rounded-md mb-4 px-1 py-2 flex flex-col lg:flex-row relative'
    partidos = soup.find_all('div', class_=tag1)

    continuar = True
    i = 0
    while continuar:
        tag2 = 'font-medium w-full lg:w-1/2 text-center dark:text-white'
        equipos = partidos[i].find('span', class_=tag2).text.strip()

        equiposs = equipos.split(' - ')

        equipo1 = equiposs[0]
        equipo2 = equiposs[1]

        if equipo1 == nombre_equipo:
            equipo_contrario = (equipo2)

            tag3 = 'text-sm text-gray-600 w-full lg:w-1/2 text-center dark:text-white'
            fecha = partidos[i].find('span', class_=tag3).text

            tag4 = 'px-1 h-booklogosm font-bold bg-primary-yellow text-white leading-8 '
            tag4 += 'rounded-r-md w-14 md:w-18 flex justify-center items-center text-base'
            cuotas = partidos[i].find_all('span', class_=tag4)
            cuota_e1 = cuotas[0].text
            cuota_e2 = cuotas[1].text

            if cuota_e1 > cuota_e2:
                equipo_g = equipo2
            else:
                equipo_g = equipo1

            mensaje = f'''
                    \nEQUIPO CONTRA EL QUE JUEGA\n{equipo_contrario}
                    \nDÍA Y HORA\n{fecha}
                    \nCUOTAS\n{equipo1} -> {cuota_e1}\n{equipo2} -> {cuota_e2}
                    \nTIENE MÁS PROBABILIDADES DE GANAR\n{equipo_g}
                    '''

            continuar = False

        elif equipo2 == nombre_equipo:
            equipo_contrario = equipo1

            tag3 = 'text-sm text-gray-600 w-full lg:w-1/2 text-center dark:text-white'
            fecha = partidos[i].find('span', class_=tag3).text

            tag4 = 'px-1 h-booklogosm font-bold bg-primary-yellow text-white leading-8 '
            tag4 += 'rounded-r-md w-14 md:w-18 flex justify-center items-center text-base'
            cuotas = partidos[i].find_all('span', class_=tag4)
            cuota_e1 = cuotas[0].text
            cuota_e2 = cuotas[1].text

            if cuota_e1 > cuota_e2:
                equipo_g = equipo2
            else:
                equipo_g = equipo1

            mensaje = f'''
                    \nEQUIPO CONTRA EL QUE JUEGA\n{equipo_contrario}
                    \nDÍA Y HORA\n{fecha}
                    \nCUOTAS\n{equipo1} -> {cuota_e1}\n{equipo2} -> {cuota_e2}
                    \nTIENE MÁS PROBABILIDADES DE GANAR\n{equipo_g}
                    '''

            continuar = False

        if i == len(partidos)-1 and continuar:
            mensaje = '\nNo se ha encontrado ningún partido para este equipo no deben de estar disponibles aún las apuestas para su próximo partido'

            continuar = False
        i += 1

    return mensaje

def load(mensaje):
    print(mensaje)


if '__main__' == __name__:

    soup = extract()
    mensaje = transform(soup)
    load(mensaje)
