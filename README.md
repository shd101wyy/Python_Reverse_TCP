## CS 461 Final Project
### Reverse TCP Shell ~~a very stupid trojan~~
- ywang189 - Yiyi Wang
- cjsmith7 - Christian Smith

### Two files are provided
- reverse_tcp.py
    -  malicious python code, run it on victim side.
    -  can be packed into <strong>"exe"</strong> file using <strong>pyinstaller</strong> and run on Windows with no antivirus software detected (tested on Windows8.1, not detected)
        - On windows, run ``` pyinstaller --noconsole --onefile reverse_tcp.py``` to pack the malicious ```reverse_tcp.py``` to Windows executable file.

- listener.js
    - simple listener written in javascript(node.js)

### How to attack
* On attacker side, execute ```node listener.js``` to run the listener file on attacker's machine.
* Plant and execute ```reverse_tcp.py``` on victim machine. (SE, camouflage py file as part of package, etc)


### Why implementing Reverse TCP attack in Python
We first tried <strong>metasploit</strong> and used the <strong>windows/shell_reverse_tcp</strong> payload to generate the malicious <strong>exe</strong> file and we also tried <strong>msfencode</strong> to encode the <strong>exe</strong> file. However, no matter how we encoded the malicious <strong>exe</strong> file, <strong>Windows Defender</strong> could <strong>always</strong> detect it(It is interesting to find out that some 3rd party av couldn't detect our trojan). After doing some research, we find out that <strong>Windows Defender</strong> will always load the program to memory first then scan it, so encoding will never work.
