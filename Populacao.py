from Individuo import Individuo 
import random
import numpy as np

class Populacao:
	def __init__(self, refeicoes, produtos_ids, dieta_kcal, npop=100, taxa_cruzamento=0.9, taxa_mutacao=0.1):
		self.npop = npop
		self.taxa_cruzamento = taxa_cruzamento
		self.individuos = self.__init_pop(refeicoes, produtos_ids, dieta_kcal, taxa_mutacao)

	def __init_pop(self, refeicoes, produtos_ids, dieta_kcal, taxa_mutacao):
		return [Individuo(taxa_mutacao, refeicoes, produtos_ids, dieta_kcal) for _ in range(0, self.npop)]

	def avalia_pop(self, nutrientes_prod, restricoes, penalidade=100):
		for individuo in self.individuos:
			individuo.calc_fitness(nutrientes_prod, restricoes, penalidade)

	def torneio(self, pv=0.9):
		pais = []
		num_pais = 1
		
		while num_pais <= self.npop:
		
			p1 = random.randint(0, self.npop-1)
			p2 = random.randint(0, self.npop-1)
		
			while p1 == p2:
				p2 = random.randint(0, self.npop-1)
		
			if(self.individuos[p2].fitness > self.individuos[p1].fitness):
				vencedor = (self.individuos[p1] if random.random() < pv  else self.individuos[p2])
			else:
				vencedor = (self.individuos[p2] if random.random() < pv else self.individuos[p1])
			
			if len(pais) > 0 and pais[-1] == vencedor: continue
			pais.append(vencedor)
			num_pais += 1

		return pais

	def __gerar_filhos(self, pai1, pai2, index_refeicoes, refeicao_troca):
		individuo = Individuo(init=False, taxa_mutacao=pai1.taxa_mutacao, dieta_kcal=pai1.dieta_kcal)
		if index_refeicoes[refeicao_troca][0] == index_refeicoes[refeicao_troca][1]:
			individuo.id_produtos = [pai2.id_produtos[index_refeicoes[refeicao_troca][0]]]
			individuo.porcoes = [pai2.porcoes[index_refeicoes[refeicao_troca][0]]]
		else: 
			individuo.id_produtos = pai2.id_produtos[index_refeicoes[refeicao_troca][0]:index_refeicoes[refeicao_troca][1]+1]
			individuo.porcoes = pai2.porcoes[index_refeicoes[refeicao_troca][0]:index_refeicoes[refeicao_troca][1]+1]
		
		individuo.id_produtos = pai1.id_produtos[:index_refeicoes[refeicao_troca][0]] + individuo.id_produtos + pai1.id_produtos[index_refeicoes[refeicao_troca][1]+1:]
		individuo.porcoes = pai1.porcoes[:index_refeicoes[refeicao_troca][0]] + individuo.porcoes + pai1.porcoes[index_refeicoes[refeicao_troca][1]+1:]

		return individuo

	def cruzamento(self, pais, refeicoes, produtos_ids):
		index_refeicoes = {"CAFE":(0,2), "LANCHE1":(3,3), "ALMOCO":(4,9), "LANCHE2":(10, 11), "JANTAR":(12, 15), "CEIA":(16,16)}
		refeicoes_aux = list(index_refeicoes.keys())
		indiv_interm = []

		for i in range(0, len(pais), 2):
			if random.random() <= self.taxa_cruzamento:
				refeicao_troca  = random.choice(refeicoes_aux)

				filho1 = self.__gerar_filhos(pais[i], pais[i+1], index_refeicoes, refeicao_troca)
				filho2 = self.__gerar_filhos(pais[i+1], pais[i], index_refeicoes, refeicao_troca)

				filho1.exec_mutacao(refeicoes, produtos_ids)
				filho2.exec_mutacao(refeicoes, produtos_ids)

				indiv_interm.append(filho1)
				indiv_interm.append(filho2)
		
		return indiv_interm

	def get_melhor_indiv(self):
		return min(self.individuos, key=lambda x: x.fitness)

	def substituir_pop(self, indiv_interm):
		indices_disp = list(range(0, self.npop))
		num_indiv = len(indiv_interm)

		for novo_indiv in range(0, num_indiv):
			index = random.choice(indices_disp)
			self.individuos[index] = indiv_interm[novo_indiv]
			indices_disp.remove(index)
		
		indiv_interm.clear()
	
	def exec_elitismo(self, melhor_indiv):
		self.individuos[np.random.randint(0, self.npop)] = melhor_indiv

	def __str__(self):
		return " ".join([str(individuo) for individuo in self.individuos])