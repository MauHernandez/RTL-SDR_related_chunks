import csv
import os

CHUNK =  7
DATE = '2015/10/15'
LAT = '8.557924'
LONG = '-71.207730'
FOLDER_NAME = 'parsed'

entrada = open ('SignalStrengthLogger-2015-11-18.csv')
entradareader = csv.reader(entrada)
listaentrada =list(entradareader)

def split_lines(lines, n):

    for i in range(0, len(lines), n): #python3 range
        yield lines[i: i+n]
#     except NameError: 
#         for i in xrange(0, len(lines), n): #python2 xrange
#             yield lines[i: i+n]

def make_sure_path_exists_and_delete_content(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_lines(lines):    
    for item in range(len(lines)):
        aux = lines[item][0].split(";")
        yield("{}\t{}".format(aux[1], aux[2]))
        

make_sure_path_exists_and_delete_content('./' + FOLDER_NAME)


for index, lines in enumerate(split_lines(listaentrada, CHUNK)):
    with open(FOLDER_NAME+'/'+str(index)+'.txt', 'w+') as f: 
        f.write('\n'.join(clean_lines(lines)))
        f.write('\n'+LAT)
        f.write('\n'+LONG)
        f.write('\n'+DATE)
    
entrada.close()
