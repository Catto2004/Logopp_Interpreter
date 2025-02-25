# Logo++ Interpreter

El presente proyecto constituye un intérprete diseñado para el lenguaje **Logo++**, el cual permite la ejecución de instrucciones fundamentales, estructuras de control, bucles y funciones, generando como resultado programas compatibles con **Python** y **Turtle Graphics**.

---

## Características principales

Este intérprete ofrece las siguientes funcionalidades:

1. **Instrucciones básicas:** Permite controlar el movimiento, el giro y la posición de la pluma, así como manipular su grosor.
2. **Azúcar sintáctica:** Soporte para incremento y decremento de variables mediante operadores simplificados.
3. **Operaciones matemáticas y booleanas:** Procesamiento de expresiones aritméticas y lógicas.
4. **Definición y llamado de funciones:** Implementación modular del código mediante funciones personalizadas.
5. **Estructuras de control:** Compatibilidad con sentencias condicionales (`IF`) y bucles (`FOR`).
6. **Visualización del Árbol Sintáctico:** Generación de representaciones gráficas en formatos `.png` y `.dot`, útiles para depuración y análisis del flujo del programa.

---

## Requisitos del sistema

Para ejecutar este intérprete, es necesario contar con:

1. **Python** en su **versión 3.8 o superior**.
2. Las siguientes bibliotecas, que pueden instalarse mediante `pip`:
```bash
   pip install lark-parser pydot
```
Opcionalmente, para la visualización de árboles `.dot`, se requiere instalar Graphviz:
En sistemas Debian/Ubuntu:
```bash
   sudo apt-get install graphviz
```
En sistemas Windows:
```bash
   winget install graphviz
```

---

## Instalación
Para instalar y ejecutar el proyecto, siga las siguientes instrucciones:
### Clonar el repositorio en su máquina local:
```bash
   git clone https://github.com/Catto2004/Logopp_Interpreter
   cd <carpeta-del-repositorio>
```
### Instalar las dependencias necesarias:
```bash
   pip install -r requirements.txt
```
Ejecutar el intérprete, proporcionando un archivo de entrada con extensión `.lpp`:
```bash
   python interprete.py archivo.lpp
```

---

## Uso del intérprete
El intérprete procesa un archivo `.lpp` como entrada y genera un archivo Python ejecutable con instrucciones Turtle.
Ejemplo de entrada `archivo.lpp`:
```logo++
DEF miFuncion(x) {
    FD x
    RT 90
}
miFuncion(50)

FOR i IN RANGE(0, 4) {
    LT 90
    FD 100
}
```

---

## Conjunto de instrucciones soportadas:
### Instrucciones básicas:

FD <valor>: Avanza la pluma.
BK <valor>: Retrocede la pluma.
LT <valor>: Gira a la izquierda.
RT <valor>: Gira a la derecha.
PU: Levanta la pluma.
PD: Baja la pluma.
WT <valor>: Modifica el grosor de la pluma.
Control de flujo:

IF <condición> { ... }
ELSE { ... }
ELIF <condición> { ... }
FOR <variable> IN RANGE(<inicio>, <fin>, <paso>) { ... }

### Definición y llamado de funciones:
```logo++
DEF miFuncion(x) {
    FD x
    RT 90
}
miFuncion(50)
```

---

## Salida generada:
El intérprete produce un archivo Python con el prefijo Out y el nombre del archivo de entrada, el cual puede ejecutarse directamente para visualizar el resultado en Turtle Graphics.

---

## Configuración:
Es posible personalizar el comportamiento del intérprete mediante la clase `Config`:
```Python
class Config:
    SinArboles = False  # Desactiva la visualización del árbol sintáctico.
    Arboldot = True      # Genera un archivo .dot del árbol.
    Arbolpng = True      # Genera una imagen .png del árbol.
    Arbolcmd = False     # Muestra el árbol en la consola.
```

---

## Resolución de problemas:
### Error al cargar la gramática:

Verifique que la gramática esté correctamente definida y que su versión de **Python sea 3.8 o superior**.
Archivo de entrada no encontrado:

Asegúrese de que el archivo `.lpp` exista y su ruta sea correcta.
### Falta de visualización del árbol sintáctico:

Verifique que las bibliotecas pydot y graphviz estén instaladas y configuradas correctamente.

---

## Créditos
Este proyecto ha sido desarrollado por:

   - Juan Diego R.B.
   - Juan Camilo Marín H.
   - Luisa López

Agradecimientos especiales a *Mochi*. 

El proyecto se encuentra bajo la **Licencia MIT**.

---

## Licencia
Este software está licenciado bajo la Licencia MIT, lo que permite su uso, distribución y modificación de forma libre, siempre y cuando se reconozca la autoría original.
