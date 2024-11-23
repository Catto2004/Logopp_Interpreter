from lark import Lark, Transformer
import sys
import os

# Gramática corregida
LogoPP = r"""
    start: line+

    line: boolean
        | _NL

    ?boolean:     BOOL                  -> boolValue
                | boolean "AND" boolean -> andOperation
                | boolean "OR" boolean  -> orOperation
                | "NOT" boolean         -> notOperation

    BOOL: "TRUE" | "FALSE"
    _NL: /(\r?\n)+/
    %ignore _NL                          // Ignorar saltos de línea entre instrucciones
    %ignore /[ \t]+/                     // Ignorar espacios y tabulaciones
"""

# Transformador
class CalcularArbol(Transformer):
    def boolValue(self, args):
        return args[0] == "TRUE"  # Devuelve True o False según el valor

    def andOperation(self, args):
        return f"({args[0]} and {args[1]})"

    def orOperation(self, args):
        return f"({args[0]} or {args[1]})"

    def notOperation(self, args):
        return f"(not {args[0]})"

# Procesar líneas del archivo
def procesar_lineas(input_file):
    try:
        with open(input_file, 'r') as infile:
            lineas = infile.readlines()
            print("Contenido del archivo línea por línea:")
            for idx, linea in enumerate(lineas):
                print(f"{idx + 1}: {repr(linea.strip())}")
            return lineas
    except FileNotFoundError:
        print(f"Error: El archivo '{input_file}' no existe.")
        sys.exit(1)

# Parsear cada línea
def parsear_lineas(lineas):
    for idx, linea in enumerate(lineas):
        try:
            print(f"\nProcesando línea {idx + 1}: {repr(linea.strip())}")
            if linea.strip():  # Ignorar líneas vacías
                arbol = parser.parse(linea.strip())
                print(arbol.pretty())
        except Exception as e:
            print(f"Error en línea {idx + 1}: {e}")

# Main
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("\033[37;1m Logo++ Interpreter \033[0m")

    if len(sys.argv) != 2:
        print("Uso: python interprete.py archivo.lpp")
        sys.exit(1)
    
    input_file = sys.argv[1]
    lineas = procesar_lineas(input_file)

    # Crear parser y transformador
    parser = Lark(LogoPP, parser="lalr", transformer=CalcularArbol())
    parsear_lineas(lineas)
