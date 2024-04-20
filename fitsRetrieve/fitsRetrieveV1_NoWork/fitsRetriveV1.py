import os
import math
import random
import pandas as pd
import wget

## File paths
atlasFile = 'atlas.csv'
listFile = 'listOfIds.txt'
webFile = 'websites.txt'
resultsFolder = 'results'

atlasFile = pd.read_csv(atlasFile)
starter = 'https://irsa.ipac.caltech.edu/SIA?COLLECTION=spitzer_sha&RESPONSEFORMAT=FITS&POS=circle'

# Convert Panda series to arrays
objidA = pd.Series(atlasFile['objid']).array
raA = pd.Series(atlasFile['ra']).array
decA = pd.Series(atlasFile['dec']).array

# initializers
ra, dec = 0, 0
id = '0'
websites = []

# Asks for Object ID, then returns ra and dec of the object is available
# If not available, display error and ends program
# Edit: replaces spaces in ID with underscores
def search(id):
    for i in range(len(objidA)):
        if id == objidA[i]:
            ra = raA[i]
            dec = decA[i]
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
    endP = f'{starter}+{r}+{d}+0.002777'
    return(endP)

# makes the website and adds to a list
def makeEntry(id):
    id, ra, dec = search(id)
    website = (makeWeb(roundCords(ra),roundCords(dec)))
    check = False

    #checks if the entry is already made
    for i in websites:
        if i[0] == id:
            check = True

    if check:
        print(f'{id} entry already in listOfIds.txt file')
    else:
        print(f'{id} entry made!')
        entry = [id, ra, dec, website]
        websites.append(entry)
    return(websites)

# clears txt and writes all entries
def createTXT(websites):
    wordsInFile = ''
    for entry in websites:
        wordsInFile = wordsInFile + f'ID:{entry[0]}\nRA:{entry[1]} DEC:{entry[2]}\n{entry[3]}\n\n'
    f = open(webFile,'w')
    f.write(wordsInFile)
    f.close
    print('Updated File!\n')

# takes ids in listOfIds.txt into a list
def listOut():
    list = []
    myfile = open(listFile, "rt")
    contents = myfile.read() + '\n'
    myfile.close()
    while len(contents) > 0:
        index = contents.find('\n')
        id = contents[0:index]
        list.append(id)
        contents = contents[index+1:]
    return(list)

#makes a number of random obj #s
def randomIds(randomN):
    for i in range(randomN):
        websites = makeEntry(objidA[random.randrange(0, len(objidA))])
    return(websites)

# Downloads links
def grab(web):
    id = web[0]
    link = web[3]

    # adds all file names in 'results' in a list
    results = []
    for file_path in os.listdir(resultsFolder):
        if os.path.isfile(os.path.join(resultsFolder, file_path)):
            results.append(file_path)

    #checks if the pdf is already downloaded
    if (id+'.fits') in results:
        print(f'{id}.fits already in results folder\n')
    else:
        print('Grabbing...')
        wget.download(link, f'{id}.fits')
        os.rename(f'{id}.fits', f'{resultsFolder}/{id}.fits')
        print(f'Downloaded: {id}.fits\n')


# Random links option
def randomLinks():
    num = input('How many links: ')
    if num.isdigit:
        websites = randomIds(math.floor(int(num)))
        createTXT(websites)
        grabbing = input('Download links?(y/n): ')
        if grabbing.lower() == 'y':
            for i in range(len(websites)):
                grab(websites[i])
            print('Downloaded!')
    else:
        print('Invalid')

# Provided List option
def nonRandomLinks():
    listOfIds = listOut()
    for obj in range(len(listOfIds)):
        websites = makeEntry(listOfIds[obj])
    createTXT(websites)
    grabbing = input('Download links?(y/n): ')
    if grabbing.lower == 'y':
        for i in len(websites[i]):
            grab(websites)

### Program starts here ###
start = input('Random links?(y/n): ')
if start.lower() == 'y':
    randomLinks()
elif start.lower() == 'n':
    nonRandomLinks()
else:
    print('Invalid')