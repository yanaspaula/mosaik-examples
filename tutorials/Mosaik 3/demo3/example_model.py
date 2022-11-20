# example_model.py
"""
Possui o modelo do tutorial.

"""

class Model:
    """Modelo simples que adiciona o valor *val* a um valor *delta* a cada passo de execução.

    Opcionalmente, é possível setar um valor inicial *init_val*. Por padrão, ele é identificado como 0.

    """
    def __init__(self, init_val=0):
        self.val = init_val
        self.delta = 1

    def step(self):
        """Adiciona *delta* a *val* em um passo de execução."""
        self.val += self.delta
