#!/usr/bin/python3

import sys, datetime, re

def main():
    # Regex to match the lines
    regex_date = "^(\D+\s\D+\s\d+\s\d+\s\d\d:\d\d:\d\d)\s+\d+\s+(....)\s+.+\s+\d+\s+\d+\s+\d+-\d+-\d+\s+(.*)$"
    regex_nodate = "^\s+\d+\s+(....)\s+.+\s+\d+\s+\d+\s+\d+-\d+-\d+\s+(.*)$"
    
    # Open input file
    filename = sys.argv[1]
    lines = open(filename, "r")
    
    # Last date detected, to keep control of multiple entries
    date_last = ""

    for line in lines: 
        line = line.rstrip()
        #print("Original: " + line)
        
        # Check if date line or sub-entry, and parse
        matches = re.search(regex_date,line)
        if matches:
            date_last = parse(matches, 1, date_last)
        if not matches:
            matches = re.search(regex_nodate,line)
            date_last = parse(matches, 0, date_last)
        if not matches:
            print("Error in line!")
            exit()

# Parses a line. Offset set to 1 if line with date, 0 if sub-entry.
def parse(matches, offset, date_last): 
    # Parse date
    if offset == 1:
        date_match = matches.group(1)
        date = datetime.datetime.strptime(date_match, "%a %b %d %Y %H:%M:%S")
        date_seconds = (date - datetime.datetime(1970,1,1)).total_seconds()
    else: 
        date_seconds = date_last

    # Parse M/A/C/B flag to A/M/D
    macb_match = matches.group(1+offset)
    if re.match("..c.",macb_match):
        macb = 'M'
    elif re.match("m...",macb_match):
        macb = 'M'
    elif re.match("...b",macb_match):
        macb = 'A'
    elif re.match(".a..",macb_match):
        macb = 'A'
    elif re.match("....",macb_match):
        macb = 'D'

    # Parse path
    path = matches.group(2+offset)
    # Was it deleted? Cut and set MACB to D(eleted)
    if path.endswith("(deleted)"): 
        path = path[:-10]
        macb = 'D'
        #print(path)
    elif path.endswith("(deleted-realloc)"):
        path = path[:-18]
        macb = 'D'
    # Trim ($FILE_NAME)
    if path.endswith("($FILE_NAME)"):
        path = path[:-13]

    # Print results
    print(str(int(date_seconds)) + "|USER|" + macb + "|" + path)
   
    # Return last date detected
    return date_seconds


if __name__ == "__main__":
    main()
