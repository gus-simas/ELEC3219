import os
import shutil
import re
from datetime import datetime


#run the script in your gem5 directory, create output_susan and output_CRC directories inside

#instruction set, make sure benchmark is compiled for the correct one
ISA = 'X86'

susan_path = 'automotive/susan'
CRC_path = 'telecomm/CRC32'

#0 for simulating a range of sizes, 1 for simulating one size only
data_cache_constant = 1
instruction_cache_constant = 0

#if 0 2^^(n-1) will be simulated
data_cache_size = 2
instruction_cache_size = 2

#if 1 range from 2 to 2^^(n-1) will be simulated
data_cache_range = 7
instruction_cache_range = 2


include_partB = 0
include_partC = 0
include_partD = 0

#part B
cache_associativity = 16
cacheline_size = 16

#part D
branch_predictor = "TAGE"







if(data_cache_constant):
	data_cache_range = 2

if(instruction_cache_constant):
	instruction_cache_range = 2



for dsize in (2**p for p in range(1, data_cache_range)):

	if(data_cache_constant):
		dsize = data_cache_size
		
	for isize in (2**p for p in range(1, instruction_cache_range)):
	
		if(instruction_cache_constant):
			isize = instruction_cache_size

		
		#run susan
		command = "./build/" + ISA + "/gem5.opt configs/example/se.py  -c " + susan_path + "/susan " + "-o " + "\"" + susan_path + "/input_large.pgm sample_output.pgm" + "\""   + " --l1d_size=" + str(dsize) + "kB --l1i_size=" + str(isize) + "kB --caches"
		
		if(include_partB):
			command = command + " --l1d_assoc " + str(cache_associativity) + " --cacheline_size "  + str(cacheline_size)
			
		if(include_partC):
			command = command + " --cpu-type=DerivO3CPU"
		else:
			command = command + " --cpu-type=TimingSimpleCPU"
			
		if(include_partD):
			command = command + " --bp-type " + str(branch_predictor)
		
		os.system(command)
		
		currentDateAndTime = datetime.now()
		
		shutil.copyfile('m5out/stats.txt', ('outputs_susan_' + ISA  + '/d' + str(dsize) + 'i' + str(isize)) + '_' + currentDateAndTime.strftime("%H:%M:%S, %-d"))
		
		#run CRC
		
		command = "./build/" + ISA + "/gem5.opt configs/example/se.py  -c " + CRC_path + "/crc " + "-o " + "\"" + "telecomm/adpcm/data/large.pcm" + "\"" + " --l1d_size=" + str(dsize) + "kB --l1i_size=" + str(isize) + "kB --caches"
		
		if(include_partB):
			command = command + " --l1d_assoc " + str(cache_associativity) + " --cacheline_size "  + str(cacheline_size)
			
		if(include_partC):
			command = command + " --cpu-type=DerivO3CPU"
		else:
			command = command + " --cpu-type=TimingSimpleCPU"
			
		if(include_partD):
			command = command + " --bp-type " + str(branch_predictor)
		
		os.system(command)
		
		currentDateAndTime = datetime.now()
		
		shutil.copyfile('m5out/stats.txt', ('outputs_CRC_' + ISA + '/d' + str(dsize) + 'i' + str(isize)) + '_' + currentDateAndTime.strftime("%H:%M:%S, %-d"))
		
		
		#text_file = open('outputs/' + 'd' + str(dsize) + 'i' + str(isize),'r')
		#file_lines = text_file.readlines()
		#
		#for line in file_lines:
		#	if(re.search('simInsts', line)):
		#		instructions = re.search('simInsts(.*)#', line)
		#	if(re.search('system.cpu.numCycles', line)):	
		#		cycles = re.search('system.cpu.numCycles(.*)#', line)
		#print(cycles.group(1).replace(" ",""))
 		
 			

