The scriprt will attempt to connect to a list of given OLTs file
the OLTs file should have the below formated example

10.33.72.14,isadmin,ANS#150
10.33.72.15,isadmin,ANS#150
10.44.72.17,isadmin,ANS@123



Once you run the script, you will be asked for an input hosts file, and the number of simutanous OLTs to be executed.
you will be then given a list of commands that will be executed on all the OLTs 
the input of the commands file is called commands_file.txt please be carefull while entering the needed commands in this file!!
you have to provide for each command a new line, example of commands_file.txt:

environment inhibit-alarms
info configure qos interface flat | match exact:bandwidth
info configure equipment ont interface flat
show equipment slot

To start executing the commands, this script will create for each OLT a file under commands directory ( these files are expect shell scripts)

once the scripts starts executing, it will show you which group of OLTs is being processed, and will then give you the completion status bar.

once the script finishes, it will save the logs under logs directory, and zip that directory for you to be able to move it fasted to your local machine if required.


below is an example of how to execute the script:


#########################################################################

The following commands will be executed on the OLTs:
environment inhibit-alarms
info configure qos interface flat | match exact:bandwidth
info configure equipment ont interface flat
show equipment slot

Please provide the input hosts file name, format OLTIP,username,password in each line:
hosts
Please provide number of Threads you would like to run simultanously:
10
The following OLTs will be processed. Total of  3 OLTs:
10.33.72.14
10.33.72.15
10.44.72.17
Are the above inputs correct? (Yes,No):y
Proceeding to Next Steps....
	0%|                                                                         | 0/3 [00:00<?, ?it/s]Processing Group 1
OLT-1/3 : 10.33.72.15
OLT-2/3 : 10.33.72.14
OLT-3/3 : 10.44.72.17
send: spawn id exp7 not open
		while executing
"send "logout\r""
		(file "commands/expect_commands_10.33.72.14-20200315120525-7360i-cli.sh" line 23)send: spawn id exp7 not open
		while executing
"send "logout\r""
		(file "commands/expect_commands_10.33.72.15-20200315120525-7360i-cli.sh" line 23)send: spawn id exp7 not open
		while executing
"send "logout\r""
		(file "commands/expect_commands_10.44.72.17-20200315120525-7360i-cli.sh" line 23)


An error with processing the file  commands/expect_commands_10.44.72.17-20200315120525-7360i-cli.sh  has occured !!!
An error with processing the file  commands/expect_commands_10.33.72.15-20200315120525-7360i-cli.sh  has occured !!!
 33%|█████████████████████▋                                           | 1/3 [01:15<02:30, 75.17s/it]An error with processing the file  commands/expect_commands_10.33.72.14-20200315120525-7360i-cli.sh  has occured !!!
100%|█████████████████████████████████████████████████████████████████| 3/3 [01:15<00:00, 25.06s/it]

###############################################################################

Script Completed
The script was executed in 75.21120381355286 Seconds
You will find all the logs in the directory logs/log_2020-03-15-12-05-17


The following files failed to execute, please check them again:

commands/expect_commands_10.44.72.17-20200315120525-7360i-cli.sh
commands/expect_commands_10.33.72.15-20200315120525-7360i-cli.sh
commands/expect_commands_10.33.72.14-20200315120525-7360i-cli.sh
