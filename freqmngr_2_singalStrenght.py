import csv

frecuencias  = open("ejemplo.txt")
lista_de_frecuencias = list()
for line in frecuencias:
#     print line.rstrip('\n')
    lista_de_frecuencias.append(line.rstrip('\n'))
frecuencias.close()

lista_de_frecuencias = sorted(list(set(lista_de_frecuencias)))

output_file = open('SignalStrengthLogger.csv','w',newline='')
outputWriter = csv.writer(output_file)

for item in lista_de_frecuencias:
    if int(item) <51000000:
        Mode = 'AM'
    if int(item) > 88000000 and int(item) <108000000:
        Mode = 'WFM'
    if item == 120000000:
        Mode = 'AM'
    else:
        Mode = 'NFM'
        
    outputWriter.writerow([item, Mode,'140000','1234567', '0500', '1200','Emi'+item])
    #Freq,Mode,FilterBandwidth,ActiveDays,ActiveTimeFrom,ActiveTimeTo,StationName
output_file.close()

# salida = open ('SignalStrengthLogger.csv')
# salidareader = csv.reader(salida)
# listasalida =list(salidareader)
# print(listasalida)
