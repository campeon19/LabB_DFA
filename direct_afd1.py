
import graphviz
OPERATORS = ['|', '.', '*', '+', '?', '(', ')']


class Trancision:
    def __init__(self, simbolo, estado):
        self.simbolo = simbolo
        self.estado = estado

# La clase Estado es la encargada de almacenar el id del estado, si es final o no, y las trancisiones que tiene un estado hacia otros estados


class Estado:
    def __init__(self, id, es_final=False):
        self.id = id
        self.es_final = es_final
        self.trancisiones = {}
    # Se agrega una trancision al estado

    def agregar_trancision(self, simbolo, estado):
        # Si el simbolo ya existe en las trancisiones se agrega el estado al que se va a transicionar
        if simbolo in self.trancisiones:
            self.trancisiones[simbolo].append(estado)
        # Si el simbolo no existe en las trancisiones se crea una nueva trancision
        else:
            self.trancisiones[simbolo] = [estado]
    # Se obtienen las trancisiones de un estado

    def get_trancisiones(self, simbolo):
        if simbolo in self.trancisiones:
            return self.trancisiones[simbolo]
        else:
            return []
    # Se borra una trancision de un estado

    def borra_trancision(self, simbolo):
        if simbolo in self.trancisiones:
            del self.trancisiones[simbolo]


class AFD:

    def __init__(self):
        self.estados = set()
        self.estados_iniciales = set()
        self.estados_finales = set()

    def get_estados(self):
        return self.estados

    def get_estados_finales(self):
        return self.estados_finales

    def draw_afd(self):
        dot = graphviz.Digraph(comment='AFD')
        for estado in self.estados_finales:
            if estado.es_final:
                dot.node(str(estado.id), str(estado.id), shape="doublecircle")
            else:
                dot.node(str(estado.id), str(estado.id))
        for estado in self.estados:
            for simbolo in estado.trancisiones:
                for estado_siguiente in estado.get_trancisiones(simbolo):
                    dot.edge(str(estado.id), str(
                        estado_siguiente.id), label=simbolo)
        dot.format = 'png'
        dot.attr(rankdir='LR')
        dot.render('AFD2', view=True)

    def get_estado(self, id):
        for estado in self.estados_finales:
            print(estado.id)
            if estado.id == id:
                return estado


class Node:
    def __init__(self, valor, id):
        self.valor = valor
        self.id = id
        self.izquierda = None
        self.derecha = None
        self.nulabilidad = None
        self.primera_posicion = set()
        self.ultima_posicion = set()
        self.siguiente_posicion = set()


def build_tree(postfix):
    # Se crea una pila vacía
    stack = []
    id = 0
    # Se recorre la expresión regular
    for c in postfix:
        # Si se encuentra un simbolo alfanumerico se crea un nodo con el simbolo y se agrega a la pila
        if c not in OPERATORS:
            if c == 'ε':
                stack.append(Node('ε', None))
            else:
                stack.append(Node(c, id))
                id += 1
        # Si se encuentra un operador unario se crea un nodo con el operador y se saca un nodo de la pila y se agrega como hijo del nodo creado
        elif c == '*':
            node = Node(c, None)
            node.izquierda = stack.pop()
            stack.append(node)
        # Si se encuentra un operador se crea un nodo con el operador y se sacan los dos nodos de la pila y se agregan como hijos del nodo creado
        elif c == "|" or c == ".":
            node = Node(c, None)
            node.derecha = stack.pop()
            node.izquierda = stack.pop()
            node.valor = c
            stack.append(node)
    return stack.pop()


def draw_tree(root):
    # Se crea un grafo dirigido
    dot = graphviz.Digraph()
    # Se recorre el árbol de expresiones regulares

    def traverse(node):
        # Si el nodo no es nulo se crea un nodo con el id del nodo y el dato del nodo y se agregan las aristas correspondientes
        if node:
            pp = [str(x) for x in node.primera_posicion]
            up = [str(x) for x in node.ultima_posicion]
            r = node.valor + " " + str(pp) + " " + \
                str(up) + " " + str(node.nulabilidad)
            dot.node(str(id(node)), str(r))
            # Si el nodo tiene un hijo izquierdo se crea una arista entre el nodo y el hijo izquierdo
            if node.izquierda:
                dot.edge(str(id(node)), str(id(node.izquierda)))
            # Si el nodo tiene un hijo derecho se crea una arista entre el nodo y el hijo derecho
            if node.derecha:
                dot.edge(str(id(node)), str(id(node.derecha)))
            # Se recorre el hijo izquierdo y el hijo derecho utilizando recursividad
            traverse(node.izquierda)
            traverse(node.derecha)

    traverse(root)
    return dot


