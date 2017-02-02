import os
import json

traindata = {}

def create():
    cwd = os.getcwd()
    print cwd
    for file in os.listdir(cwd):
        folderlocation = os.path.join(cwd, file)
        if not os.path.isfile(folderlocation):
            for i in os.listdir(folderlocation):
                filename = os.path.join(folderlocation, i)
                with open(filename, 'r') as ip:
                    data = ip.read();
                    if 'Subject:' in data:
                        data.replace('Subject: ','')
                    traindata[data] = file
    with open('train.json','w') as td:
        json.dump(traindata, td)



if __name__ == "__main__":
    create()
