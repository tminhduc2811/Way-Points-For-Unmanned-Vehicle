import utm
import numpy as np
import pandas as pd

df = pd.DataFrame({'X-Path': [], 'Y-Path': [], 'X-Vehicle': [], 'Y-Vehicle': []})


def export_to_xlsx(path):
    print('Exporting way points to xlsx')
    writer = pd.ExcelWriter(path)
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


def parse_raw_data(path):
    print('Parsing raw data...')
    f = open(path, 'r')
    x = f.readline()
    xs = x.split('new google.maps.LatLng')
    t = []
    for m in xs:
        if len(m) > 3:
            t.append([float(m.split(',')[0].split('(')[1]), float(m.split(',')[1].split(')')[0])])
    t.append(t[0])
    return t


STEP = 0.2
list_latlon = parse_raw_data('rawdata2.txt')
list_coordinates = []
xpoints = []
ypoints = []
for i in range(len(list_latlon)):
    temp1 = utm.from_latlon(list_latlon[i][0], list_latlon[i][1])
    list_coordinates.append([temp1[0], temp1[1]])

# # Create way points
for i in range(len(list_coordinates)):
    if i > 0:
        a = (list_coordinates[i][1] - list_coordinates[i-1][1])/(list_coordinates[i][0]-list_coordinates[i-1][0])
        b = list_coordinates[i][1] - a*list_coordinates[i][0]
        # y = ax + b
        if list_coordinates[i][0] >= list_coordinates[i-1][0]:
            temp = np.arange(list_coordinates[i-1][0], list_coordinates[i][0], STEP)
            for j in temp:
                xpoints.append(j/1000)
                ypoints.append((a*j + b)/1000)

        else:
            temp2 = np.arange(list_coordinates[i][0], list_coordinates[i-1][0], STEP)
            for k in range(len(temp2)):
                xpoints.append(temp2[len(temp2)-k-1]/1000)
                ypoints.append((a * temp2[len(temp2)-k-1] + b)/1000)
df['X-Path'] = xpoints
df['Y-Path'] = ypoints
export_to_xlsx('map2.xlsx')