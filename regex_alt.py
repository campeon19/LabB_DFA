def alterar_regex(regex):
    # separa la expresion regular en una lista de caracteres
    regex = list(regex)
    # recorre la lista de caracteres y buscar los caracteres + y ? y cambiarlo de la siguiente manera:
    # a+ -> (aa*)
    # a? -> (a|ε)
    for i in range(len(regex)):
        if regex[i] == '+':
            regex[i] = '(' + regex[i-1] + regex[i-1] + '*' + ')'
            # elimina el caracter anterior
            regex.pop(i-1)
        elif regex[i] == '?':
            regex[i] = '(' + regex[i-1] + '|' + 'ε' + ')'
            # elimina el caracter anterior
            regex.pop(i-1)

    # une la lista de caracteres en una cadena
    regex = ''.join(regex)
    return regex


def convertir_expresion_regular(expresion):
    # Separar la expresión regular en una lista de caracteres
    lista_caracteres = [caracter for caracter in expresion]

    # Reemplazar los símbolos + y ? por sus equivalentes entre paréntesis
    for i in range(len(lista_caracteres)):
        if lista_caracteres[i] == '+':
            lista_caracteres[i] = '(' + lista_caracteres[i-1] + \
                lista_caracteres[i-1] + '*)'
            lista_caracteres[i-1] = ''
        elif lista_caracteres[i] == '?':
            lista_caracteres[i] = '(' + lista_caracteres[i-1] + '|ε)'
            lista_caracteres[i-1] = ''

    # Unir todo y regresar la nueva expresión regular
    nueva_expresion = ''.join(lista_caracteres)
    return nueva_expresion


regex = '0?(1?)?0*'
res = convertir_expresion_regular(regex)
print(res)
