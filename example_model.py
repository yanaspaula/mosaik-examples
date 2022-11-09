# example_model.py
"""
Esse arquivo possui um exemplo de um modelo simples.

O modelo incrementa seu valor *val* com um valor *delta* a cada passo.
Opcionalmente, você pode definir o valor inicial no parâmetro *init_val*,
Por padrão, *init_val* é definido como 0.

"""

class Model:
    def __init__(self, init_val=0):
        self.val = init_val
        self.delta = 1

    def step(self):
        """Performa um passo de simulação (step) adicionando *delta* a *val*."""
        self.val += self.delta