# controller.py
"""
A simple demo controller.

"""
import mosaik_api


META = {
    'type': 'event-based', # Mosaik 3.0
    'models': {
        'Agent': {
            'public': True,
            'params': [],
            'attrs': ['val_in', 'delta'],
        },
    },
}


class Controller(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.agents = []
        self.data = {} # Mosaik 3.0: identificação do dicionário de dados no método __init__()
        self.time = 0 # Mosaik 3.0: tempo inicializado em 0

    def create(self, num, model):
        n_agents = len(self.agents)
        entities = []
        for i in range(n_agents, n_agents + num):
            eid = 'Agent_%d' % i
            self.agents.append(eid)
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs, max_advance): # Mosaik 3.0: adição do parâmetro 'max_advance' no método step()
        self.time = time # Mosaik 3.0: especiicação do atributo 'self.time = time'
        data = {}
        for agent_eid, attrs in inputs.items():
            delta_dict = attrs.get('delta', {})
            if len(delta_dict) > 0:
                data[agent_eid] = {'delta': list(delta_dict.values())[0]}
                continue

            values_dict = attrs.get('val_in', {})
            if len(values_dict) != 1:
                raise RuntimeError('Only one ingoing connection allowed per '
                                   'agent, but "%s" has %i.'
                                   % (agent_eid, len(values_dict)))
            value = list(values_dict.values())[0]

            if value >= 3:
                delta = -1
            elif value <= -3:
                delta = 1
            else:
                continue

            data[agent_eid] = {'delta': delta}

        self.data = data

        return None

    def get_data(self, outputs):
        data = {}
        for agent_eid, attrs in outputs.items():
            for attr in attrs:
                if attr != 'delta':
                    raise ValueError('Unknown output attribute "%s"' % attr)
                if agent_eid in self.data:
                    data['time'] = self.time
                    data.setdefault(agent_eid, {})[attr] = self.data[agent_eid][attr]

        return data


def main():
    return mosaik_api.start_simulation(Controller())


if __name__ == '__main__':
    main()