def calculate_nullable(root):
    if root is None:
        return False
    if root.valor not in OPERATORS:
        if root.valor == 'ε':
            root.nulabilidad = True
        else:
            root.nulabilidad = False
        return False
    if root.valor == '|':
        nullable = root.izquierda.nulabilidad or root.derecha.nulabilidad
    elif root.valor == '.':
        nullable = root.izquierda.nulabilidad and root.derecha.nulabilidad
    elif root.valor == '*':
        nullable = True
    else:
        nullable = False
    root.nulabilidad = nullable
    return nullable or False


def traverse_postorder(node, func):
    if node is not None:
        traverse_postorder(node.izquierda, func)
        traverse_postorder(node.derecha, func)
        func(node)


def calculate_first_position(node):
    if node:
        # Si el nodo es una hoja, su primera posición es su propio índice
        if node.izquierda is None and node.derecha is None:
            node.primera_posicion.add(node.id)
        # Si el nodo es un operador ., su primera posición es la primera posición de su hijo izquierdo
        elif node.valor == '.':
            calculate_first_position(node.izquierda)
            calculate_first_position(node.derecha)
            if node.izquierda.nulabilidad:
                node.primera_posicion = node.izquierda.primera_posicion.union(
                    node.derecha.primera_posicion)
            else:
                node.primera_posicion = node.izquierda.primera_posicion
        # Si el nodo es un operador |, su primera posición es la unión de las primeras posiciones de sus dos hijos
        elif node.valor == '|':
            calculate_first_position(node.izquierda)
            calculate_first_position(node.derecha)
            if list(node.izquierda.primera_posicion)[0] == None:
                node.primera_posicion = node.derecha.primera_posicion
            elif list(node.derecha.primera_posicion)[0] == None:
                node.primera_posicion = node.izquierda.primera_posicion
            else:
                node.primera_posicion = node.izquierda.primera_posicion.union(
                    node.derecha.primera_posicion)
        # Si el nodo es un operador *, su primera posición es la primera posición de su hijo
        elif node.valor == '*':
            calculate_first_position(node.izquierda)
            node.primera_posicion = node.izquierda.primera_posicion

        # Calcular la primera posición del hijo izquierdo y derecho utilizando recursividad
        calculate_first_position(node.izquierda)
        calculate_first_position(node.derecha)

    # Calcular la primera posición del nodo raíz
    if node and node.valor is not None and node.primera_posicion is None:
        node.primera_posicion = node.izquierda.primera_posicion


def calculate_last_position(node):
    if node:
        # Si el nodo es una hoja, su última posición es su propio índice
        if node.izquierda is None and node.derecha is None:
            node.ultima_posicion.add(node.id)
        # Si el nodo es un operador ., su última posición es la última posición de su hijo derecho
        elif node.valor == '.':
            calculate_last_position(node.izquierda)
            calculate_last_position(node.derecha)
            if node.derecha.nulabilidad:
                node.ultima_posicion = node.izquierda.ultima_posicion.union(
                    node.derecha.ultima_posicion)
            else:
                node.ultima_posicion = node.derecha.ultima_posicion
        # Si el nodo es un operador |, su última posición es la unión de las últimas posiciones de sus dos hijos
        elif node.valor == '|':
            calculate_last_position(node.izquierda)
            calculate_last_position(node.derecha)
            if list(node.izquierda.ultima_posicion)[0] == None:
                node.ultima_posicion = node.derecha.ultima_posicion
            elif list(node.derecha.ultima_posicion)[0] == None:
                node.ultima_posicion = node.izquierda.ultima_posicion
            else:
                node.ultima_posicion = node.izquierda.ultima_posicion.union(
                    node.derecha.ultima_posicion)
        # Si el nodo es un operador *, su última posición es la última posición de su hijo
        elif node.valor == '*':
            calculate_last_position(node.izquierda)
            node.ultima_posicion = node.izquierda.ultima_posicion

        # Calcular la última posición del hijo izquierdo y derecho utilizando recursividad
        calculate_last_position(node.izquierda)
        calculate_last_position(node.derecha)

    # Calcular la última posición del nodo raíz
    if node and node.valor is not None and node.ultima_posicion is None:
        node.ultima_posicion = node.derecha.ultima_posicion


def print_tree(arbol):
    if arbol:
        print(arbol.valor, arbol.nulabilidad)
        print_tree(arbol.izquierda)
        print_tree(arbol.derecha)


table = []


