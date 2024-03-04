import subprocess
import math
import pandas as pd
import wget

atlas = pd.read_csv('atlas.csv')
starter = 'https://irsa.ipac.caltech.edu/applications/finderchart/servlet/api?mode=getImage&file_type=pdf&subsetsize=1.0&marker=true'

# Convert Panda series to arrays
objidA = pd.Series(atlas['objid']).array
raA = pd.Series(atlas['ra']).array
decA = pd.Series(atlas['dec']).array
ra, dec = 0, 0
id = '0'

# Asks for Object ID, then returns ra and dec of the object is available
# If not available, display error and ends program
# Edit: replaces spaces in ID with underscores
def search():
    id = input("Enter object ID: ")
    for i in range(len(objidA)):
        if id == objidA[i]:
            ra = raA[i]
            dec = decA[i]
            print(f'Ra={ra}, Dec={dec}')
            id = id.replace(' ', '_')
            return (id, ra, dec)
    print('Error: search()\nInvalid id')
    exit()

# Rounds input to the 5th decimal and outputs string
def roundCords(num):
    temp = (num*100000)+0.5
    temp = math.floor(temp)
    temp = str(float(temp)/100000)
    return(temp)

# Outputs website
def makeWeb(r, d):
    endP = starter + '&RA=' + r + '&DEC=' + d
    print(f'Website:\n{endP}')
    return(endP)

# Used to run commands
def runcmd(cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


id, ra, dec = search()
website = (makeWeb(roundCords(ra),roundCords(dec)))
runcmd(f'wget --output-document={id}.pdf {website}', verbose = True)
runcmd(f'mv {id}.pdf results')