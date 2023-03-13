# Christian Perez - 19710
from graphviz import Digraph
# Se definen los operadores que se van a utilizar
EPSILON = 'ε'
CONCAT = "."
UNION = "|"
STAR = "*"
QUESTION = "?"
PLUS = "+"

# La clase Simbolo es la encargada de almacenar el simbolo y su id (id del simbolo en la tabla ASCII)


class Simbolo:
    def __init__(self, simbolo):
        self.c_id = simbolo
        self.id = ord(simbolo)

# La clase Trancision es la encargada de almacenar el simbolo y el estado al que se va a transicionar


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

# La clase AFN es la encargada de almacenar el estado inicial y el estado final del AFN y tambien de dibujar el AFN final.


class AFN:
    def __init__(self, estado_inicial, estado_final):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
    # Se obtienen los estados del AFN

    def __repr__(self):
        return f"AFN({self.estado_inicial}, {self.estado_final})"
    # Se obtienen los estados del AFN

    def get_estados(self):
        # Se crea un conjunto de estados
        estados = set()
        # Se llama a la funcion _get_estados
        self._get_estados(self.estado_inicial, estados)
        return estados
    # Se obtienen los estados del AFN

    def _get_estados(self, estado, estados):
        # Si el estado ya existe en el conjunto de estados se retorna
        if estado in estados:
            return
        # Si el estado no existe en el conjunto de estados se agrega
        estados.add(estado)
        # Se recorren los simbolos de las trancisiones del estado
        for simbolo in estado.trancisiones:
            # Se recorren los estados a los que se transiciona con el simbolo
            for next_estado in estado.get_trancisiones(simbolo):
                # Se llama a la funcion recursiva _get_estados
                self._get_estados(next_estado, estados)

    # Se imprime el AFN
    def print_afn(self):
        dot = Digraph()
        dot.attr('node', shape='doublecircle')
        dot.node(str(self.estado_final.id))
        dot.attr('node', shape='circle')
        dot.node('start', style='invis')
        dot.edge('start', str(self.estado_inicial.id))
        # para cada estado en el AFN
        for estado in self.get_estados():
            # para cada simbolo en las trancisiones del estado
            for simbolo in estado.trancisiones:
                # para cada estado al que se transiciona con el simbolo
                for next_estado in estado.get_trancisiones(simbolo):
                    # se crea una arista entre el estado y el estado al que se transiciona con el simbolo
                    dot.edge(str(estado.id), str(
                        next_estado.id), label=str(simbolo))
        # se guarda el AFN en un archivo .png y en forma de izquierda a derecha y se muestra
        dot.format = 'png'
        dot.attr(rankdir='LR')
        dot.render('afn', view=True)

    def get_estado(self, id):
        # para cada estado en el AFN
        for estado in self.get_estados():
            # si el id del estado es igual al id del estado que se quiere obtener
            if estado.id == id:
                # se retorna el estado
                return estado
        # si no se encuentra el estado se retorna None
        return None


# Se crea la funcion que convierte una expresion regular a un AFN utilizando el algorithmo de Thompson


