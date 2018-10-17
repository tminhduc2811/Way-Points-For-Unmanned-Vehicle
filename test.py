file = open('rawdata2.txt', 'r')
x = file.readline()
file.close()
print(x)
b = x.split('new google.maps.LatLng')
print(b)
c = b[1].split(',')[0].split('(')[1]
temp = []
for i in b:
    if len(i) > 5:
        print(i)
        temp.append([float(i.split(',')[0].split('(')[1]), float(i.split(',')[1].split(')')[0])])
print(temp)
