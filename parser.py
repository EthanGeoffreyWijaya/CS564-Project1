
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub
import numpy as np

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""
def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            fb = transformDollar(item["First_Bid"])
            st = transformDttm(item["Started"])
            en = transformDttm(item["Ends"])
            cu = transformDollar(item["Currently"])
            desc = item["Description"]
            name = item["Name"].replace('\"', '\"\"')
            
            if("Buy_Price" in item):
                bp = transformDollar(item["Buy_Price"])
            else:
                bp = "NULL"
            if(desc is None):
                desc = "NULL"
            else:
                desc = desc.replace('\"', '\"\"')
            
            allitems.append(str(item["ItemID"])+"|\""+name+"\"|\""+cu+"\"|\""+bp+"\"|\""
                     +fb+"\"|"+str(item["Number_of_Bids"])+"|\""+st+"\"|\""+en+"\"|\""
                     +item["Seller"]["UserID"]+"\"|\""+desc+"\"\n")
            for c in item["Category"]:
                allcats.append(str(item["ItemID"])+"|\""+c+"\"\n")

            if(item["Bids"] is not None):
                for b in item["Bids"]:
                    b = b["Bid"]
                    tm = transformDttm(b["Time"])
                    am = transformDollar(b["Amount"])
                    bu = b["Bidder"]["UserID"].replace('\"', '\"\"')
                    if("Location" in b["Bidder"]):
                        bl = b["Bidder"]["Location"].replace('\"', '\"\"')
                    else:
                        bl = "NULL"
                    if("Country" in b["Bidder"]):
                        bc = b["Bidder"]["Country"].replace('\"', '\"\"')
                    else:
                        bc = "NULL"
                
                    allbids.append(str(item["ItemID"])+"|\""+bu+"\"|\""
                         +tm+"\"|\""+am+"\"\n")
                    allusers.append("\""+bu+"\"|\""+b["Bidder"]["Rating"]+"\"|\""+bl+"\"|\""+bc+"\"\n")
                
            su = item["Seller"]["UserID"].replace('\"', '\"\"')
            sl = item["Location"].replace('\"', '\"\"')
            sc = item["Country"].replace('\"', '\"\"')
            allusers.append("\""+su+"\"|\""+item["Seller"]["Rating"]+"\"|\""+sl+"\"|\""+sc+"\"\n")


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    global allusers, allitems, allbids, allcats
    allusers, allitems, allbids, allcats = [], [], [], []
    it = open("items.dat", "w")
    ut = open("users.dat", "w")
    bt = open("bids.dat", "w")
    ct = open("categories.dat", "w")

    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print( "Success parsing " + f)
    allusers = np.unique(allusers)
    for x in allusers:
        ut.write(x)
    allitems = np.unique(allitems)
    for x in allitems:
        it.write(x)
    allbids = np.unique(allbids)
    for x in allbids:
        bt.write(x)
    allcats = np.unique(allcats)
    for x in allcats:
        ct.write(x)

if __name__ == '__main__':
    main(sys.argv)

