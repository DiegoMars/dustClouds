list = []
myfile = open("notebooks/finderChart/listOfIds.txt", "rt")
contents = myfile.read() + '\n'
myfile.close()
trys = 0
while len(contents) > 0 or trys > 10:
    index = contents.find('\n')
    id = contents[0:index]
    list.append(id)
    contents = contents[index+1:]
    trys += 1

print(list)