### Connect 4 using tsetlin machines


data = open("Data/connect-4.data")
data_set = []
eof = False
while not eof:
    line_data = data.readline()
    if len(line_data)==0:
        eof=True
    else:
        line_data = line_data.strip()
        line_data = line_data.split(',')
        new_line_data = []
        for e in line_data:
            if e=='b':
                new_line_data.append(-1)
            elif e=='x':
                new_line_data.append(0)
            elif e=='o':
                new_line_data.append(1)
            elif e=="win":
                new_line_data.append(1)
            elif e=="draw":
                new_line_data.append(0)
            else:
                new_line_data.append(-1)
        data_set.append(new_line_data)
for a in range(5):
    print(data_set[a])