def calculate_follow_position(arbol):

    if arbol:

        if arbol.valor == '.':
            for i in arbol.izquierda.ultima_posicion:
                for j in arbol.derecha.primera_posicion:
                    # arbol.siguientes_posiciones[i].append(j)
                    for k in table:
                        if k[0] == i:
                            k[2].append(j)
                    else:
                        simbol = get_val_from_node(arbol, i)
                        table.append([i, simbol, [j]])
                    # if i in table:
                    #     table[i][2].append(j)
                    # else:
                    #     simbol = get_val_from_node(arbol, i)
                    #     table.append([i, arbol.izquierda.valor, [j]])
            # else:
            #     for i in arbol.izquierda.ultima_posicion:
            #         for j in arbol.derecha.primera_posicion:
            #             # arbol.siguientes_posiciones[i].append(j)
            #             for k in table:
            #                 if k[0] == i:
            #                     k[2].append(j)
            #             else:
            #                 simbol = get_val_from_node(arbol, i)
            #                 table.append([i, simbol, [j]])
        elif arbol.valor == '*':
            for i in arbol.ultima_posicion:
                for j in arbol.primera_posicion:
                    for k in table:
                        if k[0] == i:
                            k[2].append(j)
                        else:
                            simbol = get_val_from_node(arbol, i)
                            table.append([i, simbol, [j]])
                    # arbol.siguientes_posiciones[i].append(j)
        val = False
        for k in table:
            if k[0] == arbol.id:
                val = True
        if not val:
            simbol = get_val_from_node(arbol, arbol.id)
            table.append([arbol.id, simbol, []])
        # delete list with None in first position
        for i in table:
            if i[0] is None:
                table.remove(i)

        calculate_follow_position(arbol.izquierda)
        calculate_follow_position(arbol.derecha)


def get_val_from_node(arbol, id):
    if arbol:
        if arbol.id == id:
            return arbol.valor
        else:
            return get_val_from_node(arbol.izquierda, id) or get_val_from_node(arbol.derecha, id)


def get_first_position(arbol, id):
    if arbol:
        if arbol.id == id:
            return arbol.primera_posicion
        else:
            return get_first_position(arbol.izquierda, id) or get_first_position(arbol.derecha, id)


def get_siguiente_posicion(tab, id):
    for i in tab:
        if i[0] == id:
            return i[2]


def regex_to_afd(regex):

    arbol = build_tree(regex)
    # print(arbol.valor)
    # nulabilidad(arbol)
    calculate_nullable(arbol)
    traverse_postorder(arbol, calculate_nullable)
    calculate_first_position(arbol)
    calculate_last_position(arbol)
    calculate_follow_position(arbol)
    # order table
    tab = sorted(table, key=lambda x: x[0])
    print(tab)
    root = arbol.primera_posicion

    afd = AFD()
    transiciones = {}
    id = 0
    for i in root:
        transiciones[id] = get_siguiente_posicion(tab, i)
        id += 1
    print(transiciones[1])
    # for key, value in transiciones.items():
    #     estado = Estado(key)
    #     afd.estados.add(estado)

    # while True:
    #     for key, value in transiciones.items():
    #         for i in value:
    #             estado = Estado(key)
    #             estado2 = Estado(i)
    #             afd.agregar_transicion(
    #                 estado, get_val_from_node(arbol, i), estado2)
    #     break

    # afd.draw_afd()

    graph = draw_tree(arbol)
    graph.format = 'png'
    graph.render('tree2', view=False)
    # print arbol in console. For every node, print its value, nullability
    # print(arbol[-1].valor, arbol[-1].nulabilidad)
    return afd


def construir_afn(tabla):
    afd = AFD()
    estado_inicial = Estado(0)
    estado_final = Estado(1)
    afd.estados_iniciales.add(estado_inicial)
    afd.estados.add(estado_inicial)
    afd.estados.add(estado_final)
    afd.agregar_transicion(estado_inicial, tabla[0][1], estado_final)
    estado_anterior = estado_final
    posiciones_finales = []
    for fila in tabla[1:]:
        nuevo_estado = Estado(len(afd.estados))
        afd.estados.add(nuevo_estado)
        afd.agregar_transicion(estado_anterior, fila[1], nuevo_estado)
        if fila[2] == []:
            afd.estados_finales.add(nuevo_estado)
        else:
            posiciones_finales.append((nuevo_estado, fila[2][0]))
        estado_anterior = nuevo_estado
    for (estado, posicion) in posiciones_finales:
        nuevo_estado_final = Estado(len(afd.estados))
        afd.estados.add(nuevo_estado_final)
        afd.agregar_transicion(estado, posicion, nuevo_estado_final)
        afd.estados_finales.add(nuevo_estado_final)
    return afd


# regex = 'ac.c.bc.d.|#.'
regex = 'db|c|a|ε|db|.d*.#.'

arbol = regex_to_afd(regex)
# afd = construir_afn(table)
