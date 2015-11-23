import csv


output_file = open('SignalStrengthLogger2.csv','w',newline='')
outputWriter = csv.writer(output_file)

for i in range(518000000, 525000000, 1000000):
    Mode = 'NFM'
    outputWriter.writerow([i, Mode,'14000','1234567', '0500', '2100','Emi'+str(i)])
    #Freq,Mode,FilterBandwidth,ActiveDays,ActiveTimeFrom,ActiveTimeTo,StationName
output_file.close()
