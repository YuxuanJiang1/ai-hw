import sys
import copy
from enum import Enum
import collections


df=1.0
hasmin= False
tol=0.01
iter=100

nodes ,ter_nodes,nonter_nodes = set(),set(),set()
types, values, possi, edges = {}, {}, {}, {} # type, value, possbility,edges
nodeadj={}#each value contains a dic

policy,value = None,None
roundcount = 3


NodeType=Enum('NodeType',{'terminal' :0,'transition' : 1,'chance' : 2,'decision' : 3})

def getin(line):
    start = line.split(':')[0].split()[0]
    nodes.add(start.strip())
    end = line.split(':')[1].strip()[1:-1].split(",")
    nodeadj.setdefault(start, {})
    for i in range(len(end)):
        end[i] = end[i].strip()
        if end[i] in ter_nodes:
            nodeadj[start][end[i]]=values[end[i]]

        nodeadj[start].setdefault(end[i],0)
        nodes.add(end[i])
    # when has edge but no possibility, implied p=1
    if len(end) > 0 and start not in possi.keys():
        possi[start] = [1]
    if len(end) == 1:  # single edge=>transition
        types[start] = NodeType(1)
    elif len(possi[start]) == 1:  # multipul edge, one possibility=>decision node
        types[start] = NodeType(3)
    else:  # mul edge,mul possibility=>chance node
        types[start] = NodeType(2)
    edges[start] = end

def readinput(file):
    nonnodes=nonter_nodes
    s_edge = []
    with open(file, 'r') as f:
        for line in f.readlines():
            temp = line.strip().split('/')

            if temp[0]=="#":
                continue
            if ':' in line:
                s_edge.append(line)

            elif '=' in line:
                start = line.split('=')[0].split()[0]
                end = line.split('=')[1].split()[0]
                values[start] = eval(end)
                nodes.add(start.strip())

            elif '%' in line:
                start = line.split('%')[0].split()[0]
                end = line.split('%')[1].split()
                for i in range(len(end)):
                    end[i] = eval(end[i])
                if not isinstance(end, list):
                    end = [end]
                possi[start] = end
                nodes.add(start.strip())

    for line in s_edge:
        getin(line)

    for i in nodes:
        values.setdefault(i, 0)
        if i not in edges.keys():
            ter_nodes.add(i)
            types[i] = NodeType(0)
        else:
            nonter_nodes.add(i)

    for line in s_edge:
        getin(line)


def ValueIteration():
    global value,values

    nowiter=0
    while nowiter<100:
        tempvalues=copy.deepcopy(value)
        nowiter+=1
        for node in nonter_nodes:
            templist=edges[node]#list of adj nodes
            if types[node]==NodeType(2):#chance node
                newvalue=0
                for i in range(len(templist)):

                    temp=value[templist[i]]*possi[node][i]
                    newvalue+=temp
                tempvalues[node]=values[node]+df*newvalue

            if types[node]==NodeType(3):#decision node
                maxvalue=-9999
                chosepossi=possi[node][0]
                if len(templist) == 1:
                    #maxvalue = values[templist[0]]*chosepossi
                    maxvalue = value[templist[0]] * chosepossi
                else:
                    tempvalue=0
                    otherpossi = (1 - chosepossi) / (len(templist) - 1)
                    for adjnode in templist:#choose each node and compare result with maxsum
                        chosen=adjnode
                        notchosen=[]
                        for i in templist:
                            if i!=chosen:
                                notchosen.append(i)
                                #tempvalue+=values[i]*otherpossi
                                tempvalue += value[i] * otherpossi
                        #tempvalue+=values[chosen]*chosepossi
                        tempvalue += value[chosen] * chosepossi

                        maxvalue=max(maxvalue,tempvalue)
                        tempvalue=0
                tempvalues[node]=df*maxvalue
            if types[node]==NodeType(1):#trans
                tempvalues[node]=df*values[edges[node][0]]
        #print("nowiter",nowiter)
        #print(tempvalues)
        value=tempvalues

    
def choosepolicy(policy):
    ans={}
    for node in policy.keys():
        ans.setdefault(node,[])
        edglist=policy[node]
        temp=""
        tempvalue=-99999
        minvalue=99999
        for i in edglist:
            if hasmin == False:
                if values[i]>tempvalue:
                    tempvalue=values[i]
                    temp=i
                pass
            if hasmin == True:
                if values[i]<minvalue:
                    tempvalue=values[i]
                    temp=i
        ans[node]=temp
    return ans





def printresult(values,policy):

    for j in policy.keys():
        print(j,"->", policy[j])
    print()
    for i in values.keys():
        print(i, "=", round(values[i], 5), end=' ')





if __name__ == "__main__":
    if "-df" in sys.argv:
        i = sys.argv.index("-df")
        df = float(sys.argv[i + 1])
    if "-min" in sys.argv:
        hasmin = True
    if "-tol" in sys.argv:
        i = sys.argv.index("-tol")
        tol = float(sys.argv[i + 1])
    if "-iter" in sys.argv:
        i = sys.argv.index("-iter")
        iter = int(sys.argv[i + 1])
    for each in sys.argv:
        if each[len(each) - 3: len(each)] == "txt":
            fileName = each
    #fileName = "input2.txt"
    readinput(fileName)
    #print(possi)
    value=copy.deepcopy(values)
    ValueIteration()

    newpolicy=choosepolicy(edges)
    #print(newpolicy)
    printresult(value,newpolicy)
