# ===================== EJERCICIO 1 =====================
# Quitar duplicados conservando el orden
ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
vistas = set()
unicas = []

for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print("Ejercicio 1:", unicas)


# ===================== EJERCICIO 2 =====================
# Contar con un diccionario
conteo = {}

for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1

print("Ejercicio 2:", conteo)

mas_repetida = max(conteo, key=conteo.get)
print("Ciudad más repetida:", mas_repetida)


# ===================== EJERCICIO 3 =====================
# Conjuntos en acción
inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

ambas = inscritos_matematica & inscritos_ingles
solo_mate = inscritos_matematica - inscritos_ingles
total = len(inscritos_matematica | inscritos_ingles)

print("Ejercicio 3:")
print("En ambas materias:", sorted(ambas))
print("Solo en matemática:", sorted(solo_mate))
print("Total de estudiantes distintos:", total)


# ===================== EJERCICIO 4 =====================
# De lista de diccionarios a índice
clientes = [
    {"id": 1, "nombre": "Ana"},
    {"id": 2, "nombre": "Luis"}
]

indice = {
    cliente["id"]: cliente
    for cliente in clientes
}

print("Ejercicio 4:", indice[2]["nombre"])


# ===================== EJERCICIO 5 =====================
# Tuplas como registros inmutables
ventas = [
    ("enero", 1500),
    ("febrero", 1800),
    ("marzo", 1200)
]

total = sum(monto for _mes, monto in ventas)

mejor_mes, mejor_monto = max(
    ventas,
    key=lambda venta: venta[1]
)

print("Ejercicio 5:")
print(f"Total: {total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")

for mes, monto in ventas:
    print(f"{mes:<10} {monto}")