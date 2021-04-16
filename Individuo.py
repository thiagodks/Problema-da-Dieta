import numpy as np
import random

INTERVALO_PORCOES = (0.5, 3)
MAX = 9999999999

class Individuo:
	def __init__(self, taxa_mutacao=0.1, refeicoes=None, produtos_ids=None, dieta_kcal=None, init=True):
		self.porcoes = []
		self.id_produtos = []
		self.fitness = MAX
		self.kcal = MAX
		self.dieta_kcal = dieta_kcal
		self.taxa_mutacao = taxa_mutacao
		if init: self.__init_indiv(refeicoes, produtos_ids)

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
	
	def exec_mutacao(self, refeicoes, produtos_ids):
		
		index = 0
		for refeicao, produtos in refeicoes.items():
			
			if refeicao == "LANCHE1":
				produtos = [produtos[random.randint(0,1)]]
			elif refeicao == "LANCHE2":
				produtos = [produtos[random.randint(0,1)], produtos[2]]
			elif refeicao == "CEIA":
				produtos = [produtos[random.randint(0,1)]]
			
			for produto in produtos:
				if random.random() < self.taxa_mutacao:
					self.id_produtos[index] = random.choice(produtos_ids[produto])
					self.porcoes[index] = random.uniform(INTERVALO_PORCOES[0], INTERVALO_PORCOES[1])
				index += 1

	def calc_fitness(self, nutrientes_prod, restricoes, penalidade):
		self.fitness = self.__func_objetivo(self.__calc_kcal(nutrientes_prod), nutrientes_prod, restricoes, penalidade)

	def valida(self, nutrientes_prod, restricoes):
		return not self.__check_nutrientes(self.get_nutrientes(nutrientes_prod), restricoes)
	
	def __func_objetivo(self, kcal, nutrientes_prod, restricoes, penalidade):
		penalizacao = self.__check_nutrientes(self.get_nutrientes(nutrientes_prod), restricoes)
		value = 0
		# print("penalizacao?:", penalizacao, end="\r")
		
		if not penalizacao:
			value = self.dieta_kcal
			somatorio = 0
			for index, idp in enumerate(self.id_produtos):
				nutrientes = nutrientes_prod[idp]
				# nutrientes = nutrientes_prod.loc[nutrientes_prod['id'] == idp]
				kcal = float(nutrientes["kcal"])
				# print(nutrientes, kcal, self.porcoes[index])
				# input("")
				somatorio += kcal * self.porcoes[index]
			return np.abs(value - somatorio)
		
		else:
			for nutriente, restricao in restricoes.items():
				for index, idp in enumerate(self.id_produtos):
					nutrientes = nutrientes_prod[idp]
					# nutrientes = nutrientes_prod.loc[nutrientes_prod['id'] == idp]
					value += np.abs((float(nutrientes[nutriente]) * self.porcoes[index]) - restricao)
				value /= restricao
			return np.abs(kcal - self.dieta_kcal) + (value * penalidade)
		
		return None

	def __calc_kcal(self, nutrientes_prod):
		self.kcal = 0
		for idp in self.id_produtos:
			nutrientes = nutrientes_prod[idp]
			# nutrientes = nutrientes_prod.loc[nutrientes_prod['id'] == idp]
			self.kcal += float(nutrientes["kcal"])
		return self.kcal

	def get_nutrientes(self, nutrientes_prod):
		nutrientes_indiv = {"Pt": 0, "C": 0, "Df": 0, "Ca": 0, "Mg": 0,
					  "Mn": 0, "P": 0, "Fe": 0, "Na": 0, "Zn": 0}
		
		for nt in nutrientes_indiv.keys():
			for index, idp in enumerate(self.id_produtos):
				nutrientes = nutrientes_prod[idp]
				# nutrientes = nutrientes_prod.loc[nutrientes_prod['id'] == idp]
				nutrientes_indiv[nt] += float(nutrientes[nt]) * self.porcoes[index]
		
		# print(nutrientes_indiv)
		return nutrientes_indiv

	def __check_nutrientes(self, nutrientes_indiv, restricoes, check_Na=False):
		for nt, restricao in restricoes.items():
			if nt == "Na" and nutrientes_indiv[nt] > restricao:
				return True
			if nt != "Na" and nutrientes_indiv[nt] < restricao: 
				return True
		return False

	
	def __str__(self):
		print("\n-> Id (Porção): ", end="[")
		
		for i, idp in enumerate(self.id_produtos):
			print("i:",i,"-",idp, end="#")
			# if i != len(self.id_produtos)-1: print("i:",i," ",idp, "-> (%.1f)" % self.porcoes[i], end=", ")
			# else: print(idp, "(%.1f)" % self.porcoes[i], end="")
		return "\n"
		# return "]\n" + ("-> Kcal: %.2f" % self.kcal) + ("\n-> Fitness: %.2f" % self.fitness) + "\n"		
		# return ("\n-> Kcal: %.2f" % self.kcal) + ("\n-> Fitness: %.2f" % self.fitness) + "\n"		
