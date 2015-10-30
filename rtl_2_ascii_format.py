import csv

entrada = open ('SignalStrengthLogger-2015-10-15.csv')
entradareader = csv.reader(entrada)
listaentrada =list(entradareader)

with open("Output.txt", "w") as text_file:
    for item in range(len(listaentrada)):
        aux = listaentrada[item][0].split(";")
        print("{}, {}".format(aux[1], aux[2]), file=text_file)
    
    entrada.close()
                         
