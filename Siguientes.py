from collections import defaultdict

EPSILON = 'ε'
EOF = '$'

class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.non_terminals = list(productions.keys())
        self.terminals = set()

        for head in productions:
            for prod in productions[head]:
                for symbol in prod:
                    if symbol not in productions and symbol != EPSILON:
                        self.terminals.add(symbol)

        self.first = defaultdict(set)
        self.follow = defaultdict(set)

    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for head in self.productions:
                for prod in self.productions[head]:
                    i = 0
                    while True:
                        if i == len(prod):
                            if EPSILON not in self.first[head]:
                                self.first[head].add(EPSILON)
                                changed = True
                            break

                        symbol = prod[i]

                        if symbol not in self.productions:  
                            if symbol not in self.first[head]:
                                self.first[head].add(symbol)
                                changed = True
                            break
                        else:
                            before = len(self.first[head])
                            self.first[head] |= (self.first[symbol] - {EPSILON})
                            if EPSILON in self.first[symbol]:
                                i += 1
                            else:
                                break
                            if len(self.first[head]) > before:
                                changed = True

    def compute_follow(self, start_symbol):
        self.follow[start_symbol].add(EOF)

        changed = True
        while changed:
            changed = False
            for head in self.productions:
                for prod in self.productions[head]:
                    trailer = self.follow[head].copy()
                    for symbol in reversed(prod):
                        if symbol in self.productions:
                            before = len(self.follow[symbol])
                            self.follow[symbol] |= trailer
                            if EPSILON in self.first[symbol]:
                                trailer |= (self.first[symbol] - {EPSILON})
                            else:
                                trailer = self.first[symbol]
                            if len(self.follow[symbol]) > before:
                                changed = True
                        else:
                            if symbol != EPSILON:
                                trailer = {symbol}

    def first_of_string(self, symbols):
        result = set()
        for symbol in symbols:
            if symbol not in self.productions:
                if symbol != EPSILON:
                    result.add(symbol)
                    return result
                else:
                    result.add(EPSILON)
                    return result
            result |= (self.first[symbol] - {EPSILON})
            if EPSILON not in self.first[symbol]:
                return result
        result.add(EPSILON)
        return result

    def compute_prediction(self):
        """
        Conjunto de PREDICCIÓN (o selección) de cada regla A -> α:
          PRED(A -> α) = PRIMEROS(α) - {ε}  ∪  (SIGUIENTES(A) si ε ∈ PRIMEROS(α))
        """
        prediction = {}
        for head in self.productions:
            for prod in self.productions[head]:
                first_alpha = self.first_of_string(prod)
                pred = first_alpha - {EPSILON}
                if EPSILON in first_alpha:
                    pred |= self.follow[head]
                prediction[(head, tuple(prod))] = pred
        return prediction




def print_sets(title, sets):
    print(f"\n  {title}:")
    for k in sets:
        symbols = ', '.join(sorted(sets[k]))
        print(f"    {k}:  {{ {symbols} }}")


def print_prediction(prediction):
    print("\n  CONJUNTOS DE PREDICCIÓN:")
    for (head, prod), pred_set in prediction.items():
        prod_str = ' '.join(prod)
        symbols = ', '.join(sorted(pred_set))
        print(f"    {head} -> {prod_str}  :  {{ {symbols} }}")



# Ejercicio 1
print("\n  EJERCICIO 1\n")

grammar1 = {
    'S': [['A', 'uno', 'B', 'C'], ['S', 'dos']],
    'A': [['B', 'C', 'D'], ['A', 'tres'], [EPSILON]],
    'B': [['D', 'cuatro', 'C', 'tres'], [EPSILON]],
    'C': [['cinco', 'D', 'B'], [EPSILON]],
    'D': [['seis'], [EPSILON]]
}

g1 = Grammar(grammar1)
g1.compute_first()
g1.compute_follow('S')
pred1 = g1.compute_prediction()

print_sets("PRIMEROS", g1.first)
print_sets("SIGUIENTES", g1.follow)
print_prediction(pred1)


# Ejercicio 2
print("\n\n  EJERCICIO 2\n")

grammar2 = {
    'S': [['A', 'B', 'uno']],
    'A': [['dos', 'B'], [EPSILON]],
    'B': [['C', 'D'], ['tres'], [EPSILON]],
    'C': [['cuatro', 'A', 'B'], ['cinco']],
    'D': [['seis'], [EPSILON]]
}

g2 = Grammar(grammar2)
g2.compute_first()
g2.compute_follow('S')
pred2 = g2.compute_prediction()

print_sets("PRIMEROS", g2.first)
print_sets("SIGUIENTES", g2.follow)
print_prediction(pred2)