# controller_master.py
"""
Controlador-mestre utilizando same-time loop.

Calcula a soma dos valores de *delta* dos controladores e verifica se
está no limite (-1, 1). Caso não esteja, seta todos os *delta* para 0.
"""
import mosaik_api

META = {
    'type': 'event-based',      # Necessário para same-time loop
    'models': {
        'Agent': {
            'public': True,
            'params': [],
            'attrs': ['delta_in', 'delta_out'],
        },
    },
}

class Controller(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.agents = []
        self.data = {}
        self.cache = {} # Utiliza cache para armazenar valores de *delta* anteriores
        self.time = 0

    def create(self, num, model):
        n_agents = len(self.agents)
        entities = []
        for i in range(n_agents, n_agents + num):
            eid = 'Agent_%d' % i
            self.agents.append(eid)
            entities.append({'eid': eid, 'type': model})

        return entities

    def step(self, time, inputs, max_advance):
        print('[controller_master] max_advance: {}'.format(max_advance))
        self.time = time
        data = {}
        for agent_eid, attrs in inputs.items():
            values_dict = attrs.get('delta_in', {})
            for key, value in values_dict.items():
                self.cache[key] = value
        
        if sum(self.cache.values()) < -1:
            data[agent_eid] = {'delta_out': 0}   # Seta *delta* a ser recebido pelos controladores

        self.data = data

        return None

    def get_data(self, outputs):
        data = {}
        for agent_eid, attrs in outputs.items():
            for attr in attrs:
                if attr != 'delta_out':
                    raise ValueError('Unknown output attribute "%s"' % attr)
                if agent_eid in self.data:
                    data['time'] = self.time    # Necessário para same-time loop
                    data.setdefault(agent_eid, {})[attr] = self.data[agent_eid][attr]

        return data


def main():
    return mosaik_api.start_simulation(Controller())


if __name__ == '__main__':
    main()