import Parser
import Distance
import sys
import csv

def main(argv):
	#Open files
	if len(argv) != 3:
		print('USAGE: <native pdb> <decoy pdb> <model limit>')
		sys.exit(2)
	try:
		native_in = str(argv[0])
		file_in = str(argv[1])
		nr_models = int(argv[2])
		output_file = 'Output/dataSetBreakdown.csv'
	except:
		print('USAGE: <native pdb> <decoy pdb> <model limit>')
		sys.exit(2)
	#Count atoms and calculate LCS if needed
	native_atoms = Parser.countAtoms(native_in)
	decoy_atoms = Parser.countAtoms(file_in)
	if len(native_atoms) != len(decoy_atoms):
		native_result, decoy_result = Parser.lcs(native_atoms, decoy_atoms)
	else:
		native_result, decoy_result = []	
	#Read and store native conformation
	nativelabels, nativeconformation = Parser.readConformations(str(native_in), 1, native_result)
	#Read decoys and store how many are within distance, morethan distance
	#using criteria{2,4}
	criteria = [2,4]
	f_read = open(str(file_in), 'r')
	models = 0
	atoms = []
	nr_atoms = 0
	output_data = []
	currConf = []
	while models < nr_models:
		line = f_read.readline()
		splt = line.split()
		if splt[0] == 'MODEL':
			atoms = []
			currConf = []
			nr_atoms = 0
		elif splt[0] == 'ATOM':
			nr_atoms += 1
			if(splt[2] == 'CA' and (len(decoy_result) == 0 or nr_atoms in decoy_result)):
				atoms.append((float(splt[6]), float(splt[7]), float(splt[8])))
		elif splt[0] == 'TER':
			if(len(atoms) > 0):
				currConf.append(atoms)
				distance = Distance.lrmsd(nativeconformation, currConf)
				if distance <= criteria[0]:
					within2 += 1
				else:
					morethan2 += 1
					if distance <= criteria[1]:
						within4 +=1 
					else: 
						morethan4 += 1
	#Output results in table with protein name, lcs length, number within/morethan for each criteria
	output_data.append(native_in, len(decoy_result),within2, morethan2, within4, morethan4)
	with open(output_file, 'a') as csvfile:
		writer = csv.Writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(output_data)

if __name__ == "__main__":
	main(sys.argv[1:])	
