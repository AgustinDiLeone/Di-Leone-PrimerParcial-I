import datetime
import json
import re


def parser_csv(path:str)->list:
    '''
    Breif:
        Crea una lista con los personajes y sus caracteristicas con el archivo ingresado.
    Parameters:
        path:str -> El path del archivo.
    Return:
        list-> Una lista con diccionarios que contiene la informacion del archivo.
        -1 -> Hubo un error
    '''
    if type(path) == str and len(path)>0:
        lista_personajes = []
        with open(path, "r", encoding="utf-8") as archivo:
            for line in archivo:
                registro = re.split(",|\n", line)
                personaje = {
                    "id": int(registro[0]),
                    "nombre": (registro[1]).lower(),
                    "raza": registro[2].lower(),
                    "poder_pelea": int(registro[3]),
                    "poder_ataque": int(registro[4]),
                    "habilidades": registro[5].lower()
                }
                lista_personajes.append(personaje)
        return lista_personajes

def escribir_archivo_txt(path:str, lista:list):
    mi_archivo = open(path, "a", encoding="utf-8")
    for line in lista:
        mi_archivo.write(line)
    mi_archivo.close()

def guardar_batalla_archivo(ganador_perdedor):
    '''
    Brief: Guarda la batalla en un archivo de texto
    Parameters: 
        ganador_perdedor:list -> Lista que diga ganador y perdedor
    Return: 
        -1 -> Error
    '''
    if type(ganador_perdedor) == list and len(ganador_perdedor)>1:
        fecha_actual = str(datetime.date.today())
        lista = [
            f'\n{fecha_actual}\n',
            f'El ganador es: {ganador_perdedor[0]["nombre"]}\n',
            f'El perdedor es: {ganador_perdedor[1]["nombre"]}'
        ]
        escribir_archivo_txt("batallas.txt",lista)
    else:
        return -1

def escribir_json(nomenclatura:str, lista:list):
    with open(f"{nomenclatura}", "w", encoding="utf-8") as mi_archivo:
        json.dump(lista, mi_archivo, indent=4)

def guardar_json(raza:str, habilidad:str, lista_coincidencias)->str:
    '''
    Brief:
        Guarda una lista en un archivo .json
    Parameters:
        lista:list -> lista de personajes
        raza: str -> tipo de raza elegida por el usuario
        atributo:str -> tipo de habilidad elegida por el usuario
    return:
        nomenclatura : str -> El nombre del archivo
        3 : int -> Se ingreso mal un dato
    '''
    if type(raza) == str and type(habilidad) == str and type(lista_coincidencias) == list:
        nomenclatura = f"{raza} {habilidad}.json"
        nomenclatura = nomenclatura.replace(" ", "_")
        lista = definir_que_agregar_json(lista_coincidencias, habilidad)
        escribir_json(nomenclatura,lista)
        return nomenclatura
    else:
        return 3

def definir_que_agregar_json(lista_coincidencias:list, habilidad:str):
    '''
    Brief:
        Define que se va a guardar en el archivo .json
    Parameters:
        lista_coincidencias:list -> lista de personajes que coinciden con ambos atributos ingresados
        habilidad: str -> La habilidad elegida por el usuario
    return:
        lista:list -> Una lista de str con el formato del personaje para guardar en .json
        -1: int -> Error en los datos ingresados
    '''
    if type(habilidad) == str and type(lista_coincidencias) == list:
        lista = []
        for personaje in lista_coincidencias:
            habilidades = []
            for caracteristica in personaje['habilidades']:
                if caracteristica != habilidad:
                    habilidades.append(caracteristica)
            personaje_ = {
                "nombre" : personaje ["nombre"], 
                "poder_pelea" : personaje ["poder_pelea"],
                "habilidades": habilidades
                }
            lista.append(personaje_)
        return lista
    else: 
        return -1    

def leer_json(nombre_archivo:str)->list:
    '''
    Brief:
        Lee el archivo .json
    Parameters:
        nombre_archivo:str -> nombre del archivo .json
    return:
        data:list ->El archivo en forma de lista
    '''
    with open(nombre_archivo, "r") as mi_archivo:
        data = json.load(mi_archivo)
        return data

