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
    SIZE_TLB_ENTRIES = 32
    SIZE_OFFSET = 12
    VPN_MASK = ((2 ** (32-SIZE_OFFSET)) -1) << SIZE_OFFSET

# data cahce
class TLB:
    use = None
    entries = None
    last_used = None
    num_entries = 0
    num_hits = 0
    hit_rate = 1
    num_misses = 0
    num_accesses = 0

#instruction cache
class TLB2:
    use = None
    entries = None
    last_used = None
    num_entries = 0
    num_hits = 0
    hit_rate = 1
    num_misses = 0
    num_accesses = 0


def LRU_update(RU_idx, num_entries):
    TLB.last_used[RU_idx] = 0
    for k in range(0,num_entries):
        if k != RU_idx:
            TLB.last_used[k] += 1

def LRU_update2(RU_idx, num_entries):
    TLB2.last_used[RU_idx] = 0
    for k in range(0,num_entries):
        if k != RU_idx:
            TLB2.last_used[k] += 1
        

def TLB_action(data):
    TLB.num_accesses +=1
    # check for hit or miss
    miss = True
    for idx in range(0,gvars.SIZE_TLB_ENTRIES):
        #it hits
        if(TLB.use[idx] and data[1] == TLB.entries[idx]):
            # print("hit")
            TLB.num_hits += 1
            miss = False
            LRU_update(idx, TLB.num_entries)
            break
    if miss:
        # print("miss")
        TLB.num_misses += 1
        #if TLB is full, use LRU
        if TLB.num_entries == gvars.SIZE_TLB_ENTRIES:
            # use bit doesnt change, num entries doesnt change
            # TLB.entries[random.randint(0,gvars.SIZE_TLB_ENTRIES-1)] = data[1]
            max_val =  TLB.last_used[0]
            idx = None
            # for k in range(0, gvars.SIZE_TLB_ENTRIES):
            #     if TLB.last_used[k] >= max_val:
            #         idx = k
            idx = TLB.last_used.index(max(TLB.last_used))
            # print("THINGT HERE" + str(idx) + "\n\n")
            LRU_update(idx, TLB.num_entries)
            TLB.entries[idx] = data[1]
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

    # update hit rate
    TLB.hit_rate = TLB.num_hits / TLB.num_accesses

def TLB2_action(data):
    TLB2.num_accesses +=1
    # check for hit or miss
    miss = True
    for idx in range(0,gvars.SIZE_TLB_ENTRIES):
        #it hits
        if(TLB2.use[idx] and data[1] == TLB2.entries[idx]):
            # print("hit")
            TLB2.num_hits += 1
            miss = False
            LRU_update(idx, TLB2.num_entries)
            break
    if miss:
        # print("miss")
        TLB2.num_misses += 1
        #if TLB is full, use LRU
        if TLB2.num_entries == gvars.SIZE_TLB_ENTRIES:
            # use bit doesnt change, num entries doesnt change
            # TLB2.entries[random.randint(0,gvars.SIZE_TLB_ENTRIES-1)] = data[1]
            max_val =  TLB2.last_used[0]
            idx = None
            # for k in range(0, gvars.SIZE_TLB_ENTRIES):
            #     if TLB2.last_used[k] >= max_val:
            #         idx = k
            idx = TLB2.last_used.index(max(TLB2.last_used))
            # print("THINGT HERE" + str(idx) + "\n\n")
            LRU_update2(idx, TLB2.num_entries)
            TLB2.entries[idx] = data[1]
        else:
            # find the first empty spot
            for idx in range(0, gvars.SIZE_TLB_ENTRIES):
                if(not TLB2.use[idx]):
                    # insert data and update
                    TLB2.entries[idx] = data[1]
                    TLB2.num_entries+=1
                    TLB2.use[idx] = 1
                    LRU_update2(idx, TLB2.num_entries)
                    break
    
    #update hit rate
    TLB2.hit_rate = TLB2.num_hits / TLB2.num_accesses


def main():
    print("Main called.")
    print("This has seperate memory for instructions and data. Run sim2.py for unified memory for data and instructions.")

    file = open(gvars.FILE_NAME, "r")
    contents = file.readlines()
    file.close()

    i = 0
    length = len(contents)
    increment_add = int(length / 10)
    percentage_add = int(100/10)
    increment = increment_add
    percentage = percentage_add

    valid = False
    while not valid:
        try:
            gvars.SIZE_TLB_ENTRIES = input("Input size of TLB: ")
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

    TLB2.use = [0] * gvars.SIZE_TLB_ENTRIES
    TLB2.entries = [0] * gvars.SIZE_TLB_ENTRIES
    TLB2.last_used = [0] * gvars.SIZE_TLB_ENTRIES #number of cycles that have elasped since it was last used


    print("Percent complete: 0%")

    while( i < length):
    # while( i < 300):
        data = [int(contents[i][0:1]),int(contents[i][2:-1],16)]
        # data[1] = (data[1] & gvars.VPN_MASK) >> gvars.SIZE_OFFSET
        data[1] = (data[1] & gvars.VPN_MASK) >> gvars.SIZE_OFFSET
        # print(TLB_entries)
        # print(TLB.last_used)

        if i == increment: 
            print("Percent complete: " + str(percentage) + "%")
            increment += increment_add
            percentage += percentage_add


        if data[0] == 0:
            # read
            TLB_action(data)
            pass
        elif data[0] == 1:
            # write
            TLB_action(data)
            pass
        elif data[0] == 2:
            # instruction fetch
            TLB2_action(data)
            pass
        elif data[0] == 3:
            # misc
            # ??
            pass
        else:
            # default
            print("Instruction not valid. Exiting...")
            sys.exit()
        
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

    print("\n\n")
    print("------------")
    for each in range(0, gvars.SIZE_TLB_ENTRIES):
        print(hex(TLB2.entries[each]))
    print("------------")
    print("Final TLB entries for the instruction cache are above^^ (just the 20 bit tags).")
    print("For instruction cache:")
    print("Final hit rate: " + str(TLB2.hit_rate*100)[0:9] + "%")
    print("Total misses: " + str(TLB2.num_misses))
    print("Total hits: " + str(TLB2.num_hits))


if __name__ == "__main__":
    main()