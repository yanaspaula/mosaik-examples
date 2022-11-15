"""
A simple data collector that prints all data when the simulation finishes.

"""
import collections

import mosaik_api


META = {
    'type': 'event-based', # Mosaik 3.0: adicionado tipo de simulador
    'models': {
        'Monitor': {
            'public': True,
            'any_inputs': True,
            'params': [],
            'attrs': [],
        },
    },
}


class Collector(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda:
                                            collections.defaultdict(dict))
        #self.step_size = None # Mosaik 2.0

    # def init(self, sid, step_size): # Mosaik 2.0: retirado step_size
    def init(self, sid, time_resolution): # Mosaik 3.0: adicionado 'time_resolution' no método init()
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError('Can only create one instance of Monitor.')

        self.eid = 'Monitor'
        return [{'eid': self.eid, 'type': model}]

    def step(self, time, inputs, max_advance): # Mosaik 3.0: adicionado 'max_advance' no método setp()
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                self.data[src][attr][time] = value

        # return time + self.step_size # Mosaik 2.0: método step() retorna 'step_size' de simulador
        return None # Mosaik 3.0: não há necessidade de retornar 'step_size' no método step()

    def finalize(self):
        print('Collected data:')
        for sim, sim_data in sorted(self.data.items()):
            print('- %s:' % sim)
            for attr, values in sorted(sim_data.items()):
                print('  - %s: %s' % (attr, values))


if __name__ == '__main__':
    mosaik_api.start_simulation(Collector())