import os
import math
import pandas as pd
import wget

atlas = pd.read_csv("notebooks/finderChart/atlas.csv")
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
def search(id):
    for i in range(len(objidA)):
        if id == objidA[i]:
            ra = raA[i]
            dec = decA[i]
            print(f'Ra={ra}, Dec={dec}')
            id = id.replace(' ', '_')
            return (id, ra, dec)
    print(f'Error: search()\nInvalid id: {id}')
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

# downloads file, if not already downloaded
def grab(id):
    id, ra, dec = search(id)
    website = (makeWeb(roundCords(ra),roundCords(dec)))
    
    # adds all file names in 'results' in a list
    results = []
    for file_path in os.listdir('notebooks/finderChart/results'):
        if os.path.isfile(os.path.join('notebooks/finderChart/results', file_path)):
            results.append(file_path)

    #checks if the pdf is already downloaded
    if (id+'.pdf') in results:
        print(f'{id}.pdf already in results folder\n')
    else:
        print('Grabbing...')
        wget.download(website, f'{id}.pdf')
        os.rename(f'{id}.pdf', f'notebooks/finderChart/results/{id}.pdf')
        print(f'\nDownloaded: {id}.pdf\n')

# takes ids in listOfIds.txt into a list
def listOut():
    list = []
    myfile = open("notebooks/finderChart/listOfIds.txt", "rt")
    contents = myfile.read() + '\n'
    myfile.close()
    trys = 0
    while len(contents) > 0:
        index = contents.find('\n')
        id = contents[0:index]
        list.append(id)
        contents = contents[index+1:]
    return(list)


# ask = input('Single search? (y/n)\n')
# if ask == 'y':
#     id = input('Enter object ID: ')
#     grab(id)
# elif ask == 'n':
listOfIds = listOut()
if len(listOfIds) > 0:
    for obj in range(len(listOfIds)):
        grab(listOfIds[obj])
else:
    print('No ids in the ')
# else:
#     print('Invalid input')