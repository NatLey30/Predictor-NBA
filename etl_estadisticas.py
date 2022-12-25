import requests
from xhtml2pdf import pisa
import webbrowser


def convert_html_to_pdf(source_html, output_filename):
    # abrimos el fichero de salida
    result_file = open(output_filename, "w+b")

    # convertimos HTML a PDF
    pisa_status = pisa.CreatePDF(source_html, dest=result_file)

    # cerramos fichero
    result_file.close()

    # devolvemos True si ha habido exito and False si no
    return pisa_status.err


def extract(auth_key, endpoint):
    url = f"https://v2.nba.api-sports.io/{endpoint}"

    payload = {}
    headers = {
                'x-rapidapi-key': auth_key,
                'x-rapidapi-host': 'v1.basketball.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response['response']


def transform(auth_key):
    # Pedimos el equipo del que queremos obtener datos
    nombre_equipo = input('¿De qué equipo te gustaría obtener estadísticas?\n')
    continuar = True
    # Si ese equipo no existe, pedimos otro nombre
    while continuar:
        try:
            equipo = extract(auth_key, f'/teams?name={nombre_equipo}')
            continuar = False
        except:
            print('Por favor introduzca el nombre correcto')
            nombre_equipo = input('¿De qué eqipo te gustaría obtener estadísticas?\n')

    # Sacamos los datos que nos interesan del equipo
    id_eq = equipo[0]['id']
    nm_eq = equipo[0]['nickname']
    cd_eq = equipo[0]['code']
    lg_eq = equipo[0]['logo']
    datos_eq = ['2022', cd_eq, nm_eq, lg_eq]

    # Sacamos los jugadores de este equipo
    jugadores = extract(auth_key, f'/players/?team={id_eq}&season=2022')
    datos_jg = []
    for jg in jugadores:
        fn_jg = jg['firstname']
        ln_jg = jg['lastname']
        ct_jg = jg['birth']['country']
        st_jg = jg['nba']['start']
        pro_jg = jg['nba']['pro']
        datos_jg.append([fn_jg, ln_jg, ct_jg, st_jg, pro_jg])

    # Sacamos las estadísticas de este equipo
    jugadores_estadisticas = extract(auth_key, f'/players/statistics?team={id_eq}&season=2022')
    datos_jg_eq = []
    for jg_e in jugadores_estadisticas:
        gm_jg_e = jg_e['game']['id']
        fn_jg_e = jg_e['player']['firstname']
        ln_jg_e = jg_e['player']['lastname']
        min_jg_e = jg_e['min']
        pt_jg_e = jg_e['points']
        fgm_jg_e = jg_e['fgm']
        fga_jg_e = jg_e['fga']
        ftm_jg_e = jg_e['ftm']
        fta_jg_e = jg_e['fta']
        sl_jg_e = jg_e['steals']
        bk_jg_e = jg_e['blocks']
        datos_jg_eq.append([gm_jg_e, fn_jg_e + ' ' + ln_jg_e, min_jg_e,
                            pt_jg_e, fgm_jg_e, fga_jg_e, ftm_jg_e, fta_jg_e,
                            sl_jg_e, bk_jg_e])

    return datos_eq, datos_jg, datos_jg_eq

def load(datos_eq, datos_jg, datos_jg_eq):
    mensaje = f"""
    <html>
    <head><h1>Estádisticas NBA</h1></head>
    <p><h2>Temporada {datos_eq [0]}</h2></p>
    <p><h3>Equipo: {datos_eq[2]} ({datos_eq[1]})</h3></p>
    <p><img src={datos_eq[3]}
        width="100"
        height="100"></p>
    <p><h4>Jugadores del equipo:</h4></p>
    <table>
    <tr>
        <td>Firstname</td>
        <td>Lastname</td>
        <td>Country</td>
        <td>Start</td>
        <td>Pro</td>
    </tr>"""

    for jg in datos_jg:
        mensaje += f"""
        <tr>
            <td>{jg[0]}</td>
            <td>{jg[1]}</td>
            <td>{jg[2]}</td>
            <td>{jg[3]}</td>
            <td>{jg[4]}</td>
        </tr>
        """

    # partidos = []
    partido = ''
    for par in datos_jg_eq:
        if str(par[0]) != partido:
            partido = str(par[0])
            mensaje += f"""
            </table>
            <p><h5>Estadísticas en el partido: {partido}</h5></p>
            <table>
            <tr>
                <td>Player</td>
                <td>Min</td>
                <td>Points</td>
                <td>FGM</td>
                <td>FGA</td>
                <td>FTM</td>
                <td>FTA</td>
                <td>Steals</td>
                <td>Blocks</td>
            </tr>
            <tr>
                <td>{par[1]}</td>
                <td>{par[2]}</td>
                <td>{par[3]}</td>
                <td>{par[4]}</td>
                <td>{par[5]}</td>
                <td>{par[6]}</td>
                <td>{par[7]}</td>
                <td>{par[8]}</td>
                <td>{par[9]}</td>
            </tr>"""
        else:
            mensaje += f"""
            <tr>
                <td>{par[1]}</td>
                <td>{par[2]}</td>
                <td>{par[3]}</td>
                <td>{par[4]}</td>
                <td>{par[5]}</td>
                <td>{par[6]}</td>
                <td>{par[7]}</td>
                <td>{par[8]}</td>
                <td>{par[9]}</td>
            </tr>"""

    mensaje += """
    </table>
    </html>"""

    # Escribimos en el fichero HTML
    f = open('reporte.html', 'w')
    f.write(mensaje)
    f.close()

    webbrowser.open_new_tab('reporte.html')

    # Lo convertimos a PDF
    convert_html_to_pdf(mensaje, 'Estadisticas.pdf')


if "__main__" == __name__:

    auth_key = 'xxxxxxx'  # insert your api key from config.txt

    datos_eq, datos_jg, datos_jg_eq = transform(auth_key)
    load(datos_eq, datos_jg, datos_jg_eq)
