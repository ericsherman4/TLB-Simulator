#run with python3
#python3 --version 3.6.9

import struct
import string
import sys
import random


#static class
class gvars:
    FILE_NAME = "spice.din"
    SIZE_L1 = 10
    SIZE_L2 = 10
    SIZE_TLB_ENTRIES = None
    SIZE_OFFSET = 12
    VPN_MASK = ((2 ** (32-SIZE_OFFSET)) -1) << SIZE_OFFSET



class TLB:
    use = None
    entries = None
    last_used = None #number of cycles that have elasped since it was last used
    num_entries = 0
    num_hits = 0
    hit_rate = 1
    num_misses = 0


def LRU_update(RU_idx, num_entries):
    TLB.last_used[RU_idx] = 0
    for k in range(0,num_entries):
        if k != RU_idx:
            TLB.last_used[k] += 1
        

def TLB_action(i,data):
    
    # check for hit or miss
    miss = True
    for idx in range(0,gvars.SIZE_TLB_ENTRIES):
        #it hits
        if(TLB.use[idx] and data[1] == TLB.entries[idx]):
            # print("hit")
            TLB.num_hits += 1
            TLB.hit_rate = TLB.num_hits / i
            miss = False
            LRU_update(idx, TLB.num_entries)
            break
    if miss:
        # print("miss")
        TLB.hit_rate = TLB.num_hits / i
        TLB.num_misses += 1
        #if TLB is full, use LRU
        if TLB.num_entries == gvars.SIZE_TLB_ENTRIES:
            # use bit doesnt change, num entries doesnt change
            # TLB.entries[random.randint(0,gvars.SIZE_TLB_ENTRIES-1)] = data[1]
            max_val =  TLB.last_used[0]
            idx = None
<<<<<<< HEAD
            # for k in range(0, gvars.SIZE_TLB_ENTRIES):
            #     if TLB.last_used[k] >= max_val:
            #         idx = k
            idx = TLB.last_used.index(max(TLB.last_used))
            # print("THINGT HERE" + str(idx) + "\n\n")
            LRU_update(idx, TLB.num_entries)
            TLB.entries[idx] = data[1]
=======
            for k in range(0, gvars.SIZE_TLB_ENTRIES):
                if TLB.last_used[k] >= max_val:
                    idx = k
            # print("THINGT HERE" + str(idx) + "\n\n")
            LRU_update(idx, TLB.num_entries)
            TLB.entries[k] = data[1]
>>>>>>> 761544e4fdb577ebc15bbf79ccf0bc099002ce32
        else:
            # find the first empty spot
            for idx in range(0, gvars.SIZE_TLB_ENTRIES):
                if(not TLB.use[idx]):
                    # insert data and update
                    TLB.entries[idx] = data[1]
                    TLB.num_entries+=1
                    TLB.use[idx] = 1
                    LRU_update(idx, TLB.num_entries)
                    break



def main():
    print("Main called.")
    print("This has a unifed memory for instructions and data. Run sim2.py for seperate memory for data and instructions.")

    file = open(gvars.FILE_NAME, "r")
    contents = file.readlines()
    file.close()

    i = 0
    length = len(contents)
<<<<<<< HEAD
    increment_add = int(length / 10)
    percentage_add = int(100/10)
    increment = increment_add
    percentage = percentage_add

    valid = False
    while not valid:
        try:
            gvars.SIZE_TLB_ENTRIES = input("Input size of TLB:  ")
            gvars.SIZE_TLB_ENTRIES = int(gvars.SIZE_TLB_ENTRIES)
        except:
            print("please input a number")
        else:
            if gvars.SIZE_TLB_ENTRIES > 0:
                valid = True
            else: 
                print("Size must be greater than 0")


    TLB.use = [0] * gvars.SIZE_TLB_ENTRIES
    TLB.entries = [0] * gvars.SIZE_TLB_ENTRIES
    TLB.last_used = [0] * gvars.SIZE_TLB_ENTRIES #number of cycles that have elasped since it was last used


    print("Percent complete: 0%")

=======
    increment_add = int(length / 25)
    percentage_add = int(100/25)
    increment = increment_add
    percentage = percentage_add

>>>>>>> 761544e4fdb577ebc15bbf79ccf0bc099002ce32
    while( i < length):
    # while( i < 300000):
        data = [int(contents[i][0:1]),int(contents[i][2:-1],16)]
        # data[1] = (data[1] & gvars.VPN_MASK) >> gvars.SIZE_OFFSET
        data[1] = (data[1] & gvars.VPN_MASK) >> gvars.SIZE_OFFSET
        # print(TLB_entries)
        TLB_action(i+1,data)
        # print(TLB.last_used)

        if i == increment: 
            print("Percent complete: " + str(percentage) + "%")
            increment += increment_add
            percentage += percentage_add


        # if data[0] == 0:
        #     # read
        #     pass
        # elif data[0] == 1:
        #     # write
        #     pass
        # elif data[0] == 2:
        #     # instruction fetch
        #     pass
        # elif data[0] == 3:
        #     # misc
        #     pass
        # else:
        #     # default
        #     print("Instruction not valid. Exiting...")
        #     sys.exit()
        
        i+=1

    print("------------")    
    print("\n\n")
    print("------------")
    for each in range(0, gvars.SIZE_TLB_ENTRIES):
        print(hex(TLB.entries[each]))
    print("------------")
    print("Final TLB entries for the data cache are above^^ (just the 20 bit tags).")
    print("For data cache:")
    print("Final hit rate: " + str(TLB.hit_rate*100)[0:9] + "%")
    print("Total misses: " + str(TLB.num_misses))
    print("Total hits: " + str(TLB.num_hits))


if __name__ == "__main__":
    main()