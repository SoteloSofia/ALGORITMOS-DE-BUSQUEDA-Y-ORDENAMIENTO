# Trabajo Integrador Programación I
#Eje Temático elegido: Busqueda y Ordenamiento de algoritmos. 
 
import time
import random

# --- Datos de Ejemplo del Catálogo ---
# Representamos cada producto como un diccionario
# y el catálogo como una lista de diccionarios.
catalogo_productos = [
    {"id": 105, "nombre": "Teclado Mecánico", "categoria": "Accesorios", "precio": 100.00, "stock": 15},
    {"id": 101, "nombre": "Laptop Ultrabook", "categoria": "Electrónica", "precio": 1200.00, "stock": 5},
    {"id": 103, "nombre": "Mouse Inalámbrico", "categoria": "Accesorios", "precio": 25.00, "stock": 50},
    {"id": 102, "nombre": "Monitor Curvo 27", "categoria": "Electrónica", "precio": 350.00, "stock": 10},
    {"id": 104, "nombre": "Webcam HD", "categoria": "Periféricos", "precio": 40.00, "stock": 30},
    {"id": 106, "nombre": "Auriculares Bluetooth", "categoria": "Accesorios", "precio": 75.00, "stock": 20},
    {"id": 107, "nombre": "Disco Duro Externo", "categoria": "Almacenamiento", "precio": 110.00, "stock": 8},
    {"id": 108, "nombre": "Impresora Multifunción", "categoria": "Periféricos", "precio": 200.00, "stock": 12},
    {"id": 109, "nombre": "Tableta Gráfica", "categoria": "Electrónica", "precio": 150.00, "stock": 7},
    {"id": 110, "nombre": "Smartphone Gama Alta", "categoria": "Telefonía", "precio": 800.00, "stock": 3}
]

# --- Funciones Auxiliares ---

def print_catalogo(productos, titulo="Catálogo de Productos"):
    """Imprime el catálogo de productos de forma legible."""
    print(f"\n--- {titulo} ({len(productos)} productos) ---")
    if not productos:
        print("El catálogo está vacío.")
        return

    # Imprimir encabezados
    print(f"{'ID':<5} | {'Nombre':<25} | {'Categoría':<15} | {'Precio':<10} | {'Stock':<5}")
    print("-" * 65)
    # Imprimir cada producto
    for p in productos:
        print(f"{p['id']:<5} | {p['nombre']:<25} | {p['categoria']:<15} | ${p['precio']:<9.2f} | {p['stock']:<5}")
    print("-" * 65)

def generar_datos_aleatorios(cantidad):
    """Genera una lista de productos aleatorios para pruebas de rendimiento."""
    nombres = ["Laptop", "Teclado", "Mouse", "Monitor", "Webcam", "Auriculares", "Disco Duro", "Impresora", "Tableta", "Smartphone", "Cámara", "Altavoz"]
    categorias = ["Electrónica", "Accesorios", "Periféricos", "Almacenamiento", "Telefonía"]
    productos_generados = []
    for i in range(cantidad):
        productos_generados.append({
            "id": i + 200, # IDs que no choquen con los de ejemplo
            "nombre": f"{random.choice(nombres)} {i+1}",
            "categoria": random.choice(categorias),
            "precio": round(random.uniform(90.000, 1.500), 2),
            "stock": random.randint(1, 100)
        })
    return productos_generados

