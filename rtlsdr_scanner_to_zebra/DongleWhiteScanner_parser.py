import glob
import os
import json
import datetime, csv
import xml.dom.minidom
from xml.dom.minidom import parse


"""
Get a CVS file and a a GPX  file and merge data into a JSON accepted file in Zebra app
"""

__author__ = "Maureen Hernandez"
__version__ = "1"


FOLDER_NAME = 'parsed'
FILE_NAME = 'zebra_parsed'
EXTENSION = 'json'


class Info:
    def __init__(self, *args, **kwargs):
        self.parsed = 0
        self.samples = 0
        self.status = ""

    def print_info(self):
        print "Number of samples: " + str(self.samples + 1)
        print "Number of files parsed: " + str(self.parsed)
        print self.status


def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


def save_place(place):
    with open(FOLDER_NAME + '/' + FILE_NAME + '.' + EXTENSION, 'wb') as fp:
        json.dump(place, fp)
    return True


def exist_gpx(name, file_list_gpx):
    name_of_file = name+'.gpx'
    if name_of_file in file_list_gpx:
        return True
    else:
        return False

def parse_file():
    check_path('./' + FOLDER_NAME)
    info = Info()
    info.status = "parsing"
    frequencies_cmp = set()

    file_list = glob.glob("*.csv")
    file_list_gpx = glob.glob("*.gpx")

    place = {
        "frequencies": {
            "values": []
        },
        "coordinates": []
    }

    for filename in file_list:
        aux = 0
        frequencies = []
        captures = []
        name_to_cmp = ''
        init_time = ''
        time_stamp = ''

        each_file = open(filename, 'r')
        name_to_cmp = os.path.splitext(each_file.name)[0]

        if exist_gpx(name_to_cmp, file_list_gpx):

            domtree = xml.dom.minidom.parse(name_to_cmp+".gpx")
            collection = domtree.documentElement
            sweep = collection.getElementsByTagName("trkpt")

            my_csv_file = csv.DictReader(each_file)
            init_time = float(next(my_csv_file).values()[0])
            time_stamp = (datetime.datetime.utcfromtimestamp(init_time).isoformat()) + 'Z'

            each_file.seek(0)
            next(my_csv_file)

            for row in my_csv_file:
                frequencies.append(float(row[' Frequency (MHz)']))
                captures.append(float(row['Level (dB/Hz)']))
                if str(init_time) != str(row['Time (UTC)']):
                    info.samples += 1
                    if len(frequencies_cmp) == 0:
                            frequencies_cmp = set(frequencies)
                            place["frequencies"]["values"] = sorted(frequencies_cmp)
                    for place_x in sweep:
                        latitude = ''
                        longitude = ''
                        if str(time_stamp) == str(place_x.getElementsByTagName('time')[0].childNodes[0].data):
                            lat = str(place_x.getAttribute("lon"))
                            lng = str(place_x.getAttribute("lat"))

                            place["coordinates"].append({
                                "lat": float(lat),
                                "lng": float(lng),
                                "date": datetime.datetime.fromtimestamp(float(init_time)).strftime('%Y-%m-%d %H:%M:%S'),
                                "cap": captures[:-1]
                            })
                            break
                        continue

                    #actualizamos variables de tiempo
                    aux = captures[-1]
                    captures = []
                    captures.append(aux)
                    init_time = row['Time (UTC)']
                    time_stamp = (datetime.datetime.utcfromtimestamp(float(init_time)).isoformat()) + 'Z'

        each_file.close()
        info.parsed += 1

    print(place["coordinates"])
    info.status = "saving"
    info.print_info()

    save_place(place)
    info.status = "DONE"
    info.print_info()


if __name__ == '__main__':
    parse_file()
