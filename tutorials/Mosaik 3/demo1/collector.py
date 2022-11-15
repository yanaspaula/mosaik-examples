"""
A simple data collector that prints all data when the simulation finishes.

Mosaik 3.0: comentários possuem comaarativo com exemplos do Mosaik 2.0

- adicionado tipo de simulador 'type'

- retirado atributo 'step_size' no método __init__()

- adicionado atributo 'time_resolution' em método init()

- adicionado parâmetro 'max_advance' em método step()

"""
import collections

import mosaik_api


META = {
    'type': 'event-based', # Mosaik 3.0: TIPO EVENT-BASED
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
        # self.step_size = None ## M2

        # Mosaik 3.0: NÃO HÁ ATRIBUTO 'step_size' NO MÉTODO __init__

    def init(self, sid, time_resolution): # Mosaik 3.0: ADIÇÃO DE PARÂMETRO 'time_resolution' + RETIRADO PARÂMETRO 'step_size'
        # Mosaik 3.0: NÃO HÁ ATRIBUTO 'step_size'
        # self.step_size = step_size ## M2 
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError('Can only create one instance of Monitor.')

        self.eid = 'Monitor'
        return [{'eid': self.eid, 'type': model}]

    def step(self, time, inputs, max_advance): # Mosaik 3.0: ADIÇÃO DO PARÂMETRO 'max_advance'
        # data = inputs[self.eid] ## M2
        data = inputs.get(self.eid, {}) # Mosaik 3.0: utilização do método get()
        for attr, values in data.items():
            for src, value in values.items():
                # self.data[src][attr].append(value) ## M2
                self.data[src][attr][time] = value # Mosaik 3.0: retirado método append()

        # return time + self.step_size ## M2
        return None # Mosaik 3.0: NÃO HÁ MAIS RETORNO DE 'time + step_size'

    def finalize(self):
        print('Collected data:')
        for sim, sim_data in sorted(self.data.items()):
            print('- %s:' % sim)
            for attr, values in sorted(sim_data.items()):
                print('  - %s: %s' % (attr, values))


if __name__ == '__main__':
    mosaik_api.start_simulation(Collector())