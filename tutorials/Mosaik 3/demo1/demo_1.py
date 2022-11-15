# demo_1.py
'''
Diferenças com Mosasik2:

- world.start() do collector não possui mais 'step_size'

'''
import mosaik
import mosaik.util

# Sim config. and other parameters
SIM_CONFIG = {
    'ExampleSim': {
        'python': 'simulator_mosaik:ExampleSim',
    },
    'Collector': {
        'cmd': '%(python)s collector.py %(addr)s',
    },
}
END = 10  # 10 seconds

# Create World
world = mosaik.World(SIM_CONFIG)

# Start simulators
examplesim = world.start('ExampleSim', eid_prefix='Model_') # examplesim = world.start('ExampleSim')
## collector = world.start('Collector', step_size=60) ## M2
collector = world.start('Collector') ### Mosaik 3.0: retirado 'step_size'

# Instantiate models
model = examplesim.ExampleModel(init_val=2)
monitor = collector.Monitor()

# Connect entities
world.connect(model, monitor, 'val', 'delta')

# Create more entities
more_models = examplesim.ExampleModel.create(2, init_val=3)
mosaik.util.connect_many_to_one(world, more_models, monitor, 'val', 'delta')

# Run simulation
world.run(until=END)