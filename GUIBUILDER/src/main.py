from os import devnull, environ
import sys
from steuerung import Steuerung

if __name__ == "__main__":
    if environ.get("DEV") == None:
        # Release: Disables print(), etc
        sys.stdout = sys.stderr = open(devnull, 'w')

    print("\n"*20)
    s = Steuerung()
    s.run()
