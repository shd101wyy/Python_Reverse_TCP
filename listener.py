#/usr/bin/env python
### reverse tcp shell listener
### attack executes this file
import os
os.system("netcat -nvlp 6666") # use netcat to listen on port 6666
