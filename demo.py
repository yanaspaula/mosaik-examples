# demo.py
'''
Representa o Scenario API do Mosaik.

'''
import mosaik
import mosaik.util

"""
    CONFIGURAÇÃO DOS MODELOS
"""
SIM_CONFIG = {  # Determina os modelos utilizados no cenário
    'ExampleSim': {
        'python': 'simulator_mosaik:ExampleSim',
    },
    'Collector': {
        'cmd': '%(python)s collector.py %(addr)s',
    },
}
END = 10  # 10 seconds

"""
    CRIAÇÃO DO MUNDO
"""
world = mosaik.World(SIM_CONFIG)

"""
    INICIALIZAÇÃO DOS MODELOS
"""
examplesim = world.start('ExampleSim', eid_prefix='Model_')
collector = world.start('Collector')

"""
    CRIAÇÃO DAS INSTÂNCIAS
"""
model = examplesim.ExampleModel(init_val=2)
monitor = collector.Monitor()

"""
    CONEXÃO DAS ENTIDADES
"""
world.connect(model, monitor, 'val', 'delta')
more_models = examplesim.ExampleModel.create(2, init_val=3)
mosaik.util.connect_many_to_one(world, more_models, monitor, 'val', 'delta')

"""
    EXECUÇÃO DA SIMULAÇÃO
"""
world.run(until=END)