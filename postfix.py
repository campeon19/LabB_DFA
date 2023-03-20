# Christian Perez - 19710
import os
# Si da problemas el path de graphviz, agregar la siguiente linea de codigo
os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\bin'

OPERATORS = ['|', '.', '*', '+', '?', '(', ')']

# La funcion shunting_yard() es la encargada de convertir la expresion regular de infijo a postfijo


def shunting_yard(infix):
    # precedencia de los operadores
    precedence = {'|': 1, '.': 2, '?': 3, '*': 3, '+': 3}
    # pila de operadores
    stack = []
    # cola de salida
    postfix = []
    for i, c in enumerate(infix):
        # Si se encuentra un ( se agrega a la pila
        if c == '(':
            stack.append(c)
        # Si se encuentra un ) se sacan los operadores de la pila hasta encontrar un (
        elif c == ')':
            while stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        # Si se encuentra un operador se sacan los operadores de la pila hasta encontrar un operador de menor precedencia
        elif c in precedence:
            while stack and stack[-1] != '(' and precedence[c] <= precedence[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(c)
        # Si se encuentra un simbolo se agrega a la cola de salida
        else:
            postfix.append(c)
    # Se sacan los operadores restantes de la pila y se agregan a la cola de salida
    while stack:
        postfix.append(stack.pop())

    return postfix

# La funcion add_concatenation() es la encargada de agregar el operador de concatenacion (.) a la expresion regular


def add_concatenation(exp):
    output = []  # cola de salida

    # Se recorre la expresion regular
    for i, char in enumerate(exp):
        # Si se encuentra un simbolo alfanumerico seguido de un simbolo alfanumerico o un ( se agrega el operador de concatenacion (.)
        # Si se encuentra un ) seguido de un simbolo alfanumerico o un ( se agrega el operador de concatenacion (.)
        # Si se encuentra un * seguido de un ( se agrega el operador de concatenacion (.)
        # Si se encuentra un + seguido de un ( se agrega el operador de concatenacion (.)
        # Si se encuentra un ? seguido de un ( se agrega el operador de concatenacion (.)
        # Si se encuentra un * seguido de un simbolo alfanumerico se agrega el operador de concatenacion (.)
        # Si se encuentra un + seguido de un simbolo alfanumerico se agrega el operador de concatenacion (.)
        # Si se encuentra un ? seguido de un simbolo alfanumerico se agrega el operador de concatenacion (.)
        if char not in OPERATORS and i < len(exp) - 1 and exp[i + 1] not in OPERATORS or \
                char == ')' and i < len(exp) - 1 and exp[i + 1] not in OPERATORS or \
                char not in OPERATORS and i < len(exp) - 1 and exp[i + 1] == '(' or \
                char == ')' and i < len(exp) - 1 and exp[i + 1] == '(' or \
                char == '*' and i < len(exp) - 1 and exp[i + 1] == '(' or \
                char == '+' and i < len(exp) - 1 and exp[i + 1] == '(' or \
                char == '?' and i < len(exp) - 1 and exp[i + 1] == '(' or \
                char == '*' and i < len(exp) - 1 and exp[i + 1] not in OPERATORS or \
                char == '+' and i < len(exp) - 1 and exp[i + 1] not in OPERATORS or \
                char == '?' and i < len(exp) - 1 and exp[i + 1] not in OPERATORS:
            output.append(char)
            output.append('.')
        else:
            # Si no se cumple ninguna de las condiciones anteriores se agrega el simbolo a la cola de salida
            output.append(char)

    return ''.join(output)


# La funcion infix_to_postfix() es la encargada de llamar a las funciones add_concatenation() y shunting_yard()
def infix_to_postfix(infix):
    resultado = add_concatenation(infix)
    resultado = shunting_yard(resultado)
    resultado = ''.join(resultado)
    return resultado
