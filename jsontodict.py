import json

def jsontodict(JSONfile):
    with open('Graphs/'+JSONfile) as json_file:
        data = json.load(json_file)
        DAG={}
        for i in data["nodes"]:
            l = data["nodes"][i]["Dependencies"]
            for j in range(len(l)):
                l[j] = str(l[j])
            DAG[i]=[timeInSecond(data["nodes"][i]["Data"]) , l]
    return DAG

def timeInSecond(timeInStr):
    second=0
    second+=float(timeInStr[0:2])*3600 + float(timeInStr[3:5])*60 + float(timeInStr[6:])
    return second

#a=jsontodict('smallComplex.json')
#print(a)