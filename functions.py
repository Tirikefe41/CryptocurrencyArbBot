import json

def readJson(filename):
    # file = open('static/'+filename+'.json', 'r')
    # r = file.read()
    # file.close()
    with open('static/'+filename+'.json', 'r') as read_file:
        data = json.load(read_file)
    return data

def jsonAdd(filename, data_dict):
    d = readJson(filename)
    d.append(data_dict)
    jsonWrite(filename, d)

def jsonWrite(filename, data_dict):
#     file = open('static/'+filename+'.json', 'w')
#     file.write(json.dumps(data_dict))
#     file.close()
    with open('static/'+filename+'.json', 'w') as write_file:
        json.dump(data_dict, write_file, default=str)
        write_file.close()