import matplotlib.pyplot as plt
from termcolor import colored

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