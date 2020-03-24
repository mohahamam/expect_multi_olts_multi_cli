#!/usr/bin/expect
set timeout -1
set prompts ">#|#|\$"
log_file logs/log_2020-03-24-13-51-35/10.33.72.14-20200324135141-7360i-cli.log
spawn ssh isadmin@10.33.72.14
expect "yes/no" { 
			send "yes\r"
			expect "*?assword" { send "ANS#150\r" }
			} "*?assword" { send "ANS#150\r" }
expect ">#"
send "environment inhibit-alarms\r"
expect -re $prompts
send "exit all\r"
expect -re $prompts
send "info configure qos interface flat | match exact:bandwidth\r"
expect -re $prompts
send "info configure equipment ont interface flat\r"
expect -re $prompts
send "show equipment slot\r"
expect -re $prompts
send "exit all\r"
expect ">#"
send "\r"
send "###Ending the session\r"
expect ">#"
send "logout\r"
interact
