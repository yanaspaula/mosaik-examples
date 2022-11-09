# simulator_mosaik.py
"""
Componente de interface (Sim API) do Mosaik.
É aqui onde os métodos de comunicação do Mosaik são definidos para o modelo.

Para uma explicação detalhada dos métodos do Sim API, acesse: https://mosaik.readthedocs.io/en/latest/mosaik-api/low-level.html?highlight=init()#api-calls

"""
import mosaik_api       # Sim API de alto-nível
import example_model    # Modelo a ser integrado

META = {
    'api_version': '3.0.2',             # Versão utilizada do Mosaik
    'type': 'time-based',               # Como o simulador é avançado no tempo
    'models': {                         # Modelos definidos nesse arquivo
        'ExampleModel': {
            'public': True,             # Define se um modelo pode ser instanciado pelo usuário ou não
            'params': ['init_val'],     # Parâmetros que podem ser passados ao modelo em sua criação
            'attrs': ['delta', 'val'],  # Atributos que podem ser acessados no modelo (leitura ou escrita) 
            # 'any_inputs': True|False, # Se {True}, qualquer atributo pode ser associado a esse modelo
            # 'trigger': ['attr_1', ...]
        },
    },
    # 'extra_methods': [                # Lista opcional de métodos que o simulador pode prober em adição às chamadas API padrão
    #     'method_example_1',
    # ]
}


class ExampleSim(mosaik_api.Simulator): # Herda classe abstrata do API de alto-nível
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Model_'
        self.entities = {}  # Mapeia EIDs (identificação das entidades) às intâncias/entidades
        self.time = 0 

    """ 
        Inicia a troca de comunicação entre o simulador e o Mosaik.    
    """
    def init(self, sid, time_resolution, eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError('ExampleSim only supports time_resolution=1, but'
                             ' %s was set.' % time_resolution)
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    """ 
        Cria instâncias de um simulador.    
    """
    def create(self, num, model, init_val):
        next_eid = len(self.entities)
        entities = []
        for i in range(next_eid, next_eid + num):
            model_instance = example_model.Model(init_val) 
            eid = '%s%d' % (self.eid_prefix, i)
            self.entities[eid] = model_instance 
            entities.append({'eid': eid, 'type': model})
        return entities

    """ 
        Marca um processo de simulação (definido pelo tempo de um simulador) no Mosaik. 
        É neste método que cálculos, funções ou outras ações do simulador são definidas e executadas.    
    """
    def step(self, time, inputs, max_advance): 
        self.time = time

        # Check for new delta and do step for each model instance:
        for eid, model_instance in self.entities.items():
            if eid in inputs:
                attrs = inputs[eid]
                for attr, values in attrs.items():
                    new_delta = sum(values.values())
                model_instance.delta = new_delta
            model_instance.step()
        return time + 1  # Step size is 1 second

    """ 
        Este método pode ser usado pelo Mosaik para acessar dados de um simulador e disponibilizá-los 
        para outros simuladores.
    """
    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            model = self.entities[eid]
            data['time'] = self.time 
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
