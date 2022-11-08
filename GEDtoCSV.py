import csv
import numpy as np

import tkinter as tk
import tkinter.filedialog as fd
from tkinter import *
from tkinter import ttk

import requests

GoogleAPIKey = "AIzaSyAj79TrFXjuJdtqmklfXbjptiveClji7Kw"


headers = ["Latitude","Longitude", "Name", "Description", "Icon", "TimeBegin", "IconColour"]
finalInformation = np.empty([10,5000,10], dtype = "U256")
tempInformation = np.empty([10,5000,10], dtype = "U256")
information = np.empty([10,5000,10], dtype = "U256")


abstractionLevelStr = input("What level of location abstraction would you like to accept?\n A higher number means only very specific locations will be included, lower means broad locations will be accepted as well.\n 3 is recommended for accurate the United States\n 2 recommended for broad United States or accurate elsewhere\n 1 recommended for broad elsewhere.\n")
abstractionLevel = int(abstractionLevelStr)


bannedWords = np.array(["tether", " to ", "unknown", "maternal", "paternal"])
bannedCounty = np.array([" Co,", " County,", " co,", " county,", "co.,", "Co."])
bannedUnknown = np.array(["UNKNOWN", "unknown", "Unknown", "BET", "AND", "OR", "AFT",])

main = tk.Tk()
main.geometry("+300+400")
main.withdraw()

root = tk.Tk()
root.geometry("+500+320")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Please select the GEDCOM files to be converted to .CSV files", font = ("30")).grid(column=0, row=0)
ttk.Label(frm, text="The conversion process may take a few minutes. Please wait. This message will dissapear when the conversion is complete", font = ("30")).grid(column=0, row=1)

input_file_names = fd.askopenfilenames(parent=main, title='Select the GEDCOM files to be converted', filetypes = [("Ged files", "*.ged")])



file_names = np.empty([len(input_file_names)], dtype = "U256")	

FI_Length = np.zeros([len(input_file_names)], dtype = int)

for x in range(0, len(input_file_names)):
	
	for i in range(0, len(input_file_names[x])-4) :
		file_names[x] += input_file_names[x][i]
	
	f = open(input_file_names[x], "r", errors = "ignore")
	
	lines = f.readlines()
	
	line_counter = 0;
	indiv_counter = 0;
	name_counter = 0;
	birth_counter = 0;
	death_counter = 0;
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
			birth_counter = indiv_counter
			death_counter = indiv_counter
			
			
		elif "1 NAME " in line:
			name_counter = name_counter + 1
			if name_counter == indiv_counter:
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
			else:
				name_counter = name_counter - 1
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
			if birth_counter == indiv_counter:
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
				birth_counter = birth_counter + 1


				
				
		elif "1 DEAT" in line :
			line_counter = line_counter + 1
			line = lines[line_counter]
			if death_counter == indiv_counter:
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
				death_counter = death_counter + 1

					
					
					
		else :
			line_counter = line_counter + 1


