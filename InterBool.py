from lark import Lark, Transformer
import sys
import os


# To-Do:
# Aún no implementado:
#           ...  | bool
#                | control
#                | loop
#            x   | function, Demasiado complicado, preguntar???
#            x   | call, Demasiado complicado


# ############################## Mensajes ##############################
# Creditos
Creditos = """
#          ^~^  ,      This code was generated using the Logo++ Interpreter
#         ('Y') )      by [Catto] Juan Diego Ruiz B, Juan Camilo Marin H. && Luisa Lopez.
#         /   \/       special thanks to: DMG.
#        (\|||/)       >> This code is under MIT License. <<
"""
# Mensaje de bienvenida
MensajeInterprete = """
           \033[37;1m Logo++ Interpreter \033[0m
"""
# Gato para mensaje
Gato = """0======v================================0
       \ \033[93m  ^~^  ,
          ('Y') )
          /   \/
         (\|||/)
\033[0m"""


# ############################## Gramatica ##############################
LogoPP = r"""
    start: instruction+

    ?instruction: basic
                | VARIABLE "=" math -> assign
                | bool
                | sugar

    ?bool:        bool "/\\" bool -> andOper
                | bool "\\/" bool -> orOper
                | "!" bool       -> notOper
                | "(" bool ")"
                | atom

    ?atom:        "TRUE" -> true
                | "FALSE" -> false

    ?basic:       "FD" math -> fd
                | "BK" math -> bk
                | "LT" math -> lt
                | "RT" math -> rt
                | "PU"      -> pu
                | "PD"      -> pd
                | "WT" math -> wt

    ?sugar:       VARIABLE "++" -> increment
                | VARIABLE "--" -> decrement
                | VARIABLE "+=" math -> add_assign
                | VARIABLE "-=" math -> sub_assign

    ?math:        math "+" term -> add
                | math "-" term -> sub
                | term
    
    ?term:        term "*" factor -> mul
                | term "/" factor -> div
                | factor

    ?factor:      INTNUM
                | VARIABLE -> var
                | "-" factor -> neg
                | "(" math ")"

    %ignore /#[^\n]*/
    %ignore /\n/
    VARIABLE: /[a-zA-Z_][a-zA-Z0-9_]*/
    INTNUM: /-?\d+(\.\d+)?([eE][+-]?\d+)?/x
    %ignore /[ \t\n\f\r]+/x
"""


# ############################## Árbol de Gramatica ##############################
class CalcularArbol(Transformer):
    def __init__(self):
        self.context = {}  # Diccionario global de variables
        self.functions = {}  # Diccionario para almacenar funciones definidas

    ############### Instrucciones básicas
    def fd(self, args):
        return f"t.fd({args[0]})"
    def bk(self, args):
        return f"t.bk({args[0]})"
    def lt(self, args):
        return f"t.lt({args[0]})"
    def rt(self, args):
        return f"t.rt({args[0]})"
    def pu(self, _):
        return "t.pu()"
    def pd(self, _):
        return "t.pd()"
    def wt(self, args):
        return f"t.width({args[0]})"
    
    ############### Operaciones booleanas
    def andOper(self, args):
        return f"({args[0]} and {args[1]})"
    def orOper(self, args):
        return f"({args[0]} or {args[1]})"
    def notOper(self, args):
        return f"(not {args[0]})"
    def true(self, _):
        return True
    def false(self, _):
        return False
    
    ############### Azucar sintáctica
    def increment(self, args):
        var_name = str(args[0])
        if var_name in self.context:
            self.context[var_name] += 1
            #print(f"DEBUG: Incremento -> {var_name} = {self.context[var_name]}")
            return f"{var_name} += 1"
        else:
            raise ValueError(f"Variable no definida: {var_name}")

    def decrement(self, args):
        var_name = str(args[0])
        if var_name in self.context:
            self.context[var_name] -= 1
            #print(f"DEBUG: Decremento -> {var_name} = {self.context[var_name]}")
            return f"{var_name} -= 1"
        else:
            raise ValueError(f"Variable no definida: {var_name}")

    # Operaciones combinadas (+= y -=)
    def add_assign(self, args):
        var_name, value = args
        if var_name in self.context:
            self.context[var_name] += value
            #print(f"DEBUG: Suma asignada -> {var_name} = {self.context[var_name]}")
            return f"{var_name} += {value}"
        else:
            raise ValueError(f"Variable no definida: {var_name}")

    def sub_assign(self, args):
        var_name, value = args
        if var_name in self.context:
            self.context[var_name] -= value
            #print(f"DEBUG: Resta asignada -> {var_name} = {self.context[var_name]}")
            return f"{var_name} -= {value}"
        else:
            raise ValueError(f"Variable no definida: {var_name}")

    ############### Manejo de variables
    def assign(self, args):
        var_name, value = args
        self.context[str(var_name)] = value
        #print(f"DEBUG: Asignación -> {var_name} = {value}")
        return f"{var_name} = {value}"

    def var(self, args):
        var_name = str(args[0])
        if var_name in self.context:
            #print(f"DEBUG: Uso de variable '{var_name}' con valor {self.context[var_name]}")
            return self.context[var_name]
        else:
            raise ValueError(f"Variable no definida: {var_name}")

    ############### Operaciones matemáticas
    def add(self, args):
        return f"({args[0]} + {args[1]})"
    def sub(self, args):
        return f"({args[0]} - {args[1]})"
    def mul(self, args):
        return f"({args[0]} * {args[1]})"
    def div(self, args):
        return f"({args[0]} / {args[1]})"
    def neg(self, args):
        return f"(-{args[0]})"
    def INTNUM(self, value):
        return int(value)


# ############################## Procesamiento de Archivos ##############################
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

        print(f"\033[1;37mArchivo convertido y guardado en: \033[35m{output_file}\033[0m")
    except Exception as e:
        print(f"Error al parsear el archivo: {e}")


# ############################## Ejecución del programa ##############################
# Mostrar mensaje de bienvenida
os.system("cls" if os.name == "nt" else "clear")
print(MensajeInterprete)

# Crear parser con transformador
parser = Lark(LogoPP, parser="lalr")

# Leer los argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("0=======================================0")
    print("\033[1;31m               Be careful!\033[0m")
    print(" Usage: python interprete.py archivo.lpp")
    print(Gato)
else:
    input_file = sys.argv[1]
    output_file = "Out" + os.path.basename(input_file).replace('.lpp', '.py')

    print("0=======================================0")
    print("            \033[1;37m You can do this!\033[0m")
    print(Gato)
    # Convertir el archivo
    convertir_archivo(input_file, output_file)