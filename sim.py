#run with python3
#python3 --version 3.6.9

import struct
import string
import sys
import binascii
import random


#static class
class gvars:
    FILE_NAME = "spice.din"
    SIZE_L1 = 10
    SIZE_L2 = 10
    SIZE_TLB_ENTRIES = 32
    SIZE_OFFSET = 12
    VPN_MASK = (2 ** (32-SIZE_OFFSET) -1) << SIZE_OFFSET



class TLB:
    use = [0] * gvars.SIZE_TLB_ENTRIES
    entries = [0] * gvars.SIZE_TLB_ENTRIES
    num_entries = 0
    num_hits = 0
    hit_rate = 1




def TLB_action(i,data):
    
    # check for hit or miss
    miss = True
    for idx in range(0,gvars.SIZE_TLB_ENTRIES):
        if(TLB.use[idx] and data[1] == TLB.entries[idx]):
            # print("hit")
            TLB.num_hits += 1
            TLB.hit_rate = TLB.num_hits / i
            miss = False
            break
    if miss:
        # print("miss")
        TLB.hit_rate = TLB.num_hits / i
        if TLB.num_entries == gvars.SIZE_TLB_ENTRIES:
            # use bit doesnt change, num entries doesnt change
            TLB.entries[random.randint(0,gvars.SIZE_TLB_ENTRIES-1)] = data[1]
        else:
            # find the first empty spot
            for idx in range(0, gvars.SIZE_TLB_ENTRIES):
                if(not TLB.use[idx]):
                    # insert data and update
                    TLB.entries[idx] = data[1]
                    TLB.num_entries+=1
                    TLB.use[idx] = 1
                    break


        

def main():
    print("Main called.")

    file = open(gvars.FILE_NAME, "r")
    contents = file.readlines()

    i = 0

    # while( i < len(contents)):
    while( i < 2200):
        data = [int(contents[i][0:1]),int(contents[i][2:-1],16)]
        data[1] = (data[1] & gvars.VPN_MASK) >> gvars.SIZE_OFFSET
        # print(TLB_entries)
        TLB_action(i+1,data)
        

        # print(data[1])
        # print(type(data[1]))
        # print(len(data[1]))

        if data[0] == 0:
            # read
            pass
        elif data[0] == 1:
            # write
            pass
        elif data[0] == 2:
            # instruction fetch
            pass
        elif data[0] == 3:
            # misc
            pass
        else:
            # default
            print("Instruction not valid. Exiting...")
            sys.exit()
        
        i+=1

    print("Final hit rate: " + str(TLB.hit_rate*100)[0:9] + "%")

# TLB is for translating virtual address to physical address
# we are given the virtual address
# on a miss, we need to go through the page table and get the physical address, but the assingment says not to worry about the that. 
# soo, on a hit or a miss, what exactly are we putting iin the the TLB???????
    



    file.close()



if __name__ == "__main__":
    main()