def postfix_to_afn(postfix):
    # Se crea una pila
    stack = []
    # Se define un id que servira para asignar un id a cada estado del AFN
    id = 0
    # Para cada simbolo en la expresion regular
    for simbolo in postfix:
        # Si el simbolo es un "."
        if simbolo == CONCAT:
            # Se obtienen los dos ultimos AFN de la pila
            afn2 = stack.pop()
            afn1 = stack.pop()
            afn1.estado_final.es_final = False
            # Se obtiene el simbolos de las trancisiones del estado final del segundo AFN
            af2Simbolo = afn2.estado_inicial.trancisiones.keys()
            # Se recorren los simbolos de las trancisiones del estado final del segundo AFN
            for simbolo in af2Simbolo:
                # Se recorren el estado inicial del segundo a los que se transiciona con el simbolo
                for estado in afn2.estado_inicial.get_trancisiones(simbolo):
                    # Se agrega una trancision al estado final del primer AFN con el simbolo y el estado inicial del segundo AFN
                    # Con esto se logra borrar el estado extra y concatenar los dos AFN sin necesidad de uniones EPSILON
                    afn1.estado_final.agregar_trancision(simbolo, estado)
            # Se crea un nuevo AFN con el estado inicial del primer AFN y el estado final del segundo AFN
            newAFN = AFN(afn1.estado_inicial, afn2.estado_final)
            stack.append(newAFN)
        # Si el simbolo es un "|"
        elif simbolo == UNION:
            # Se obtienen los dos ultimos AFN de la pila
            afn2 = stack.pop()
            afn1 = stack.pop()
            # Se crea un nuevo estado inicial y un nuevo estado final y se les asigna un id
            estado_inicial = Estado(id)
            id += 1
            estado_final = Estado(id)
            id += 1
            # Se agrega una trancision EPSILON al estado inicial con el estado inicial del primer AFN y el estado inicial del segundo AFN
            estado_inicial.agregar_trancision(EPSILON, afn1.estado_inicial)
            estado_inicial.agregar_trancision(EPSILON, afn2.estado_inicial)
            afn1.estado_final.es_final = False
            # Se agrega una trancision EPSILON al estado final del primer AFN y al estado final con el nuevo estado final
            afn1.estado_final.agregar_trancision(EPSILON, estado_final)
            afn2.estado_final.es_final = False
            # Se agrega una trancision EPSILON al estado final del segundo AFN y al estado final con el nuevo estado final
            afn2.estado_final.agregar_trancision(EPSILON, estado_final)
            # Se crea un nuevo AFN con el nuevo estado inicial y el nuevo estado final
            newAFN = AFN(estado_inicial, estado_final)
            stack.append(newAFN)
        # Si el simbolo es un "*"
        elif simbolo == STAR:
            # Se obtiene el ultimo AFN de la pila
            afn = stack.pop()
            # Se crea un nuevo estado inicial y un nuevo estado final y se les asigna un id
            estado_inicial = Estado(id)
            id += 1
            estado_final = Estado(id)
            id += 1
            # Se agrega una trancision EPSILON del nuevo estado inicial, al estado inicial del AFN y al nuevo estado final
            estado_inicial.agregar_trancision(EPSILON, afn.estado_inicial)
            estado_inicial.agregar_trancision(EPSILON, estado_final)
            afn.estado_final.es_final = False
            # Se agrega una trancision EPSILON del estado final del AFN, al estado inicial del AFN y al nuevo estado final
            afn.estado_final.agregar_trancision(EPSILON, afn.estado_inicial)
            afn.estado_final.agregar_trancision(EPSILON, estado_final)
            # Se crea un nuevo AFN con el nuevo estado inicial y el nuevo estado final
            newAFN = AFN(estado_inicial, estado_final)
            stack.append(newAFN)
        # Si el simbolo es un "?"
        elif simbolo == QUESTION:
            # Se obtiene el ultimo AFN de la pila
            afn = stack.pop()
            # Se crean 4 estados nuevos y se les asigna un id
            estado_inicial = Estado(id)
            id += 1
            estado_intermedio1 = Estado(id)
            id += 1
            estado_intermedio2 = Estado(id)
            id += 1
            estado_final = Estado(id)
            id += 1
            # Se agrega una trancision EPSILON del nuevo estado inicial, al estado inicial del AFN
            estado_inicial.agregar_trancision(EPSILON, afn.estado_inicial)
            afn.estado_final.es_final = False
            # Se agrega una trancision EPSILON del estado final del AFN, al nuevo estado final
            afn.estado_final.agregar_trancision(EPSILON, estado_final)
            # Se agrega una trancision EPSILON del nuevo estado inicial, al nuevo siguiente estado que contendra EPSILON
            estado_inicial.agregar_trancision(EPSILON, estado_intermedio1)
            # Se agrega una trancision EPSILON del estado anterior al siguiente que es el EPSILON del a|E
            estado_intermedio1.agregar_trancision(EPSILON, estado_intermedio2)
            # Se agrega una trancision EPSILON del estado anterior al estado final
            estado_intermedio2.agregar_trancision(EPSILON, estado_final)
            newAFN = AFN(estado_inicial, estado_final)
            stack.append(newAFN)
        # Si el simbolo es un "+"
        elif simbolo == PLUS:
            # Se obtiene el ultimo AFN de la pila
            afn = stack.pop()
            # Se crean 3 estados nuevos y se les asigna un id
            estado_inicial = Estado(id)
            id += 1
            estado_intermedio = Estado(id)
            id += 1
            estado_final = Estado(id)
            id += 1
            afn.estado_final.es_final = False
            # Se agrega una trancision EPSILON del estado final del AFN al siguiente estado
            afn.estado_final.agregar_trancision(EPSILON, estado_inicial)
            # Se agrega una trancision EPSILON del estado final del AFN al nuevo estado final
            afn.estado_final.agregar_trancision(EPSILON, estado_final)
            # Se agrega una trancision EPSILON del estado intermedio al inicial
            estado_intermedio.agregar_trancision(EPSILON, estado_inicial)
            # Se agrega una trancision EPSILON del estado intermedio al estado final
            estado_intermedio.agregar_trancision(EPSILON, estado_final)
            # se obtiene el simbolo del estado anterior para poder aplicar aa* siguiendo lo mismo que en la concatenacion
            afnSimbolo = afn.estado_inicial.trancisiones.keys()
            for simbolo in afnSimbolo:
                for estado in afn.estado_inicial.get_trancisiones(simbolo):
                    # se agrega una trancision del estado inicial al estado intermedio
                    estado_inicial.agregar_trancision(
                        simbolo, estado_intermedio)
            newAFN = AFN(afn.estado_inicial, estado_final)
            stack.append(newAFN)
        else:
            # Si el simbolo es un simbolo y no un operador, simplemente se crean 2 estados y se unen con el simbolo
            estado_inicial = Estado(id)
            id += 1
            estado_final = Estado(id, True)
            id += 1
            estado_inicial.agregar_trancision(simbolo, estado_final)
            newAFN = AFN(estado_inicial, estado_final)
            stack.append(newAFN)
    return stack.pop()


