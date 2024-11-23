from lark import Lark, Transformer
import sys
import os

# Creditos
Creditos = """ \033[93m
#          ^~^  ,      
#         ('Y') )     \033[0;37m This code was generated using the Logo++ Interpreter \033[93m
#         /   \/      \033[0;37m by [Catto] Juan Diego Ruiz B && Juan Camilo Marin H. \033[93m
#        (\|||/)      \033[0;37m Under MIT License. \033[93m
\033[0m"""


# Mensaje de bienvenida
MensajeInterprete = """
    \033[37;1m Logo++ Interpreter \033[0m
"""

# Gato ASCII
Gato = """ \033[93m
#          ^~^  ,
#         ('Y') )
#         /   \/
#        (\|||/)
\033[0m"""

# Gramática
LogoPP = r"""
    start: instruction+

    ?instruction: basic
                | control
                | boolean
                | math    

    ?basic:       "FD" INTNUM -> fd
                | "BK" INTNUM -> bk
                | "LT" INTNUM -> lt
                | "RT" INTNUM -> rt
                | "PU"        -> pu
                | "PD"        -> pd
                | "WT" INTNUM -> wt

    ?math:        math "+" term -> add
                | math "-" term -> sub
                | term
    
    ?term:        term "*" factor -> mul
                | term "/" factor -> div
                | factor

    ?factor:      INTNUM
                | "-" factor -> neg
                | "(" math ")"

    ?boolean:     BOOL                  -> boolValue
                | boolean "AND" boolean -> andOperation
                | boolean "OR" boolean  -> orOperation
                | "NOT" boolean         -> notOperation

    BOOL: "TRUE" | "FALSE"
    INTNUM: /-?\d+(\.\d+)?([eE][+-]?\d+)?/x
    %ignore /[ \t\n\f\r]+/x
"""

# Arbol de gramatica
class CalcularArbol(Transformer):

    # Definicion de las instrucciones basicas
    def fd(self, INTNUM):
        return f"t.fd({INTNUM[0]})"
    def bk(self, INTNUM):
        return f"t.bk({INTNUM[0]})"
    def lt(self, INTNUM):
        return f"t.lt({INTNUM[0]})"
    def rt(self, INTNUM):
        return f"t.rt({INTNUM[0]})"
    def pu(self):
        return "t.pu()"
    def pd(self):
        return "t.pd()"

    # Definicion de las operaciones aritmeticas
    def add(self, args):
        return f"{args[0]} + {args[1]}"
    def sub(self, args):
        return f"{args[0]} - {args[1]}"
    def mul(self, args):
        return f"{args[0]} * {args[1]}"
    def div(self, args):
        return f"{args[0]} / {args[1]}"
    
    # Definicion de las operaciones Logicas/Booleanas
    def andOperation(self, args):
        return f"({args[0]} and {args[1]})"
    def orOperation(self, args):
        return f"({args[0]} or {args[1]})"
    def notOperation(self, args):
        return f"(not {args[0]})"
    def wt(self, INTNUM):
        return f"t.width({INTNUM[0]})"
    
    # Manejo de datos
    def INTNUM(self, value):        # Enteros
        return int(value)
    def bool_value(self, args):     # Booleanos
        return args[0] == "TRUE"
    
    # Manejo de opereaciones aritmeticas

# ignorar v

#                | loop
#                | function
#                | call

# ############################## Ejecución del programa ##############################
# Mostrar mensaje de bienvenida
os.system("cls" if os.name == "nt" else "clear")
print(MensajeInterprete)

# Crear parser con transformador
parser = Lark(LogoPP, parser="lalr")

# Función principal para procesar archivos
def convertir_archivo(input_file, output_file):
    try:
        # Leer el archivo de entrada
        with open(input_file, 'r') as infile:
            contenido = infile.read().strip()  # Limpia la entrada

        # Parsear el contenido
        arbol = parser.parse(contenido)

        # Aplicar el transformador para convertir el AST a instrucciones
        transformador = CalcularArbol()
        codigo_transformado = transformador.transform(arbol)

        # Guardar el resultado en un archivo .py
        with open(output_file, 'w') as outfile:
            # Escribir el código inicial para usar turtle
            outfile.write("import turtle\n")
            outfile.write("t = turtle.Turtle()\n\n")

            # Escribir las instrucciones transformadas
            for linea in codigo_transformado.children:
                outfile.write(linea + '\n')

            # Finalizar con el mainloop de turtle
            outfile.write("\nturtle.mainloop()\n")
            outfile.write("\n" + Creditos)

        print(f"Archivo convertido y guardado en: {output_file}")
    except Exception as e:
        print(f"Error al parsear el archivo: {e}")

# Leer los argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("Uso: python interprete.py archivo.lpp")
else:
    input_file = sys.argv[1]
    output_file = "Out" + input_file.replace('.lpp', '.py')

    # Convertir el archivo
    convertir_archivo(input_file, output_file)