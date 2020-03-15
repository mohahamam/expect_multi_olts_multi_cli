#!/usr/bin/python3
import arrow,os,shutil,threading,subprocess,time
from pprint import pprint
from tqdm import tqdm

##creat necessary directories.
logdir =os.path.join('logs','log_'+ arrow.now().format('YYYY-MM-DD-HH-mm-ss'))
if not os.path.exists(logdir):
	os.makedirs(logdir)
commands_dir =os.path.join('commands')
if os.path.exists(commands_dir):
	shutil.rmtree(commands_dir)
if not os.path.exists(commands_dir):
	os.makedirs(commands_dir)

### A function to clean up commands file removing any unecessay enter, and lines that starts with #
def read_commands_file(commands_file):
	with open (commands_file,'r') as inputfile:
		commands = inputfile.readlines()
	cleaned_commands =[x.rstrip('\n') for x in commands if not '\n'.startswith(x) if not '#' in x]
	return cleaned_commands


input_commands = read_commands_file('commands_file.txt')
print('The following commands will be executed on the OLTs:')
for line in input_commands:
	print(line)



# A funtion to creat the expect files
def create_expect_file(cleaned_commands,olt_ip,olt_username,olt_password):
	expect_commands_per_olt=os.path.join(commands_dir,'expect_commands_'+olt_ip+'-'+ arrow.now().format('YYYYMMDDHHmmss')+'-7360i-cli.sh')
	olt_logfilename=os.path.join(logdir,olt_ip+'-'+ arrow.now().format('YYYYMMDDHHmmss')+'-7360i-cli.log')
	
	with open(expect_commands_per_olt,'w') as outputfile:
		outputfile.write('#!/usr/bin/expect\nset timeout -1\n')
		outputfile.write('log_file '+olt_logfilename+'\n')
		#outputfile.write('spawn ssh -oHostKeyAlgorithms=+ssh-dss '+olt_username+'@'+olt_ip+'\n')
		outputfile.write('spawn ssh '+olt_username+'@'+olt_ip+'\n')
		outputfile.write('''expect "yes/no" { 
			send "yes\\r"
			expect "*?assword" { send "'''+olt_password+'''\\r" }
			} "*?assword" { send "'''+olt_password+'''\\r" }''')
		outputfile.write('\n'+'expect ">#"'+'\n')
		for line in cleaned_commands:
			if 'environment inhibit-alarms' in line:
				outputfile.write('send "'+line+'\\r"'+'\n')
				outputfile.write('expect "#"'+'\n')
				outputfile.write('send "exit all\\r"'+'\n')
				outputfile.write('expect ">#"'+'\n')
			else:
				outputfile.write('send "'+line+'\\r"'+'\n')
				outputfile.write('expect ">#"'+'\n')
		outputfile.write('send "\\r"'+'\n')
		outputfile.write('send "###Ending the session\\r"'+'\n')
		outputfile.write('expect ">#"'+'\n')
		outputfile.write('send "logout\\r"'+'\n')
#		outputfile.write('interact'+'\n')
				
#Creating the list of OLTs.
olts_file=input('\nPlease provide the input hosts file name, format OLTIP,username,password in each line:\n')
simultanous_olts=input('Please provide number of Threads you would like to run simultanously:\n')
simultanous_olts=int(simultanous_olts)

with open (olts_file,'r') as olts:
	olts_input=olts.read()
olts_input=olts_input.split('\n')
olts_clean=[x for x in olts_input if not x.startswith('#') and x !=""]
olts_clean=set(olts_clean)
list_of_olts=sorted(olts_clean)

print('The following OLTs will be processed. Total of ',str(len(list_of_olts)),'OLTs:')
for olt in list_of_olts:
	print(olt.split(',')[0])


#####Confirming the List of OLTs and the commands to be sent.
def canweproceed():
	answer = input('Are the above inputs correct? (Yes,No):')

	if answer.lower()=='yes':
		print('Proceeding to Next Steps....')
		time.sleep(0.5)
		pass
	elif answer.lower()=='y':
		print('Proceeding to Next Steps....')
		time.sleep(0.5)
		pass
	else:
		print('You have chosen ',answer)
		print('Quitting...')
		time.sleep(0.25)
		exit()
canweproceed()

for olt in list_of_olts:
	create_expect_file(input_commands,olt.split(',')[0],olt.split(',')[1],olt.split(',')[2])	

list_of_expect_files = os.listdir(commands_dir)



list_of_lists = [list_of_expect_files[i:i+simultanous_olts] for i in range(0, len(list_of_expect_files), simultanous_olts)]


subprocess.run('chmod +x '+commands_dir+'/*',shell=True,check=True)

			
list_of_failed_files=[]
def executing_commands_files(expect_file):

	try:
		subprocess.check_output(expect_file)
		
	except:
		print('An error with processing the file ',expect_file,' has occured !!!')
		list_of_failed_files.append(expect_file)

a=0
with tqdm(total=len(list_of_expect_files)) as pbar:
	for group in list_of_lists:
		threads = []
		a+=1
		
		print('Processing Group',str(a))
		pprint(group)
		for expectfile in group:
			threadprocess=threading.Thread(target=executing_commands_files,args=[os.path.join(commands_dir,expectfile)])
			threads.append(threadprocess)
		for x in threads:
			x.start()
		for x in threads:
			x.join()
			pbar.update(1)
			
			
print('Script Completed')
print('You will find all the logs in the directory',logdir)

try:
	shutil.make_archive(logdir, 'zip', logdir)
except:
	print('could not zip the directory',logdir)

print('The following files failed to execute, please check them again:\n')
for file_01 in list_of_failed_files:
	print(file_01)