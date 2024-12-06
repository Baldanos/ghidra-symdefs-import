# ARM symdefs import script
#@author Balda

#specs taken from https://developer.arm.com/documentation/dui0803/a/Accessing-and-managing-symbols-with-armlink/Symdefs-file-format

import re

r = re.compile("(0x[0-9a-f]{8}) ([ADTNX]) (\w+)")

symfile = askFile("Select a symdefs file", "Load symdefs file")

with open(str(symfile), 'r') as f:
    for l in f.readlines():
        # Discard comments
        if l[0] in ';#':
            continue

        m = r.match(l)
        if(m):
            addr = int(m.group(1), 0)
            typ = m.group(2)
            val = m.group(3)

            # Code is added as functions
            if typ in "ATX":
                # Fix for thumb addresses
                addr = toAddr(addr & 0xfffffffffffffffe)
                func = createFunction(addr, val)
                if func is None:
                    print("Error adding {} ({}) @ {}".format(val, typ, addr))
            
            # Data and numbers are created as labels
            if typ in "DN":
                addr = toAddr(addr)
                label = createLabel(addr, val, True)
                if label is None:
                    print("Error adding {} ({}) @ {}".format(val, typ, addr))

