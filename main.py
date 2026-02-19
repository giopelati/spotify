from data_extract.data_extract import orquestrator
import os

files = os.listdir('./json')

orquestrator(files)