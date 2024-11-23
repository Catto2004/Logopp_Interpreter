from lark import Lark, Transformer
import sys
import os

# Creditos
Creditos = """
#          ^~^  ,      
#         ('Y') )      This code was generated using the Logo++ Interpreter
#         /   \/       by [Catto] Juan Diego Ruiz B && Juan Camilo Marin H. 
#        (\|||/)       Under MIT License. 
"""


# Mensaje de bienvenida
MensajeInterprete = """
           \033[37;1m Logo++ Interpreter \033[0m
"""

# Gato ASCII
Gato = """0======v================================0
       \ \033[93m  ^~^  ,
          ('Y') )
          /   \/
         (\|||/)
\033[0m"""

# Gramática
LogoPP = r"""
    start: instruction+

    ?instruction: basic
                | VARIABLE "=" math -> assign
                | function_def
                | function_call

    ?basic:       "FD" math -> fd
                | "BK" math -> bk
                | "LT" math -> lt
                | "RT" math -> rt
                | "PU"      -> pu
                | "PD"      -> pd
                | "WT" math -> wt

    ?function_def: "DEF" VARIABLE "(" [VARIABLE ("," VARIABLE)*] ")" "{" instruction+ "}" -> define_function

    ?function_call: VARIABLE "(" [math ("," math)*] ")" -> call_function

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
    VARIABLE: /[a-zA-Z_][a-zA-Z0-9_]*/
    INTNUM: /-?\d+(\.\d+)?([eE][+-]?\d+)?/x
    %ignore /[ \t\n\f\r]+/x
"""

# Arbol de gramatica
class CalcularArbol(Transformer):
    def __init__(self):
        self.context = {}  # Diccionario global de variables
        self.functions = {}  # Diccionario para almacenar funciones definidas

    # Instrucciones básicas
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

    # Manejo de variables
    def assign(self, args):
        var_name, value = args
        self.context[str(var_name)] = value
        print(f"DEBUG: Asignación -> {var_name} = {value}")
        return ""

    def var(self, args):
        var_name = str(args[0])
        if var_name in self.context:
            print(f"DEBUG: Uso de variable '{var_name}' con valor {self.context[var_name]}")
            return self.context[var_name]
        else:
            raise ValueError(f"Variable no definida: {var_name}")

    # Operaciones matemáticas
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

    # Definición de funciones
    def define_function(self, args):
        func_name = str(args[0])
        parameters = [str(param) for param in args[1:-1]]
        body = args[-1]
        self.functions[func_name] = (parameters, body)
        print(f"DEBUG: Función definida -> {func_name} con parámetros {parameters}")
        return ""

    def call_function(self, args):
        func_name = str(args[0])
        if func_name not in self.functions:
            raise ValueError(f"Función no definida: {func_name}")

        # Obtener parámetros y cuerpo de la función
        parameters, body = self.functions[func_name]
        arguments = args[1:]

        if len(parameters) != len(arguments):
            raise ValueError(f"Número incorrecto de argumentos para {func_name}: se esperaban {len(parameters)}, se recibieron {len(arguments)}")

        # Crear un contexto temporal para los parámetros
        temp_context = self.context.copy()
        for param, arg in zip(parameters, arguments):
            temp_context[param] = arg
            print(f"DEBUG: Asignando argumento {param} = {arg}")

        # Guardar el contexto anterior y reemplazarlo con el temporal
        old_context = self.context
        self.context = temp_context

        # Transformar cada instrucción en el cuerpo
        result = []
        if hasattr(body, 'children'):  # Asegúrate de que body es un nodo con hijos
            for instruction in body.children:
                transformed = self.transform(instruction)
                if transformed:  # Evita añadir instrucciones vacías
                    result.append(transformed)
        else:
            raise ValueError(f"Error en el cuerpo de la función '{func_name}': no contiene instrucciones.")

        # Restaurar el contexto anterior
        self.context = old_context

        return result





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

        print(f"\033[1;37mArchivo convertido y guardado en: \033[35m{output_file}\033[0m")
    except Exception as e:
        print(f"Error al parsear el archivo: {e}")

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