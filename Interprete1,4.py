from lark import Lark, Transformer, tree
import sys
import os

# Cambiar a elección.
class Config:
    SinArboles = False  # Si se desea graficar el árbol sintáctico
    Arboldot = True  # Si se desea guardar el árbol sintáctico como archivo DOT
    Arbolpng = True  # Si se desea guardar el árbol sintáctico como imagen PNG
    Arbolcmd = False  # Si se desea mostrar el árbol sintáctico

# To-Do:
# Ya implementado:
#                | basic
#                | sugar
#                | math
#                | Variables
#                | function
#                | call
#                | bool
#                | control
#                | loop
#                > Arboles PNG y DOT
# Aún no implementado:



# ############################## Mensajes ##############################
# Creditos
class Mensajes:
    Creditos = """
          ^~^  ,      This code was generated using the Logo++ Interpreter
         ('Y') )      by [Catto] Juan Diego Ruiz B, Juan Camilo Marin H. && Luisa Lopez.
         /   \/       special thanks to: Mochi.
        (\|||/)       >> This code is under MIT License. <<
    """
    # Mensaje de bienvenida
    MensajeInterprete = """
           \033[37;1m Logo++ Interpreter \033[0m
            Versión Beta 1.4.0
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
                | sugar
                | function
                | call

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
                | VARIABLE       -> var
                | "-" factor     -> neg
                | "(" math ")"

    ?bool:        atom
                | bool "AND" bool  -> andOper
                | bool "OR" bool   -> orOper
                | "NOT" bool       -> notOper

    ?atom:        "TRUE"           -> trueVal
                | "FALSE"          -> falseVal

    ?function:    "DEF" VARIABLE "(" [VARIABLE ("," VARIABLE)*] ")" "{" instruction+ "}" -> defFunction

    ?call:        VARIABLE "(" [VARIABLE ("," VARIABLE)*] ")"                            -> callFunction

    ?control:     "IF" bool "{" instruction+ "}" -> ifOper

    ?loop:        "FOR" VARIABLE "IN" "RANGE(" VARIABLE ")" "{" instruction+ "}"         -> forOper
                | "FOR" VARIABLE "," VARIABLE "IN" "ZIP(" "RANGE(" INTNUM "," INTNUM "," INTNUM ")" "," "RANGE(" INTNUM "," INTNUM "," INTNUM ")" ")" "{" instruction+ "}" -> forforOper

    UNEXPECTED: /.+/

    %ignore UNEXPECTED
    %ignore /#[^\n]*/
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
    
    ############### Definición y llamada de funciones
    def defFunction(self, args):
        function_name = str(args[0])
        parameters = [str(arg) for arg in args[1:]]
        self.functions[function_name] = parameters
        param_list = ", ".join(parameters)
        return f"def {function_name}({param_list}):"

    def callFunction(self, args):
        function_name = str(args[0])
        arguments = [str(arg) for arg in args[1:]]
        if function_name in self.functions:
            arg_list = ", ".join(arguments)
            return f"{function_name}({arg_list})"
        else:
            raise ValueError(f"Función no definida: {function_name}")

    ############### Operaciones booleanas
    def trueVal(self, _):
        return True
    def falseVal(self, _):
        return False
    def andOper(self, args):
        return f"({args[0]} and {args[1]})"
    def orOper(self, args):
        return f"({args[0]} or {args[1]})"
    def notOper(self, args):
        return f"(not {args[0]})"

    ############### Control
    def ifOper(self, args):
        return f"if {args[0]}:"
    def elseOper(self, _):
        return "else:"
    def elifOper(self, args):
        return f"elif {args[0]}:"

    ############### Ciclos
    def forOper(self, args):
        return f"for {args[0]} in range({args[1]}):"
    
    def forforOper(self, args):
        return f"for {args[0]}, {args[1]} in zip(range({args[2]}, {args[3]}, {args[4]}), range({args[5]}, {args[6]}, {args[7]}):"
    

# ############################## Procesamiento de Archivos ##############################
# Graficador de arboles
def procesar_ast(arbol):
    if not Config.SinArboles:
        try:
            # Imprimir el AST en la consola
            if Config.Arbolcmd:
                print("\033[1;34mÁrbol Sintáctico:\033[0m")
                print(arbol.pretty())

            # Guardar el AST como imagen y archivo DOT
            if Config.Arbolpng:
                tree.pydot__tree_to_png(arbol, "tree.png")  # Guarda como imagen PNG
            else:
                print("\033[1;33mEl árbol sintáctico en PNG no se mostrará.\033[0m")

            if Config.Arboldot:
                tree.pydot__tree_to_dot(arbol, "tree.dot", rankdir="TD")  # Guarda como archivo DOT
            else:
                print("\033[1;33mEl árbol sintáctico en DOT no se creará.\033[0m")

            if Config.Arbolpng or Config.Arboldot:
                print("\033[1;32mAST visual guardado como 'tree.png' y/o 'tree.dot'.\033[0m")
            else:
                print("\033[1;33mRevisar la configuración\033[0")

        except Exception as e:
            print(f"Error al procesar el AST: {e}")
    else:
        print("\033[1;33mNo se va a guardar ningún arbol.\033[0m")

# Función principal para procesar archivos
def convertir_archivo(input_file, output_file):
    try:
        # Leer el archivo de entrada
        with open(input_file, 'r') as infile:
            contenido = infile.read().strip()  # Limpia la entrada

        # Parsear el contenido
        arbol = parser.parse(contenido)

        # Procesar el AST para graficar
        procesar_ast(arbol)

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
            outfile.write("\n" + Mensajes.Creditos)

        print(f"\033[1;37mArchivo convertido y guardado en: \033[35m{output_file}\033[0m")
    except Exception as e:
        print(f"Error al parsear el archivo: {e}")


# ############################## Ejecución del programa ##############################
# Mostrar mensaje de bienvenida
os.system("cls" if os.name == "nt" else "clear")
print(Mensajes.MensajeInterprete)

# Crear parser con transformador
try:
    parser = Lark(LogoPP, parser="lalr")
    print("Gramática cargada correctamente.")
except Exception as e:
    print(f"Error al cargar la gramática: {e}")


# Leer los argumentos de la línea de comandos
if len(sys.argv) != 2:
    print("0=======================================0")
    print("\033[1;31m               Be careful!\033[0m")
    print(" Usage: python interprete.py archivo.lpp")
    print(Mensajes.Gato)
else:
    input_file = sys.argv[1]
    output_file = "Out" + os.path.basename(input_file).replace('.lpp', '.py')

    print("0=======================================0")
    print("            \033[1;37m You can do this!\033[0m")
    print(Mensajes.Gato)
    # Convertir el archivo
    convertir_archivo(input_file, output_file)
