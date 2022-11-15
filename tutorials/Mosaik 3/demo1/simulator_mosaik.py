# simulator_mosaik.py
"""
Mosaik interface for the example simulator.

Mosaik 3.0: comentários possuem comaparativo com exemplos do Mosaik 2.0

- adição de tipo 'type'

- adicionado atributo 'self.time' em método __init__()

- adição de parâmetro 'time_resolution' em método init()
    - adição de tratamento do novo parâmetro 'time_resolution'

- adicionado parâmetro 'max_advance' em método step()

- adicionado atributo 'self.time = time' no método step()

- adicionado 'data['time'] = self.time' no método get_data()

"""
import mosaik_api

import example_model


META = {
    'type': 'time-based', ### Mosaik 3.0: tipo 'time-based'
    'models': {
        'ExampleModel': {
            'public': True,
            'params': ['init_val'],
            'attrs': ['delta', 'val'],
        },
    },
}


class ExampleSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        ## self.simulator = simulator.Simulator() ## M2
        self.eid_prefix = 'Model_'
        self.entities = {}  # Maps EIDs to model instances/entities
        self.time = 0 ### Mosaik 3.0:adicionado atributo 'self.time'

    def init(self, sid, time_resolution, eid_prefix=None): ### Mosaik 3.0: ADIÇÃO DO PARÂMETRO 'time_resolution'
        ### Mosaik 3.0: tratamento do novo parâmetro 'time_resolution'
        if float(time_resolution) != 1.:
            raise ValueError('ExampleSim only supports time_resolution=1, but'
                             ' %s was set.' % time_resolution)
        ###

        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model, init_val):
        next_eid = len(self.entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            model_instance = example_model.Model(init_val) ### Mosaik 3.0: exemplo instancia próprio modelo ao invés de criar simulador.
            eid = '%s%d' % (self.eid_prefix, i)
            # self.simulator.add_model(init_val) ## M2: implementação diferente
            self.entities[eid] = model_instance ### Mosaik 3.0: implementação diferente
            entities.append({'eid': eid, 'type': model})

        return entities


    def step(self, time, inputs, max_advance): ### Mosaik 3.0:ADICIONADO PARÂMETRO 'max_advance'
        
        ## M2 #############
        # deltas = {} ## M2
        #for eid, attrs in inputs.items():
        #    for attr, values in attrs.items():
        #        model_idx = self.entities[eid]
        #        new_delta = sum(values.values())
        #        deltas[model_idx] = new_delta

        # Perform simulation step
        # self.simulator.step(deltas)

        # return time + 60  # Step size is 1 minute
        ###################

        self.time = time ### Mosaik 3.0: adicionada especificação do tempo

        # Check for new delta and do step for each model instance:
        for eid, model_instance in self.entities.items():
            if eid in inputs:
                attrs = inputs[eid]
                for attr, values in attrs.items():
                    new_delta = sum(values.values())
                model_instance.delta = new_delta

            model_instance.step()

        return time + 1  # Step size is 1 second

    def get_data(self, outputs):
        # models = self.simulator.models ## M2
        data = {}
        for eid, attrs in outputs.items():
            # model_idx = self.entities[eid] ## M2
            model = self.entities[eid]
            data['time'] = self.time # Mosaik 3.0
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta['models']['ExampleModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)

                # Get model.val or model.delta:
                data[eid][attr] = getattr(model, attr)

        return data


def main():
    return mosaik_api.start_simulation(ExampleSim())


if __name__ == '__main__':
    main()