def medir_tiempo(func):
    """Decorador para medir el tiempo de ejecución de una función."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Tiempo de ejecución de '{func.__name__}': {end_time - start_time:.6f} segundos.")
        return result
    return wrapper

# --- Algoritmos de Búsqueda ---

@medir_tiempo
def busqueda_lineal_por_nombre(catalogo, nombre_buscado):
    """
    Realiza una búsqueda lineal para encontrar productos por nombre.
    Retorna una lista de productos que coinciden con el nombre (parcial o completo).
    """
    resultados = []
    print(f"\n--- Búsqueda Lineal: Buscando '{nombre_buscado}' ---")
    for producto in catalogo:
        # Usamos .lower() para hacer la búsqueda insensible a mayúsculas/minúsculas
        if nombre_buscado.lower() in producto["nombre"].lower():
            resultados.append(producto)
    return resultados

@medir_tiempo
def busqueda_binaria_por_id(catalogo_ordenado, id_buscado):
    """
    Realiza una búsqueda binaria para encontrar un producto por ID.
    El catálogo DEBE estar ordenado por 'id' antes de llamar a esta función.
    Retorna el producto si lo encuentra, None en caso contrario.
    """
    print(f"\n--- Búsqueda Binaria: Buscando ID '{id_buscado}' ---")
    bajo = 0
    alto = len(catalogo_ordenado) - 1

    while bajo <= alto:
        medio = (bajo + alto) // 2
        producto_medio = catalogo_ordenado[medio]

        if producto_medio["id"] == id_buscado:
            return producto_medio
        elif producto_medio["id"] < id_buscado:
            bajo = medio + 1
        else:
            alto = medio - 1
    return None

# --- Algoritmos de Ordenamiento ---

def _merge(izquierda, derecha, clave_ordenamiento):
    """
    Función auxiliar para Merge Sort: mezcla dos sublistas ordenadas.
    """
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i][clave_ordenamiento] < derecha[j][clave_ordenamiento]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    
    # Añadir los elementos restantes (si los hay)
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

# Función recursiva auxiliar para Merge Sort (sin decorador para evitar problemas de recursión)
def _recursive_merge_sort(lista, clave_ordenamiento):
    n = len(lista)
    if n <= 1:
        return lista

    medio = n // 2
    izquierda = lista[:medio]
    derecha = lista[medio:]

    izquierda_ordenada = _recursive_merge_sort(izquierda, clave_ordenamiento)
    derecha_ordenada = _recursive_merge_sort(derecha, clave_ordenamiento)

    return _merge(izquierda_ordenada, derecha_ordenada, clave_ordenamiento)

@medir_tiempo
def merge_sort_por_precio(catalogo):
    """
    Ordena una lista de productos por precio usando el algoritmo Merge Sort.
    Crea una copia para no modificar la lista original.
    """
    lista = catalogo[:] # Crear una copia para no modificar la original
    print(f"\n--- Ordenando por Precio (Merge Sort) ---")
    
    # Llama a la función recursiva auxiliar para realizar el ordenamiento
    return _recursive_merge_sort(lista, "precio")


# --- Bloque Principal de Ejecución ---
if __name__ == "__main__":
    print_catalogo(catalogo_productos, "Catálogo Inicial")

    # --- 1. Demostración de Búsqueda Lineal ---
    print("\n\n--- DEMOSTRACIÓN DE BÚSQUEDA LINEAL ---")
    nombre_a_buscar = "Monitor"
    resultados_lineal = busqueda_lineal_por_nombre(catalogo_productos, nombre_a_buscar)
    if resultados_lineal:
        print_catalogo(resultados_lineal, f"Resultados para '{nombre_a_buscar}'")
    else:
        print(f"No se encontraron productos con el nombre '{nombre_a_buscar}'.")


    # --- 2. Demostración de Ordenamiento con Merge Sort ---
    print("\n\n--- DEMOSTRACIÓN DE ORDENAMIENTO (MERGE SORT) ---")
    catalogo_ordenado_por_precio = merge_sort_por_precio(catalogo_productos)
    print_catalogo(catalogo_ordenado_por_precio, "Catálogo Ordenado por Precio (Merge Sort)")

    # --- 3. Demostración de Búsqueda Binaria (Requiere lista ordenada por ID) ---
    print("\n\n--- DEMOSTRACIÓN DE BÚSQUEDA BINARIA ---")
    # Primero, ordenamos el catálogo por ID para que la búsqueda binaria funcione.
    catalogo_ordenado_para_binaria = sorted(catalogo_productos, key=lambda p: p["id"])
    print_catalogo(catalogo_ordenado_para_binaria, "Catálogo Ordenado por ID (Para Búsqueda Binaria)")

    id_a_buscar = 104
    producto_encontrado_binaria = busqueda_binaria_por_id(catalogo_ordenado_para_binaria, id_a_buscar)
    if producto_encontrado_binaria:
        print(f"Producto encontrado por Búsqueda Binaria para ID {id_a_buscar}: {producto_encontrado_binaria['nombre']}")
    else:
        print(f"No se encontró el producto con ID {id_a_buscar}.")

    # --- 4. Demostración de Rendimiento con Grandes Cantidades de Datos ---
    print("\n\n--- DEMOSTRACIÓN DE RENDIMIENTO CON GRANDES DATOS ---")
    cantidad_productos_grandes = 5000 # Puedes cambiar esto a 10000, 50000, etc.
    catalogo_grande = generar_datos_aleatorios(cantidad_productos_grandes)

    # Medir Merge Sort (mucho más rápido)
    print(f"\nProbando Merge Sort con una lista de {cantidad_productos_grandes} productos...")
    catalogo_grande_merge = merge_sort_por_precio(catalogo_grande)

    # Medir Búsqueda Lineal en lista grande
    print(f"\nProbando Búsqueda Lineal con una lista de {cantidad_productos_grandes} productos...")
    busqueda_lineal_por_nombre(catalogo_grande, "Producto inexistente") # Buscando un nombre que no exista

    # Para Búsqueda Binaria, necesitamos que la lista grande esté ordenada por ID
    print(f"\nPreparando lista grande para Búsqueda Binaria ({cantidad_productos_grandes} productos)...")
    catalogo_grande_ordenado_id = sorted(catalogo_grande, key=lambda p: p["id"])
    
    # Buscando un ID que debería existir
    id_existente = random.randint(200, 200 + cantidad_productos_grandes - 1) 
    print(f"\nProbando Búsqueda Binaria con ID existente ({id_existente})...")
    busqueda_binaria_por_id(catalogo_grande_ordenado_id, id_existente) 
    
    # Buscando un ID que no existe
    print("\nProbando Búsqueda Binaria con ID inexistente (9999999)...")
    busqueda_binaria_por_id(catalogo_grande_ordenado_id, 9999999) 