#%%
import serial
import time
from string import ascii_lowercase
import json

with open("charTranslation.json", encoding="UTF-8") as f:
	test = json.load(f)
	ddr_2_ascii = {value: key for key, value in test.items()}
	for index in range(1,128):
		tmp = ddr_2_ascii.get(hex(index).upper()[2:]," ")
		print(f"\"{tmp}\",")