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
print(len(data[0]))
articles = data[0]
for text in articles:
    words = text.split(" ")
    for word in words:
        clean_word=''.join(e for e in word if word.isalnum()).lower()
        if len(clean_word) != 0:
            if clean_word not in data_dict.keys():
                data_dict[clean_word]="1"
            else:
                val = int(data_dict[clean_word])
                val +=1
                data_dict[clean_word]=str(val)
            current_count = data_dict[clean_word]
print(data_dict)