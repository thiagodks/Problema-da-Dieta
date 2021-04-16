import matplotlib.pyplot as plt
from termcolor import colored
import pandas as pd
import numpy as np
import argparse
import pickle

def get_fitness(fitness):
	x1 = str(fitness)
	if x1.find("e") == -1: 
		return ("%.6f" % fitness)
	x2 = x1[:6]
	x2 += x1[x1.find("e"):]
	return x2

def dict_to_str(dicionario):
	return "||".join([str(i[0]) + ":" + str(i[1]) for i in list(dicionario.items())])

def plot_graphics(log_pop, args, name=""):

	log_pop = list(map(list, zip(*log_pop)))
	p_best, mean_fitness, median_fitness = log_pop[0], log_pop[1], log_pop[2]
	p_best = [p.fitness for p in p_best]

	fig, (ax1, ax2) = plt.subplots(1,2)
	fig.set_size_inches(20, 7)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(top=0.80)
	
	itr = len(p_best)
	ax1.set_title("Fitness a cada Iteração")
	ax1.set_xlabel("Gerações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, itr)), p_best, 'g--', label='Melhor Fitness: %.2f' % (p_best[-1]))
	ax1.legend(ncol=1)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness")
	ax2.set_xlabel("Gerações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')
	ax2.plot(list(range(0, itr)), p_best, 'g--', label='Melhor Fitness: %.2f' % (p_best[-1]))
	ax2.plot(list(range(0, itr)), mean_fitness, 'b--', label='Media: %.2f' % (mean_fitness[-1]))
	ax2.plot(list(range(0, itr)), median_fitness, 'y--', label='Mediana: %.2f' % (median_fitness[-1]))
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	print(colored("\033[1m"+"-> Gráfico salvo em: ", "green"), 'Graficos/'+name+"||"+dict_to_str(args)+'||.png')
	fig.savefig('Graficos/'+name+"||"+dict_to_str(args)+'||.png', bbox_inches='tight')

def plot_table(results):

	table = {"$\\bf{NPOP}$": [],
			"$\\bf{NGER}$": [],
			"$\\bf{TC}$": [],
			"$\\bf{TM}$": [],
			"$\\bf{FIT}$": [],
			"$\\bf{MD}$": [],
			"$\\bf{ME}$": [],
			"$\\bf{STD}$": []}

	for i in results:
		melhor_fit = min(i[0], key=lambda x: x.fitness).fitness
		media = np.mean([x.fitness for x in i[0]]) 
		mediana = np.median([x.fitness for x in i[0]]) 
		std = np.std([x.fitness for x in i[0]]) 
		table["$\\bf{NPOP}$"].append(i[1]["npop"])
		table["$\\bf{NGER}$"].append(i[1]["nger"])
		table["$\\bf{TC}$"].append(i[1]["tc"])
		table["$\\bf{TM}$"].append(i[1]["tm"])
		table["$\\bf{FIT}$"].append(melhor_fit)
		table["$\\bf{ME}$"].append(media)
		table["$\\bf{MD}$"].append(mediana)
		table["$\\bf{STD}$"].append(std)

	df = pd.DataFrame(data=table)

	fig, ax = plt.subplots()

	fig.patch.set_visible(False)
	plt.axis("off")
	plt.grid("off")
	ax.set_title("Top-20 Execuções", y=0.99, fontdict={"fontsize": 6}, weight='bold')

	ncol = len(table.keys())
	colors = [["#ccccb3"] * ncol, ["#e0e0d1"] * ncol] * int(len(results)/2)
	the_table = ax.table(cellText=df.values,colLabels=df.columns, cellColours=colors, cellLoc="center", loc="center", colColours =["#78786d"] * ncol)
	the_table.auto_set_font_size(False)
	the_table.set_fontsize(6)

	fig.tight_layout()
	fig.savefig("Tabelas/results_table_"+str(len(results))+".pdf", bbox_inches='tight')
	print(colored("\033[1m"+"\n-> Tabela salva em: " + "Tabelas/results_table_"+str(len(results))+".pdf", "green"))
	print("\nTabela: \n", df)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', required=True, type=str, help='Arquivo com os resultados fatoriais')
	args = vars(parser.parse_args())
	results = pickle.load(open(args['f'], 'rb'))
	results.sort(key=lambda x: min(x[0], key=lambda y: y.fitness))
	plot_table(results[:20])