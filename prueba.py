from lark import Lark

LogoPP = r"""
    start: instruction+

    ?instruction: basic
                | VARIABLE "=" math -> assign
                | bool
                | sugar

    ?bool:        bool "/\\" bool -> andOper
                | bool "\\/" bool -> orOper
                | "!" bool        -> notOper
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

try:
    parser = Lark(LogoPP, parser="lalr")
    print("Gramática compilada con éxito.")
except Exception as e:
    print("Error en la gramática:", e)