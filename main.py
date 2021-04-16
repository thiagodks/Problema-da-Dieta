import json
import pandas as pd
import numpy as np
from Individuo import Individuo
from Populacao import Populacao
import __io
import plot_charts as pc

def gen_log(populacao):

	melhor_indiv = populacao.get_melhor_indiv()
	fitness_pop = [i.fitness for i in populacao.individuos]
	media_fit = np.mean(fitness_pop)
	mediana_fit = np.median(fitness_pop)
	std_fit = np.std(fitness_pop)

	# print(melhor_indiv.fitness, media_fit, mediana_fit, std_fit)
	# input("")
	return melhor_indiv, media_fit, mediana_fit, std_fit

if __name__ == '__main__':

	args = __io.get_args()

	dieta_kcal = int(args["dk"])
	npop = int(args["np"])
	nger = int(args["ng"])
	taxa_cruzamento = float(args["tc"])
	taxa_mutacao = float(args["tm"])

	parametros = {
		"dieta_kcal": dieta_kcal,
		"npop": npop,
		"nger": nger,
		"taxa_cruzamento": taxa_cruzamento,
		"taxa_mutacao": taxa_mutacao
	}

	refeicoes = {"CAFE":["bebidas", "frutas", "carbo1"],
				"LANCHE1":["frutas", "lacteos"],
				"ALMOCO":["carbo2", "graos", "vegetais", "vegetais", "proteinas", "sucos"],
				"LANCHE2":["bebidas", "sucos", "carbo1"],
				"JANTAR":["carbo2", "graos", "vegetais", "proteinas"],
				"CEIA":["frutas", "lacteos"]}

	restricoes = {"Pt": 75, "C": 300, "Df": 25, "Ca": 1000, "Mg": 260,
				"Mn": 2.3, "P": 700, "Fe": 14, "Na": 2400, "Zn": 7}


	produtos_ids = json.load(open("Dataset/produtos.json", "r"))
	nutrientes_prod = pd.read_csv("Dataset/dataset_formatado.csv")
	nutrientes_prod_dict = {}
	for index, row in nutrientes_prod.iterrows():
		nutrientes_prod_dict[int(row["id"])] = row
	
	populacao = Populacao(refeicoes, produtos_ids, dieta_kcal, npop, taxa_cruzamento, taxa_mutacao)
	log_pop = []

	for ger_i in range(0, nger):
		populacao.avalia_pop(nutrientes_prod_dict, restricoes, penalidade=100)

		log_pop.append(gen_log(populacao))
		# print("fitness mediana:", np.median([i.fitness for i in populacao.individuos]))
		# input("")

		melhor_indiv = populacao.get_melhor_indiv() 
		pais = populacao.torneio()
		indiv_interm = populacao.cruzamento(pais, refeicoes, produtos_ids)
		populacao.substituir_pop(indiv_interm)
		populacao.exec_elitismo(melhor_indiv)
		print("(",ger_i, ") Melhor solução encontrada até o momento: %.2f" % 
			  melhor_indiv.fitness, melhor_indiv.valida(nutrientes_prod_dict, restricoes), end="\r")

	
	print()
	pc.plot_graphics(log_pop, parametros)