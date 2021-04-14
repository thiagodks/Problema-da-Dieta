import random
import json
import pandas as pd
import numpy as np

INTERVALO_PORCOES = (0.5, 3)

class Individuo:
	def __init__(self, refeicoes, produtos, dieta_kcal):
		self.porcoes = []
		self.id_produtos = []
		self.fitness = None
		self.kcal = None
		self.dieta_kcal = dieta_kcal
		self.__init_indiv(refeicoes, produtos)

	def __init_indiv(self, refeicoes, produtos_ids):

		for refeicao, produtos in refeicoes.items():
			
			if refeicao == "LANCHE1":
				produtos = [produtos[random.randint(0,1)]]
			elif refeicao == "LANCHE2":
				produtos = [produtos[random.randint(0,1)], produtos[2]]
			elif refeicao == "CEIA":
				produtos = [produtos[random.randint(0,1)]]
			
			for produto in produtos:
				self.id_produtos.append(random.choice(produtos_ids[produto]))
				self.porcoes.append(random.uniform(INTERVALO_PORCOES[0], INTERVALO_PORCOES[1]))
	
	def calc_fitness(self, nutrientes_prod, restricoes, penalidade):
		self.fitness = self.__func_objetivo(self.__calc_kcal(nutrientes_prod), nutrientes_prod, restricoes, penalidade)

	def __calc_kcal(self, nutrientes_prod):
		self.kcal = 0
		for idp in self.id_produtos:
			nutrientes = nutrientes_prod.loc[nutrientes_prod['id'] == idp]
			self.kcal += (float(nutrientes["C"]) * 4) + (float(nutrientes["Pt"]) * 4)
		return self.kcal

	def __func_objetivo(self, kcal, nutrientes_prod, restricoes, penalidade):
		value = 0
		for nutriente, restricao in restricoes.items():
			for index, idp in enumerate(self.id_produtos):
				nutrientes = nutrientes_prod.loc[nutrientes_prod['id'] == idp]
				value += np.abs((float(nutrientes[nutriente]) * self.porcoes[index]) - restricao)
			value /= restricao
		
		return np.abs(kcal - self.dieta_kcal) + (value * penalidade)
	
	def __str__(self):
		print("\n-> Id (Porção): ", end="[")
		
		for i, idp in enumerate(self.id_produtos):
			if i != len(self.id_produtos)-1: print(idp, "-> (%.1f)" % self.porcoes[i], end=", ")
			else: print(idp, "(%.1f)" % self.porcoes[i], end="")
		
		return "]\n" + ("-> Kcal: %.2f" % self.kcal) + ("\n-> Fitness: %.2f" % self.fitness) + "\n"		
