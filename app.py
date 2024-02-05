from flask import Flask, render_template, jsonify
import requests
import time
from datetime import datetime
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def add_header(response):
    # Disable caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    return render_template('mapa.html')
@app.route('/get_path')
def get_path():
    data = obtener_rutas()
    return jsonify(data)

@app.route('/get_data')
def get_data():
    data = obtener_datos_desde_python()
    return jsonify(data)

def obtener_datos_desde_python():
    # URL de la página que contiene los datos en tiempo real
    url = 'https://dadesobertes.fgc.cat/api/records/1.0/search/?dataset=posicionament-dels-trens&q=&rows=10000&timezone=Europe%2FMadrid'

    # Intervalo de tiempo entre cada extracción de datos (en segundos)
    intervalo = 60

    while True:
        try:
            # Descarga los datos de la URL
            response = requests.get(url)
            
            # Convierte los datos a formato JSON
            data = response.json()
            data_trains=[]
            # Extrae los datos relevantes
            for obj in data['records']:
                # if 'lin' in obj['fields']:
                #     print("Linea: "+obj['fields']['lin'])
                # else:
                #     print("Linea: NULL")
                # if 'geo_point_2d' in obj['fields']:
                #     print("Geoposicionamiento: ("+str(obj['fields']['geo_point_2d'][0])+", "+str(obj['fields']['geo_point_2d'][1])+")")
                # else:
                #     print("Geoposicionamiento: NULL")
                # if 'ocupacio_m1_percent' in obj['fields']:
                #         print("Ocupación: "+obj['fields']['ocupacio_m1_percent'])
                # else:
                #     print("Ocupación: NULL")
                # if 'origen' in obj['fields']:
                #         print("Origen: "+obj['fields']['origen'])
                # else:
                #     print("Ocupación: NULL")
                # if 'desti' in obj['fields']:
                #         print("Destino: "+obj['fields']['desti'])
                # else:
                #     print("Ocupación: NULL")
                # print("____________________________________________________")
            
                data_trains.append({'linea': obj['fields']['lin'], 'geo_posicion': [obj['fields']['geo_point_2d'][0], obj['fields']['geo_point_2d'][1]],'origen': obj['fields']['origen'],'destino': obj['fields']['desti']})
            print("")
            return data_trains

        except Exception as e:
            print('Error: ' + str(e))

def obtener_rutas():
       # URL de la página que contiene los datos en tiempo real
    url = 'https://dadesobertes.fgc.cat/api/records/1.0/search/?dataset=gtfs_routes&timezone=Europe%2FMadrid'
    try:
        # Descarga los datos de la URL
        response = requests.get(url)
        
        # Convierte los datos a formato JSON
        data = response.json()
        data_routes=[]
        # Extrae los datos relevantes
        for obj in data['records']:
            
            # Invierte las coordenadas en cada punto
            inverted_coordinates = [[[coord[1], coord[0]] for coord in line] for line in obj['fields']['shape']['coordinates']]

            data_routes.append({'linea': obj['fields']['route_short_name'], 'shape': inverted_coordinates[0]})
            print(inverted_coordinates)
            print("_________________________________")

        return data_routes

    except Exception as e:
        print('Error: ' + str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
