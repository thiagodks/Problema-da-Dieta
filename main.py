import json
import pandas as pd
import numpy as np
from Individuo import Individuo
from Populacao import Populacao
import __io

if __name__ == '__main__':

	args = __io.get_args()

	refeicoes = {"CAFE":["bebidas", "frutas", "carbo1"],
				"LANCHE1":["frutas", "lacteos"],
				"ALMOCO":["carbo2", "graos", "vegetais", "vegetais", "proteinas", "sucos"],
				"LANCHE2":["bebidas", "sucos", "carbo1"],
				"JANTAR":["carbo2", "graos", "vegetais", "proteinas"],
				"CEIA":["frutas", "lacteos"]}

	restricoes = {"Pt": 75, "C": 300, "Df": 25, "Ca": 1000, "Mg": 260,
				"Mn": 2.3, "P": 700, "Fe": 14, "Na": 2400, "Zn": 7}

	dieta_kcal = int(args["dk"])
	npop = int(args["np"])
	nger = int(args["ng"])
	taxa_cruzamento = float(args["tc"])
	taxa_mutacao = float(args["tm"])

	produtos_ids = json.load(open("Dataset/produtos.json", "r"))
	nutrientes_prod = pd.read_csv("Dataset/dataset_formatado.csv")

	populacao = Populacao(refeicoes, produtos_ids, dieta_kcal, npop, taxa_cruzamento, taxa_mutacao)

	for ger_i in range(0, nger):
		populacao.avalia_pop(nutrientes_prod, restricoes, penalidade=1000)
		# print(populacao)
		pais = populacao.torneio()
		indiv_interm = populacao.cruzamento(pais, refeicoes, produtos_ids)
		# print("pais:", len(pais))
		break

	# indiv = Individuo(refeicoes, produtos, dieta_kcal)

	# indiv.calc_fitness(nutrientes_prod, restricoes, penalidade=100)