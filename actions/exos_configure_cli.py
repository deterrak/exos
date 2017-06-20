#!/usr/bin/python

import sys
import getopt
import os.path
import pexpect

# define some globals
#opPrompt = '\w+@\w+:~\$ '
## * EXOS-VM.1 # 
opPromptCfgSave = '\*.+\#\s'
opPrompt = '.+\#\s'
cfgPrompt = '\w+@\w+\# '

targetIp = '172.16.142.55'
cmdFile = 'CMD.txt'
logFile = 'my_log.txt'
username = 'user'
password = 'password'


def printhelp():
    print sys.argv[0] + ' -i <targetIp> -c <commandFile> -l <logFile>'
    print '   -i      -the IPv4 adderss'
    print '   -c      -the file that lists the commands that will be run. Default = CMD.txt'
    print '   -l      -the logFile to record the interactive session'


def debug():
    print "debug: " + targetIp + " " + cmdFile + " " + logFile


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:c:l:u:p:",
                                   ["TargetIP=", "CommandFile", "LogFile=", "Username=", "Password="])
        global targetIp
        global cmdFile
        global logFile
        global username
        global password
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printhelp()
            sys.exit()
        elif opt in ("-i", "--TargetIP"):
            targetIp = arg
        elif opt in ("-c", "--CommandFile"):
            cmdFile = arg
        elif opt in ("-l", "--LogFile"):
            logFile = arg
        elif opt in ("-u", "--Username"):
            username = arg
        elif opt in ("-p", "--Password"):
            password = arg
    print("DEBUG ARGVs are: " + str(argv))
    print('target IPv4 address is [%s]' % targetIp)
    if os.path.isfile(cmdFile):
        print('command file is [%s]' % cmdFile)
    else:
        print('error: command file [%s]' % cmdFile)
        print('Current Working Dir is [%s]' % os.getcwd())
        sys.exit(1)
    print('log file is [%s]' % logFile)
    fout = file(logFile, 'w+')

    # spawn an SSH session to the target
    print('spawing session to target [%s]' % targetIp)
    target = 'ssh -l ' + username + " " + targetIp
    p = pexpect.spawn(target)
    p.logfile = fout

    # wait for the login prompt
    i = p.expect(['yes/no', 'assword: ', pexpect.TIMEOUT], timeout=55)

    if i == 0:
        print('accepting the SSH key')
        p.sendline('yes')
    if i == 1:
        print('login OK')
    elif i == 2:
        print("timeout")

    p.sendline(password)
    i = p.expect([opPromptCfgSave, opPrompt, '\#'], timeout=55)
    if i == 0:
        print('matched opPrompCfgSave')
    if i == 1:
        print('matched opPromp')
    if i == 2:
        print('matched \#')

    print('Attempt to execute commands')
    #p.sendline('configure')
    #p.expect(cfgPrompt)
    #print('Configure mode succeeded')
    # Read the command file
    with open(cmdFile, 'r') as f:
        for line in f:
            print("=" * 75)
            print("trying %s" % line.rstrip())
            p.sendline(line.rstrip())
            p.expect([opPromptCfgSave, opPrompt])
            print("%s" % p.before)
            if not line:
                print("continuing...")
                continue

    # commit
    #p.sendline('commit')
    #p.expect(opPrompt)

    # save
    p.sendline('save')
    #p.expect(cfgPrompt)
    print('save the configuration changes')

    # confirm that we want to save any configuration changes
    p.expect('y/N')
    p.sendline('y')

    # exit configuration mode
    #p.sendline('exit')
    p.expect([opPromptCfgSave, opPrompt])
    print('exit configuration mode')
    # exit operational mode
    p.sendline('exit')
    print('exit operational mode')

    # close the log file
    fout.close()


if __name__ == "__main__":
    main(sys.argv[1:])
