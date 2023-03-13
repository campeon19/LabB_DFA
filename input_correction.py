# Christian Perez - 19710
import re

# validacion de expresiones regulares donde recibe una expresion regular y devuelve True si es valida y False si no lo es mostrando porque no es valida


def validate_regex(regex):
    try:
        # Se validan diferentes parametros de la expresion regular
        if re.search(r"\|\|", regex):
            raise re.error("Hay dos o más operadores | consecutivos")
        elif re.search(r"\|\)", regex):
            raise re.error(
                "Hay un operador | seguido de un paréntesis de cierre")
        elif re.search(r"\(\|", regex):
            raise re.error(
                "Hay un paréntesis de apertura seguido de un operador |")
        elif re.search(r"\(\)", regex):
            raise re.error(
                "Hay un paréntesis de apertura seguido de un paréntesis de cierre sin nada entre ellos")
        elif re.search(r"\(\*", regex):
            raise re.error(
                "Hay un paréntesis de apertura seguido de un operador *")
        elif re.search(r"\(\?", regex):
            raise re.error(
                "Hay un paréntesis de apertura seguido de un operador ?")
        elif re.search(r"\(\+", regex):
            raise re.error(
                "Hay un paréntesis de apertura seguido de un operador +")
        # Verificar si hay un caracter alfanumérico antes y despues de |
        elif re.search(r"\|", regex):
            if re.search(r"\|", regex).start() == 0 or re.search(r"\|", regex).end() == len(regex):
                raise re.error(
                    "Hay un operador | al inicio o al final de la expresión regular o no hay un simbolo antes y/o después de él")

        # Si paso la expresion regular las pruebas anteriores, pasara luego por re.compile()
        # para verificar si la expresion regular es valida utilizando otros parametros como los parentesis
        # si no es valida, se mostrara el error y devolvera False, si es valida, devolvera True
        re.compile(regex)
        print("La expresión regular es válida")
        return True
    except re.error as e:
        # Retorno del error de la expresion regular
        print("La expresión regular no es válida: {}".format(str(e)))
        return False
