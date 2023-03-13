from NFA import postfix_to_afn
from postfix import infix_to_postfix
from tree_visualizer import show_tree
from input_correction import validate_regex


def main():
    regular_expression = input("Enter a regular expression: ")
    # borrar espacios en blanco
    regular_expression = regular_expression.replace(" ", "")
    if validate_regex(regular_expression):
        postfix = infix_to_postfix(regular_expression)
        print(postfix)
        show_tree(postfix)
        print("Arbol de expresión regular generado y guardado como 'tree.png'")
        afn = postfix_to_afn(postfix)
        afn.print_afn()
        print("AFN generado y guardado como 'afn.png'")
        print("Gracias por usar el programa")


if __name__ == "__main__":
    main()
