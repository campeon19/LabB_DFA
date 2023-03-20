# Christian Perez - 19710
import graphviz

# La clase Nodo representa un nodo en el árbol de expresiones regulares

OPERATORS = ['|', '.', '*', '+', '?', '(', ')']


class Node:
    def __init__(self, data):
        self.id = id(self)
        self.data = data
        self.left = None
        self.right = None

# La función build_tree crea el árbol de expresiones regulares a partir de una expresión regular en notación postfija


def build_tree(postfix):
    # Se crea una pila vacía
    stack = []
    # Se recorre la expresión regular
    for c in postfix:
        # Si se encuentra un simbolo alfanumerico se crea un nodo con el simbolo y se agrega a la pila
        if c not in OPERATORS:
            stack.append(Node(c))
        # Si se encuentra un operador unario se crea un nodo con el operador y se saca un nodo de la pila y se agrega como hijo del nodo creado
        elif c == '*' or c == '?' or c == '+':
            node = Node(c)
            node.left = stack.pop()
            stack.append(node)
        # Si se encuentra un operador se crea un nodo con el operador y se sacan los dos nodos de la pila y se agregan como hijos del nodo creado
        else:
            node = Node(c)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    return stack.pop()

# La función draw_tree crea un arbol a partir de un nodo raiz de una expresión regular en notación postfija


def draw_tree(root):
    # Se crea un grafo dirigido
    dot = graphviz.Digraph()
    # Se recorre el árbol de expresiones regulares

    def traverse(node):
        # Si el nodo no es nulo se crea un nodo con el id del nodo y el dato del nodo y se agregan las aristas correspondientes
        if node:
            dot.node(str(id(node)), node.data)
            # Si el nodo tiene un hijo izquierdo se crea una arista entre el nodo y el hijo izquierdo
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)))
            # Si el nodo tiene un hijo derecho se crea una arista entre el nodo y el hijo derecho
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)))
            # Se recorre el hijo izquierdo y el hijo derecho utilizando recursividad
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    return dot

# La función show_tree crea el árbol de expresiones regulares y lo muestra en una ventana en formato png


def show_tree(postfix):
    tree = build_tree(postfix)
    dot = draw_tree(tree)
    dot.format = 'png'
    dot.render('tree', view=False)
