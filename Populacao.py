from Individuo import Individuo 
import random

class Populacao:
    def __init__(self, refeicoes, produtos_ids, dieta_kcal, npop=100, taxa_cruzamento=0.9):
        self.npop = npop
        self.taxa_cruzamento = taxa_cruzamento
        self.individuos = self.__init_pop(refeicoes, produtos_ids, dieta_kcal)

    def __init_pop(self, refeicoes, produtos_ids, dieta_kcal):
        return [Individuo(refeicoes, produtos_ids, dieta_kcal) for _ in range(0, self.npop)]

    def avalia_pop(self, nutrientes_prod, restricoes, penalidade=1000):
        for individuo in self.individuos:
            individuo.calc_fitness(nutrientes_prod, restricoes, penalidade)

    def torneio(self, pv=0.9):
        pais = []
        num_pais = 1
        
        while num_pais <= self.npop:
        
            p1 = random.randint(0, self.npop)
            p2 = random.randint(0, self.npop)
        
            while p1 == p2:
                p2 = random.randint(0, self.npop)
        
            if(self.individuos[p2].fitness > self.individuos[p1].fitness):
                vencedor = self.individuos[p1] if random.random() < pv else self.individuos[p2]
            else:
                vencedor = self.individuos[p2] if random.random() < pv else self.individuos[p1]
            
            pais.append(vencedor)
            num_pais += 1

        return pais


    def __str__(self):
        return " ".join([str(individuo) for individuo in self.individuos])