class AFD:

    def __init__(self):
        self.estados = set()
        self.estados_iniciales = set()
        self.estados_finales = set()

    def get_estados(self):
        return self.estados

    def draw_afd(self):
        dot = Digraph(comment='AFD')
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
        dot.render('AFD.gv', view=True)


def cerradura_epsilon(connjunto, afn):
    estados_visitados = []
    estados_por_visitar = []
    for estado in connjunto:
        estados_por_visitar.append(estado)
    while estados_por_visitar:
        estado = estados_por_visitar.pop()
        if estado not in estados_visitados:
            estados_visitados.append(estado)
            for estado_siguiente in afn.get_estado(estado).get_trancisiones(EPSILON):
                estados_por_visitar.append(estado_siguiente.id)
    return estados_visitados


def mover(conjunto, simbolo):
    estados_siguientes = []
    for estado in conjunto:
        for estado_siguiente in afn.get_estado(estado).get_trancisiones(simbolo):
            estados_siguientes.append(estado_siguiente.id)
    return estados_siguientes


def afd_from_afn(afn, alfabeto):
    afd = AFD()
    id = 0
    alfabeto = alfabeto
    conjunto_estados = {}
    # Se obtiene el estado inicial del AFN
    estado_inicial = [afn.estado_inicial.id]
    conjunto_estados[id
                     ] = cerradura_epsilon(estado_inicial, afn)
    estados_por_visitar = [id]
    id += 1
    while estados_por_visitar:
        conjunto = estados_por_visitar.pop()
        for simbolo in alfabeto:
            estados_siguientes = cerradura_epsilon(
                mover(conjunto_estados[conjunto], simbolo), afn)
            if estados_siguientes:
                if estados_siguientes not in conjunto_estados.values():
                    conjunto_estados[id] = estados_siguientes
                    estados_por_visitar.append(id)
                    id += 1
                for key, value in conjunto_estados.items():
                    if estados_siguientes == value:
                        estado = Estado(conjunto)
                        estado.agregar_trancision(
                            simbolo, Estado(key))
                        afd.estados.add(estado)
    for key, value in conjunto_estados.items():
        if afn.estado_final.id in value:
            afd.estados_finales.add(Estado(key, True))
        else:
            afd.estados_finales.add(Estado(key))
    afd.estados_iniciales.add(Estado(0))
    print("afd created")
    print(conjunto_estados)
    return afd


def get_alfabet(expresion_regular):
    alfabet = set()
    for char in expresion_regular:
        if char not in OPERADORES and char not in PARENTESIS:
            alfabet.add(char)
    return alfabet


OPERADORES = [EPSILON, CONCAT, UNION, STAR, QUESTION, PLUS]
PARENTESIS = ['(', ')']

# get a dictionary with the states of the afn as keys and its trancisions as values


def get_estados(afn):
    estados = {}
    set_estados = afn.get_estados()
    for estado in set_estados:
        estados[estado.id] = estado.trancisiones
    return estados


regex = 'ab|'
alfabet = get_alfabet(regex)
print(alfabet)
afn = postfix_to_afn(regex)
print("afn created")
afd = afd_from_afn(afn, alfabet)
afd.draw_afd()
