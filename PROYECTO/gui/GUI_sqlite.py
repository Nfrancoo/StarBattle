import json
import sqlite3
import os

# Verificar si el archivo niveluno.json existe
if os.path.exists('datos_partida_NivelUno.json'):
    with open('datos_partida_NivelUno.json') as json_file:
        data = json.load(json_file)

    conn = sqlite3.connect('basedatos_juego.db')
    cursor = conn.cursor()

    # Verificar si la tabla existe, si no, crearla
    cursor.execute('''CREATE TABLE IF NOT EXISTS tabla_puntuaciones_niveluno (
                        duracion INTEGER,
                        puntos_jugador INTEGER,
                        puntos_enemigo INTEGER
                        )''')

    # Insertar los datos en la tabla correspondiente
    cursor.execute('INSERT INTO tabla_puntuaciones_niveluno VALUES (?, ?, ?)', (data['duracion'], data['puntos_jugador'], data['puntos_enemigo']))

    conn.commit()
    conn.close()

# Verificar si el archivo niveldos.json existe
if os.path.exists('datos_partida_NivelDos.json'):
    with open('datos_partida_NivelDos.json') as json_file:
        data = json.load(json_file)

    conn = sqlite3.connect('basedatos_juego.db')
    cursor = conn.cursor()

    # Verificar si la tabla existe, si no, crearla
    cursor.execute('''CREATE TABLE IF NOT EXISTS tabla_puntuaciones_niveldos (
                        duracion INTEGER,
                        puntos_jugador INTEGER,
                        puntos_enemigo INTEGER
                        )''')

    # Insertar los datos en la tabla correspondiente
    cursor.execute('INSERT INTO tabla_puntuaciones_niveldos VALUES (?, ?, ?)', (data['duracion'], data['puntos_jugador'], data['puntos_enemigo']))

    conn.commit()
    conn.close()

# Verificar si el archivo niveltres.json existe
if os.path.exists('datos_partida_NivelTres.json'):
    with open('datos_partida_NivelTres.json') as json_file:
        data = json.load(json_file)

    conn = sqlite3.connect('basedatos_juego.db')
    cursor = conn.cursor()

    # Verificar si la tabla existe, si no, crearla
    cursor.execute('''CREATE TABLE IF NOT EXISTS tabla_puntuaciones_niveltres (
                        duracion INTEGER,
                        puntos_jugador INTEGER,
                        puntos_enemigo INTEGER
                        )''')

    # Insertar los datos en la tabla correspondiente
    cursor.execute('INSERT INTO tabla_puntuaciones_niveltres VALUES (?, ?, ?)', (data['duracion'], data['puntos_jugador'], data['puntos_enemigo']))

    conn.commit()
    conn.close()

# Verificar si el archivo nivelcuatro.json existe
if os.path.exists('datos_partida_NivelCuatro.json'):
    with open('datos_partida_NivelCuatro.json') as json_file:
        data = json.load(json_file)

    conn = sqlite3.connect('basedatos_juego.db')
    cursor = conn.cursor()

    # Verificar si la tabla existe, si no, crearla
    cursor.execute('''CREATE TABLE IF NOT EXISTS tabla_puntuaciones_nivelcuatro (
                        duracion INTEGER,
                        puntos_jugador INTEGER,
                        puntos_enemigo INTEGER
                        )''')

    # Insertar los datos en la tabla correspondiente
    cursor.execute('INSERT INTO tabla_puntuaciones_nivelcuatro VALUES (?, ?, ?)', (data['duracion'], data['puntos_jugador'], data['puntos_enemigo']))

    conn.commit()
    conn.close()
