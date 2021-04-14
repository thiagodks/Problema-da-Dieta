import pandas as pd
import pickle
import json

def load_data(file_name="Dataset/dataset_formatado.csv", sep=","):
	return pd.read_csv(file_name, sep)

def load_products(file_name):
	return json.load(open(file_name, "r"))

def save_solution(solution, file_name):
	pickle.dump(solution, open(file_name, "wb"))

def load_solution(file_name):
	return pickle.load(open(file_name, "rb"))      