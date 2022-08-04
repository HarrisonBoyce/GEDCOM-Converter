import csv
import numpy as np

import tkinter as tk
import tkinter.filedialog as fd
from tkinter import *
from tkinter import ttk


headers = ["ID","Surname", "Given Name", "Sex", "Birth Date", "Birth Location", "Death Date", "Death Location"]
information = np.empty([10,100,100], dtype = "U256")


main = tk.Tk()
main.geometry("+300+400")
main.withdraw()

root = tk.Tk()
root.geometry("+500+320")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Please select the GEDCOM files to be converted to .CSV files", font = ("30")).grid(column=0, row=0)

input_file_names = fd.askopenfilenames(parent=main, title='Select the GEDCOM files to be converted', filetypes = [("Ged files", "*.ged")])



file_names = np.empty([len(input_file_names)], dtype = "U256")	


for x in range(0, len(input_file_names)):
	
	for i in range(0, len(input_file_names[x])-4) :
		file_names[x] += input_file_names[x][i]
	
	f = open(input_file_names[x], "r")
	
	lines = f.readlines()
	
	line_counter = 0;
	indiv_counter = 0;
	line = "Hi";
		
	while line_counter < len(lines) :
		line = lines[line_counter]
		#print("in while TRLR")
		I_gap = 3;
		N_gap = 7;
		S_gap = 6;
		BD_gap = 7;
		BP_gap = 7;
		DD_gap = 7;
		DP_gap = 7;
		
		
		if "0 @I" in line:
			while line[I_gap] != "@":
				information[x][indiv_counter][0] += line[I_gap]
				I_gap = I_gap + 1
				#print(line[I_gap])
			indiv_counter = indiv_counter + 1
			#print("in while I")
			#print(indiv_counter)
			line_counter = line_counter + 1
			
			
		elif "1 NAME " in line:
			while line[N_gap] != "/" and N_gap < len(line) - 1 :
				information[x][indiv_counter-1][2] += line[N_gap]
				#print(line[N_gap])
				N_gap = N_gap + 1
				#print("in while N1")
			if line[N_gap] == "/" :
				N_gap = N_gap + 1
			while line[N_gap] != "/" and N_gap < len(line) - 1 :
				information[x][indiv_counter-1][1] += line[N_gap]
				#print(line[N_gap])
				N_gap = N_gap + 1
				#print("in while N2")
			line_counter = line_counter + 1	
				
				
		elif "1 SEX " in line:
			while line[S_gap] != "/" and S_gap <len(line)-1 :
				information[x][indiv_counter-1][3] += line[S_gap]
				#print(line[S_gap])
				S_gap = S_gap + 1
				#print("in while S")
			line_counter = line_counter + 1
				
				
		elif "1 BIRT" in line :
			line_counter = line_counter + 1
			line = lines[line_counter]
			if "2 DATE" in line :
				while BD_gap < len(line) - 1 :
					information[x][indiv_counter-1][4] += line[BD_gap]
					BD_gap = BD_gap + 1
					#print("in BD while")
				line_counter = line_counter + 1
				line = lines[line_counter]
			if "2 PLAC" in line :
				while BP_gap < len(line) - 1 :
					information[x][indiv_counter-1][5] += line[BP_gap]
					BP_gap = BP_gap + 1
					#print("in BP while")
				line_counter = line_counter + 1
				
				
		elif "1 DEAT" in line :
			line_counter = line_counter + 1
			line = lines[line_counter]
			if "2 DATE" in line :
				while DD_gap < len(line) - 1 :
					information[x][indiv_counter-1][6] += line[DD_gap]
					DD_gap = DD_gap + 1
					#print("in DD while")
				line_counter = line_counter + 1
				line = lines[line_counter]
			if "2 PLAC" in line :
				while DP_gap < len(line) - 1 :
					information[x][indiv_counter-1][7] += line[DP_gap]
					DP_gap = DP_gap + 1
					#print("in DP while")
				line_counter = line_counter + 1
		else :
			line_counter = line_counter + 1


			
for x in range(0,len(file_names)):
	file_names[x] += ".csv"
	with open(file_names[x], "w+", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(information[x])


print("\n\nThe produced CSV files are in the same directory as the provided GEDCOM files, at: ");
for x in file_names:
	print(x)