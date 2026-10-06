from models import Estudiante
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email","carnet")
CAMPOS_OBLIGATORIOS =("nombre","apellido","email","carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


# ===================== AYUDAS INTERNAS =====================

def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1

# ===================== C · CREATE =====================

def crear_estudiante(datos):
    
    try:
        
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

    
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        carnets = {
            registro["carnet"].lower()
            for registro in gestor.leer()
        }

        
        if valores["carnet"].lower() in carnets:
            return False, "Ese carnet ya está registrado"

        estudiante = Estudiante(
            siguiente_id(),
            valores["nombre"],
            valores["apellido"],
            valores["email"],
            valores["carnet"]
        )

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())

        if gestor.guardar(registros):
            return True, "Estudiante guardado correctamente"

        return False, "No se pudo guardar el estudiante"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """LISTA de objetos Estudiante."""
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):

    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []

    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:                 
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break                                  
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    
    try:
        
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "email" in cambios:
            cambios["email"] = cambios["email"].strip()

            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"

        if "carnet" in cambios:
            cambios["carnet"] = cambios["carnet"].strip()
            registros = gestor.leer()

            carnets_otros = {
                registro["carnet"].lower()
                for registro in registros
                if registro["id"] != id_estudiante
            }

            if cambios["carnet"].lower() in carnets_otros:
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()
        posicion = None

        for indice, registro in enumerate(registros):   
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros[posicion].update(cambios)     

        gestor.guardar(registros)

        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    
    quedan = [registro for registro in registros if registro["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    if gestor.guardar(quedan):
        return True, f"Estudiante {id_estudiante} eliminado"

    return False, "No se pudo eliminar el estudiante"

# ===================== NOTAS =====================

def agregar_nota(id_estudiante,materia,nota):
    try:
        materia = materia.strip()

        if not materia:
            return False, "La materia no puede estar vacia"

        try:
            nota = float(nota)
        except ValueError:
            return False, "La nota debe ser un numero"

        if nota < 0 or nota > 20:
            return False, "La nota debe estar entre 0 y 20"

        registros = gestor.leer()
        posicion = None

        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con ese id {id_estudiante}"

        registros[posicion].setdefault("notas",{})
        registros[posicion].setdefault("materias",[])

        registros[posicion]["notas"].setdefault(materia,[]).append(nota)

        if materia not in registros[posicion]["materias"]:
            registros[posicion]["materias"].append(materia)

        if gestor.guardar(registros):
            return True, f"Nota agregada en {materia}"

        return False, "No se pudo guardar la nota"
    
    except Exception as error:
        return False, f"Error inesperado: {error}"
    

#===================== MATERIAS =====================

def materias_ofertadas():
    materias = set()

    for registro in gestor.leer():
        materias.update(registro.get("materias",[]))
    return materias

def estudiantes_en_comun(id_a,id_b):
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if estudiante_a is None:
        return False, f"No existe un estudiante con id {id_a}"

    if estudiante_b is None:
        return False, f"No existe un estudiante con id {id_b}"

    materias_comunes = estudiante_a.materias & estudiante_b.materias

    return True, materias_comunes