for x in range(0, len(input_file_names)):
	skips = 0;
	for i in range (0, len(information[x])-1):
		commaLocal = 0
		preCommaString = ""
		
		information[x][i][5] = information[x][i][5].strip(" ,")
		information[x][i][7] = information[x][i][7].strip(" ,")
		
		if "ABT" in information[x][i][4]:							#if has "ABT" in date, remove the ABT
			information[x][i][4] = information[x][i][4].strip("ABT")
		if "BEF" in information[x][i][4]:							#if has "BEF" in date, remove the BEF
			information[x][i][4] = information[x][i][4].strip("BEF")
		if "Abt." in information[x][i][4]:							#if has "ABT" in date, remove the ABT
			information[x][i][4] = information[x][i][4].strip("Abt.")
		if "Abt" in information[x][i][4]:							#if has "ABT" in date, remove the ABT
			information[x][i][4] = information[x][i][4].strip("Abt")
		
		if "ABT" in information[x][i][6]:							#if has "ABT" in date, remove the ABT
			information[x][i][6] = information[x][i][6].strip("ABT")
		if "BEF" in information[x][i][6]:							#if has "BEF" in date, remove the BEF
			information[x][i][6] = information[x][i][6].strip("BEF")
		if "Abt." in information[x][i][6]:							#if has "ABT" in date, remove the ABT
			information[x][i][6] = information[x][i][6].strip("Abt.")
		if "Abt" in information[x][i][6]:							#if has "ABT" in date, remove the ABT
			information[x][i][6] = information[x][i][6].strip("Abt")

		
			
		if any(bannedUnknown[w] in information[x][i][4] for w in (0,1,2,3,4,5,6)):	#if has variations of unknown in date, dont keep it
			information[x][i][4] = ""
		if any(bannedUnknown[v] in information[x][i][6] for v in (0,1,2,3,4,5,6)):
			information[x][i][6] = ""
		
		if len(information[x][i][4]) < 4:
			information[x][i][4] = ""
		if len(information[x][i][6]) < 4:
			information[x][i][6] = ""
			
			
		if information[x][i][4].startswith(("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")):
			information[x][i][4] = "01 " + information[x][i][4]
		if information[x][i][6].startswith(("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")):
			information[x][i][6] = "01 " + information[x][i][6]		#if has no day listed, mark as 1st for consistency
		
		
		if information[x][i][5].count(",") < abstractionLevel: 		#if not enough detail via commas in birth local, delete
			information[x][i][5] = ""
		if information[x][i][7].count(",") < abstractionLevel:		#if not enough detail via commas in death local, delete
			information[x][i][7] = ""	
			
		if information[x][i][5].find(",") > - 1:
			commaLocal = information[x][i][5].find(",")
			preCommaString = information[x][i][5][0:commaLocal+1]
			if any(bannedCounty[k] in preCommaString for k in (0,1,2,3,4,5)):
				information[x][i][5] = ""									#if the first piece of location info is a county its too broad, dont keep it
		if information[x][i][7].find(",") > - 1:
			commaLocal = information[x][i][7].find(",")
			preCommaString = information[x][i][7][0:commaLocal+1]
			if any(bannedCounty[k] in preCommaString for k in (0,1,2,3,4,5)):
				information[x][i][7] = ""	
				
				
		if len(information[x][i][4]) == 4 or len(information[x][i][4]) == 5:
			information[x][i][4] = "01-01-" + information[x][i][4]
		if len(information[x][i][6]) == 4 or len(information[x][i][6]) == 5:
			information[x][i][6] = "01-01-" + information[x][i][6]		#only given a year, fill the day/month with 01/01 for consistency
			
			
		if len(information[x][i][4]) == 0 or len(information[x][i][5]) == 0:	#if has birth date or location but not both, remove the other
			information[x][i][4] = ""
			information[x][i][5] = ""
		if len(information[x][i][6]) == 0 or len(information[x][i][7]) == 0:	#if has death date or location but not both, remove the other
			information[x][i][6] = ""
			information[x][i][7] = ""
			
			
		if len(information[x][i][4]) == 0 and len(information[x][i][6]) == 0:	#if there isnt any date or location info dont keep it
			skips = skips + 1
		elif len(information[x][i][1]) == 0 and len(information[x][i][2]) == 0:	#if no name dont keep it
			skips = skips + 1
		elif any(bannedWords[j] in information[x][i][2] for j in (0,1,2,3,4)):	#if name has banned words dont keep it
			skips = skips + 1
		else: 
			tempInformation[x][i-skips] = information[x][i]
			

for x in range(0, len(input_file_names)):
	offset = 0
	for i in range (0, len(tempInformation[x])-1):
		isBirth = 0;
		if len(tempInformation[x][i][4]) > 0:
			finalInformation[x][i+offset][7] = tempInformation[x][i][5]
			finalInformation[x][i+offset][2] = tempInformation[x][i][2]
			finalInformation[x][i+offset][2] += tempInformation[x][i][1]
			finalInformation[x][i+offset][4] = "180"
			if x < 12:
				finalInformation[x][i+offset][6] = str(30*x)
			elif x < 24:
				finalInformation[x][i+offset][6] = str(30*(x-12))
			else:
				finalInformation[x][i+offset][6] = str(30*(x-24))
			finalInformation[x][i+offset][3] = "Birth"
			finalInformation[x][i+offset][5] = tempInformation[x][i][4]
			finalInformation[x][i+offset][0] = tempInformation[x][i][5]
			isBirth = 1
		if len(tempInformation[x][i][6]) > 0:
			if isBirth:
				offset = offset + 1
			finalInformation[x][i+offset][7] = tempInformation[x][i][7]
			finalInformation[x][i+offset][2] = tempInformation[x][i][2]
			finalInformation[x][i+offset][2] += tempInformation[x][i][1]
			finalInformation[x][i+offset][4] = "180"
			if x < 12:
				finalInformation[x][i+offset][6] = str(30*x)
			elif x < 24:
				finalInformation[x][i+offset][6] = str(30*(x-12))
			else:
				finalInformation[x][i+offset][6] = str(30*(x-24))
			finalInformation[x][i+offset][3] = "Death"
			finalInformation[x][i+offset][5] = tempInformation[x][i][6]
			finalInformation[x][i+offset][0] = tempInformation[x][i][7]

for x in range(0, len(input_file_names)):
	f = 0
	FI_Length[x] = 0
	while finalInformation[x][f][0] != "":
		FI_Length[x] = FI_Length[x] + 1
		f = f + 1
		
		

			
for x in range(0, len(input_file_names)):
	print(f"Converting file {x+1}. Events found: {FI_Length[x]}")
	for i in range(0, FI_Length[x]):
		baseURL = "https://maps.googleapis.com/maps/api/geocode/json?address="
		baseURL += finalInformation[x][i][0]
		baseURL += "&key="
		baseURL += GoogleAPIKey

		
		r = requests.get(baseURL).json()
		
		if r["status"] == "OK":
			geometry = r["results"][0]["geometry"]
			finalInformation[x][i][0] = geometry["location"]["lat"]
			finalInformation[x][i][1] = geometry["location"]["lng"]

		
for x in range(0,len(file_names)):
	file_names[x] += ".csv"
	with open(file_names[x], "w+", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(finalInformation[x])


print("\n\nThe produced CSV files are in the same directory as the provided GEDCOM files, at: ");
for x in file_names:
	print(x)