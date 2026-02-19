from data_extract.data_extract import orquestrator
import os

files = os.listdir('./json')

for file in files:
    file_path = f'./json/{file}'
    orquestrator(file_path)