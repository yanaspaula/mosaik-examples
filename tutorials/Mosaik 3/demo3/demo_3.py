# demo_3.py
import mosaik
import mosaik.util

# Configuração do cenário
SIM_CONFIG = {
    'ExampleSim': {
        'python': 'simulator_mosaik:ExampleSim',
    },
    'ExampleCtrl': {
        'python': 'controller_demo_3:Controller',
    },
    'ExampleMasterCtrl': {
        'python': 'controller_master:Controller',
    },
    'Collector': {
        'cmd': '%(python)s collector.py %(addr)s',
    },
}
END = 6  # 10 seconds - valor do max_advance

# Criação do mundo
world = mosaik.World(SIM_CONFIG)

# Inicialização dos simuladores
examplesim = world.start('ExampleSim', eid_prefix='Model_')
examplectrl = world.start('ExampleCtrl')
examplemasterctrl = world.start('ExampleMasterCtrl')
collector = world.start('Collector')

# Criação das instâncias dos simuladores
models = [examplesim.ExampleModel(init_val=i) for i in (-2, 0, -2)]
agents = examplectrl.Agent.create(len(models))
master_agent = examplemasterctrl.Agent.create(1)
monitor = collector.Monitor()

# Conexão das entidades
for model, agent in zip(models, agents):
    world.connect(model, agent, ('val', 'val_in'))
    world.connect(agent, model, 'delta', weak=True)

for agent in agents:
    world.connect(agent, master_agent[0], ('delta', 'delta_in'))
    world.connect(master_agent[0], agent, ('delta_out', 'delta'), weak=True) # Necessário para same-time-loops

mosaik.util.connect_many_to_one(world, models, monitor, 'val', 'delta')
mosaik.util.connect_many_to_one(world, agents, monitor, 'delta')
world.connect(master_agent[0], monitor, 'delta_out')

print('----- Parâmetro max_advance -----')
# Execução da simulação
world.run(until=END)