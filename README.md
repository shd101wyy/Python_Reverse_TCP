## CS 461 Final Project
### Reverse TCP Shell ~~a very stupid trojan~~
- ywang189 - Yiyi Wang
- cjsmith7 - Christian Smith

### Multiple files are provided
- <strong>reverse_tcp.py</strong>
    -  malicious python code, run it on victim side.
    -  can be packed into <strong>"exe"</strong> file using <strong>pyinstaller</strong> and run on Windows with no antivirus software detected (tested on Windows8.1, not detected)
        - On windows, run ``` pyinstaller --noconsole --onefile reverse_tcp.py``` to pack the malicious ```reverse_tcp.py``` to Windows executable file.
- <strong>listener.js</strong>
    - simple listener written in javascript(node.js)
- <strong>schtasks_template.xml</strong>(for Windows hack only)
    - sample template for schtasks program on Windows
    - eg: when schedule a malicious task from the <strong>schtasks_template.xml</strong> on Windows, run the following command
```
schtasks /CREATE /XML path_to_schtasks_template.xml /TN malicious_task_name
```  
- <strong> dist/reverse_tcp.exe </strong>
    - packed <strong>exe</strong> file using <strong>pyinstaller</strong> mentioned above.
    - <storng>don't run</strong> this file on your machine, it is <strong>dangerous</strong>(as it will connect to my attack machine at ip 45.55.139.173).
- <strong>cleanup.bat (for Windows)</strong>
    - remove our simple stupid trojan from victim's system
    - double click it to cleanup.

### How to Hack (For Windows)
1. Edit the variable <strong> attacker_ip  </strong> in <strong> reverse_tcp.py </strong> to attacker's ip address
2. Run ```pyinstaller --noconsole --onefile reverse_tcp.py``` to create <strong>reverse_tcp.exe</strong>
3. Copy <strong>reverse_tcp.exe</strong> to victim's machine and execute it. (No console will pop up so don't worry)
4. Run ```node listener.js``` on attacker's machine to start listening to responses from victims.

### How to Hack (For .nix)
1. Edit the variable <strong> attacker_ip  </strong> in <strong> reverse_tcp.py </strong> to attacker's ip address
3. Copy <strong>reverse_tcp.py</strong> to victim's machine and run ```python reverse_tcp.py```.
4. Run ```node listener.js``` to start listening to responses from victims.


### General decriptions
* On attacker side, execute ```node listener.js``` to run the listener file on attacker's machine.
* Plant and execute ```reverse_tcp.py``` on victim machine. (SE, camouflage py file as part of package, etc)

### How it works(For Windows)
* The <Strong>reverse_tcp.py</strong>(<strong>reverse_tcp.exe</strong>) file will first copy itself to %Appdata% folder, then create <strong>schtasks_template.xml</strong> file for scheduling tasks
* It then runs <strong>schtasks</strong> program and setup the running task so that the victim will try connecting to attacker every 30 minutes by default.
* After that, victim will try to connect to attacker's ip and port.
* Attacker will send commands to victim, and victim will execute those commands on their machine.



### Why implementing Reverse TCP attack in Python
We first tried <strong>metasploit</strong> and used the <strong>windows/shell_reverse_tcp</strong> payload to generate the malicious <strong>exe</strong> file and we also tried <strong>msfencode</strong> to encode the <strong>exe</strong> file. However, no matter how we encoded the malicious <strong>exe</strong> file, <strong>Windows Defender</strong> could <strong>always</strong> detect it(It is interesting to find out that some 3rd party av couldn't detect our trojan). After doing some researches, we found out that <strong>Windows Defender</strong> will always load the program to memory first then scan it, so encoding will never work.

### What we learnt
- <strong> Windows Defender </strong> is powerful.
- <strong> Not all metasploit payloads </strong> work on Windows/
- <strong> Security awareness is important </strong>
- <strong> Security is fun. CS460 is an aweasome class.</strong>
