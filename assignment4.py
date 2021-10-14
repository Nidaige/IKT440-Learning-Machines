### Clasify text samples
from sklearn import datasets

def Get_Stop_Words():
    file = open("Data/stop_words.txt")
    words = []
    eof = False
    while not eof:
        word = file.readline().strip()
        if len(word)==0:
            eof=True
        else:
            words.append(word)
    return words




data = datasets.fetch_20newsgroups(data_home=None, subset='train', categories=None, shuffle=True, random_state=42, remove=(), download_if_missing=True, return_X_y=True)
data_dict = {}
stop_words = Get_Stop_Words()
for a in range(1):
    for b in data[a]:
        c = b.split(" ")
        for d in c:
            k=''.join(e for e in d if d.isalnum()).lower()
            if len(k) != 0:
                if k not in data_dict.keys():
                    data_dict[k]="1"
                else:
                    val = int(data_dict[k])
                    val +=1
                    data_dict[k]=str(val)
                current_count = data_dict[k]
print(data_dict)