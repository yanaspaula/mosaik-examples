# random_simulator.py
"""
  Este código apresenta um resumo de todos os elementos necessários para realizar 
  uma integração entre um simulador e o Mosaik.  
 
"""

import random
import mosaik_api   # 0. TIPO DO SIM API

"""
  1. METADDOS DO SIMULADOR
  
"""
META = {  # Possui informações que definem o simulador para o Mosaik
	'models': {
		'RandomModel': { 
			'public': True,
			'params': [],
			'attrs': ['val'],
		}
	}
}

"""
	2. MODELO
  
"""
class Model:
	def __init__(self):
		self.val = random.random()  # Este modelo cria valores randômicos
	
	def step(self):
		self.val += random.random()  # A cada passo, ele soma um novo valor randômico ao valor inicial

"""
	3. SIMULADOR
  
"""
class Simulator(object): # Serve como classe integradora para instanciar o modelo
	def __init__(self):
		self.models = []
		self.data = []

	def add_model(self):
		model = Model()   # Instancia os modelos
		self.models.append(model)
		self.data.append([])

	def step(self): 
		for i, model in enumerate(self.models):
			model.step()
			self.data[i].append(model.val) # adiniona o valor de *val* ao modelo *model* no atributo *data* do objeto *Simulator*

"""
	4. INTERFACE DE COMUNICAÇÃO (SIM API)
  
"""
class RandomSim(mosaik_api.Simulator):  # Herda classe abstrata de alto-nível do Mosaik
	def __init__(self): # Inicializa o simulador criado
		super().__init__(META)
		self.simulator = Simulator()
		self.eid_prefix = 'RanModel'
		self.entities = {}

	def init(self, sid, eid_prefix = None): # Inicialização enviada ao Mosaik (metadados do simulador)
		if eid_prefix is not None:
			self.eid_prefix = eid_prefix
		return self.meta

	def create(self, num, model): # Inicializa *num* instâncias do modelo *model* para o API do Mosaik
		next_eid = len(self.entities)
		entities = []

		for i in range(next_eid, next_eid + num):
			eid = "%s%d" % (self.eid_prefix, i)
			self.simulator.add_model()
			self.entities[eid] = i
			entities.append({"eid": eid, "type": model})
		return entities

	def step(self, time, inputs): # Obtém dados para o Mosaik
		for eid, attrs in inputs.items():
			for attr, values in attrs.items():
				model_idx = self.entities[eid]

		self.simulator.step()
		return time + 60 # Tamanho do passo (step) é  de um minuto

	def get_data(self, outputs): # Permite que outros simuladores obtenham informação do ```Model``
		models = self.simulator.models
		data = {}
		for eid, attrs in outputs.items():
			model_idx = self.entities[eid]
			data[eid] = {}
			for attr in attrs:
				if attr not in self.meta['models']['RandomModel']['attrs']:
					raise ValueError("Unknown output attribute: %s" % attr)

				data[eid][attr] = getattr(models[model_idx], attr)
		return data


#	Exemplo de execução do simulador.

#if __name__ == '__main__':	
# 	sim = Simulator()
#
# 	# Adiciona *2* modelos no simulador
# 	for i in range(2):
# 		sim.add_model()
#	
# 	sim.add_model()
# 	sim.step()
#
# 	print("Valores randômicos no Modelo:")
# 	for i, inst in enumerate(sim.data):
# 		print("%d: %s" % (i, inst))
