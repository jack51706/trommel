import argparse
import os
from datetime import datetime
import indicators
import indicator_config
import sys
import time

parser = argparse.ArgumentParser(description= "TROMMEL: Sift Through Directories of Files to Identify Indicators That May Contain Vulnerabilities")
parser.add_argument("-p","--path", required=True, help="Directory to Search")
parser.add_argument("-o","--output", default='Unspecified_Name', help="Output TROMMEL Results File Name (no spaces)")
parser.add_argument("-b","--binary", action='store_true', help="Search in Binary Files")
parser.add_argument("-s","--search", help="User specificed Keyword Search")
parser.add_argument("-d","--dir", required=True, help="Directory to Write Output TROMMEL Results")

args = vars(parser.parse_args())

path = args['path']
output = args['output']
bin_search = args['binary']
user_search = args['search']
dir_output = args['dir']


#Main function		
def main():
	db_file = 'vfeed.db'
	files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
	if db_file in files:
		print 'Found vFeed database in working directory...continuing.'
	else:
		sys.exit('TROMMMEL quit. Please download & put the vFeed database in this working directory to continue.')
	

	if user_search:
		print 'TROMMEL is doing a one-off keyword search specified by the user. Results will be printed to stdout.'
		time.sleep(7)
		#Enumerate dir passed by user
		for root, dirs, files in os.walk(path):
			for names in files:
				ff = os.path.join(root,names)
				#Ignore any symlinks
				if not os.path.islink(ff):
					#Ignore the /dev directory. Script has problems with files in this directory
					dev_kw = "/dev/"
					if not dev_kw in ff:
						indicators.user_search_kw(ff, user_search, bin_search)
	
	else:	
		
		#Date informtion
		yrmoday = datetime.now().strftime("%Y%m%d_%H%M%S")

		#Save file name and date information to file in working directory script
		trommel_output =  file(dir_output + output+'_TROMMEL_'+yrmoday,'w')
		
		trommel_vfeed_output = file("TROMMEL_vFeed_Results_"+yrmoday, 'w')
		
		#Print information to terminal
		print "\nTROMMEL is working to sift through the directory of files.\n\nResults will be saved to '%s_TROMMEL_%s'.\nvFeed results will be saved to 'TROMMEL_vFeed_Results_%s'.\n" % (output, yrmoday,yrmoday)
	
		
		#Title written to file
		trommel_output.write('''

	 :::==== :::====  :::====  :::=======  :::=======  :::===== :::     
	 :::==== :::  === :::  === ::: === === ::: === === :::      :::     
	   ===   =======  ===  === === === === === === === ======   ===     
	   ===   === ===  ===  === ===     === ===     === ===      ===     
	   ===   ===  ===  ======  ===     === ===     === ======== ========
																																							  

	''')
	
		#User given name and path to user given directory to search
		trommel_output.write("TROMMEL Results File Name: %s\nDirectory: %s\n" % (output,path))
	
		#Count number of files within given path directory
		total = 0
		for root, dirs, files in os.walk(path, followlinks=False):
			total += len(files)
		trommel_output.write("There are %d total files within the directory.\n\n" % total)
	
		#Disclaimer written to output file
		trommel_output.write("Results could be vulnerabilities. These results should be verified as false positives may exist.\n\n")
		
		#Enumerate dir passed by user
		for root, dirs, files in os.walk(path):
		
			for names in files:
				ff = os.path.join(root,names)
			
				if '/bin/busybox' in ff:
					value = indicator_config.check_arch(ff, trommel_output)
					print "Based on the binary 'busybox' the instruction set architecture is %s.\n" % value
		
				#Ignore any symlinks
				if not os.path.islink(ff):
				
					#Ignore the /dev directory. Script has problems with files in this directory
					dev_kw = "/dev/"
					if not dev_kw in ff:
					
						if path and output: 
							indicators.kw(ff, trommel_output, trommel_vfeed_output, names, bin_search)
						
							
if __name__ == '__main__':
		main()