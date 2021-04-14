import json
import pandas as pd
import numpy as np
from Individuo import Individuo

if __name__ == '__main__':

	refeicoes = {"CAFE":["bebidas", "frutas", "carbo1"],
				"LANCHE1":["frutas", "lacteos"],
				"ALMOCO":["carbo2", "graos", "vegetais", "vegetais", "proteinas", "sucos"],
				"LANCHE2":["bebidas", "sucos", "carbo1"],
				"JANTAR":["carbo2", "graos", "vegetais", "proteinas"],
				"CEIA":["frutas", "lacteos"]}

	restricoes = {"Pt": 75, "C": 300, "Df": 25, "Ca": 1000, "Mg": 260,
				"Mn": 2.3, "P": 700, "Fe": 14, "Na": 2400, "Zn": 7}

	dieta_kcal = 1200

	produtos = json.load(open("Dataset/produtos.json", "r"))

	nutrientes_prod = pd.read_csv("Dataset/dataset_formatado.csv")

	print(nutrientes_prod.head())

	indiv = Individuo(refeicoes, produtos, dieta_kcal)

	indiv.calc_fitness(nutrientes_prod, restricoes, penalidade=100)

	print(indiv) 