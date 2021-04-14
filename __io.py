import pandas as pd
import pickle
import json
import argparse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-dk', required=False, default=1200, type=int, help='Calorias da Dieta')
	parser.add_argument('-np', required=False, default=100, type=int, help='Número de Indivíduos da População')
	parser.add_argument('-ng', required=False, default=100, type=int, help='Número de Gerações')
	parser.add_argument('-tc', required=False, default=0.9, type=float, help='Taxa de Cruzamento')
	args = vars(parser.parse_args())
	return args

def load_data(file_name="Dataset/dataset_formatado.csv", sep=","):
	return pd.read_csv(file_name, sep)

def load_products(file_name):
	return json.load(open(file_name, "r"))

def save_solution(solution, file_name):
	pickle.dump(solution, open(file_name, "wb"))

def load_solution(file_name):
	return pickle.load(open(file_name, "rb"))      