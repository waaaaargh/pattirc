#!/usr/bin/python2
import sys
sys.path.append('./pattirc')

import ConfigParser

from window import Window

if __name__ == '__main__':
    cp = ConfigParser.ConfigParser()
    cp.read("config.cfg")
    at = cp.get("general", "access_token")

    w = Window(access_token=at)
    w.mainloop()
