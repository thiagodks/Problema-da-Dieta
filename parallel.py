from concurrent.futures import ProcessPoolExecutor
from main import gen_log, pd_to_dict
from Individuo import Individuo
from Populacao import Populacao
from termcolor import colored
import multiprocessing
from tqdm import tqdm
import numpy as np
import itertools
import pickle
import __io

def run(parametros):

	prmt = {"npop": parametros[0],
			"nger": parametros[1],
			"tc": parametros[2], 
			"tm": parametros[3],
	}    
	melhores_solucoes = []
	for _ in range(0, 10):

		populacao = Populacao(refeicoes, produtos_ids, dieta_kcal, prmt["npop"], prmt["tc"], prmt["tm"])
	
		for _ in range(0, prmt["nger"]):
			populacao.avalia_pop(nutrientes_prod_dict, restricoes, penalidade=1000)
			melhor_indiv = populacao.get_melhor_indiv() 
			pais = populacao.torneio()
			indiv_interm = populacao.cruzamento(pais, refeicoes, produtos_ids)
			populacao.substituir_pop(indiv_interm)
			populacao.exec_elitismo(melhor_indiv)

		melhores_solucoes.append(melhor_indiv)
	return melhores_solucoes, prmt

dieta_kcal = 1200

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

NPOP = [10, 50, 100]
NGER = [25, 50, 100]
TC = [0.4, 0.6, 0.8]
TM = [0.1, 0.2, 0.4]

all_list = [NPOP, NGER, TC, TM]
parametros = list(itertools.product(*all_list)) 

executor = ProcessPoolExecutor()
num_args = len(parametros)
chunksize = int(num_args/multiprocessing.cpu_count())
results = [i for i in tqdm(executor.map(run, parametros),total=num_args)]

pickle.dump(results, open("Resultados_fatorial/results_"+str(len(parametros))+".pickle", 'wb'))