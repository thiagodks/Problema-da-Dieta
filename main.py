import numpy as np
from Individuo import Individuo
from Populacao import Populacao
import __io
import plot_charts as pc
from tqdm import tqdm

def gen_log(populacao):
	melhor_indiv = populacao.get_melhor_indiv()
	fitness_pop = [i.fitness for i in populacao.individuos]
	return melhor_indiv, np.mean(fitness_pop), np.median(fitness_pop), np.std(fitness_pop)

def pd_to_dict(nutrientes_prod):
	nutrientes_prod_dict = {}
	for _, row in nutrientes_prod.iterrows():
		nutrientes_prod_dict[int(row["id"])] = row
	return nutrientes_prod_dict

if __name__ == '__main__':

	print()
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

	produtos_ids = __io.load_products("Dataset/produtos.json")
	nutrientes_prod = __io.load_data("Dataset/dataset_formatado.csv")
	nutrientes_prod_dict = pd_to_dict(nutrientes_prod)

	populacao = Populacao(refeicoes, produtos_ids, dieta_kcal, npop, taxa_cruzamento, taxa_mutacao)
	log_pop = []

	for ger_i in range(0, nger):
		populacao.avalia_pop(nutrientes_prod_dict, restricoes, penalidade=1000)

		log_pop.append(gen_log(populacao))
		# print("fitness mediana:", np.median([i.fitness for i in populacao.individuos]))
		# input("")

		melhor_indiv = populacao.get_melhor_indiv() 
		pais = populacao.torneio()
		indiv_interm = populacao.cruzamento(pais, refeicoes, produtos_ids)
		populacao.substituir_pop(indiv_interm)
		populacao.exec_elitismo(melhor_indiv)
		print("=> Geração: "+str(ger_i+1)+"/"+str(nger)+" -> Melhor solução encontrada até o momento: %.2f" % 
			  melhor_indiv.fitness, melhor_indiv.valida(nutrientes_prod_dict, restricoes), end="    \r")
	
	print("\n\nRestrições:", restricoes)
	print("\nDieta:", populacao.get_melhor_indiv().get_nutrientes(nutrientes_prod_dict), "\n")
	print("\nFitness: %.2f" % populacao.get_melhor_indiv().fitness, " - Kcal: %.2f" % populacao.get_melhor_indiv().kcal)
	print(populacao.get_melhor_indiv().id_produtos, len(populacao.get_melhor_indiv().id_produtos))
	print(populacao.get_melhor_indiv().porcoes, len(populacao.get_melhor_indiv().porcoes))
	pc.plot_graphics(log_pop, parametros)