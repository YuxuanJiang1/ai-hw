import copy
class position:#the input information of position
    def __init__(self, node,X,Y):
        self.node=node
        self.X=X
        self.Y=Y

class connection:#the input information of connection
    def __init__(self, node1,node2):
        self.node1=node1
        self.node2=node2
input=[]
connect=[]



def INPUT(a):
    unvisited=[]
    flag=0
    with open(a, 'r') as f:
        for line in f.readlines():
            temp = line.strip().split()
            # print (temp)
            if len(temp) == 3:
                if temp[0] != '#':
                    node = temp[0]
                    X = temp[1]
                    Y = temp[2]
                    input.append(position(node, X, Y))

            if len(temp) == 2:
                if temp[0] != '#':
                    node1 = temp[0]
                    node2 = temp[1]
                    connect.append(connection(node1, node2))
    Node = []
    for i in range(len(input)):
        Node.append(input[i].node)
    for j in range(len(connect)):
        if connect[j].node1 not in Node or connect[j].node2 not in Node:
            print('input error')

    #print(input[0].X,unvisited)
    #return (input,connection)

deld={}

#current=[]
def dfs(a,d,depth,visited,path):
    if a=='G':
        path.append('G')
        print(path)
        return True


    else:
        if d==0:
            current= copy.deepcopy(next1[a])
            temp=copy.deepcopy(current)
            for m in temp:
                if m in visited:
                    current.remove(m)
            current.sort()
            if len(current)>0:
                visited.append(a)
                print('Expand', a)
                path.append(a)
                j=current[0]

                return dfs(j,len(path),depth,visited,path)



        if 0<d < depth:
            current=copy.deepcopy(next1[a])
            temp = copy.deepcopy(current)
            for m in temp:
                if m in visited:
                    current.remove(m)
            current.sort()


            if len(current)>0:
                if a not in visited:
                    visited.append(a)
                    print ('Expand',a)
                    path.append(a)
                j=current[0]
                return dfs(j,len(path),depth,visited,path)
                #print (j)
            if len(current)==0:
                if a not in visited:
                    visited.append(a)
                    print('Expand', a)
                else:
                    path.remove(a)
                    if len(path)==0:
                        return False

                return dfs(path[-1],len(path),depth,visited,path)

        if d==depth:
            visited.append(a)
            print('hit depth=', depth, ':', a)

            b=path[-1]

            current=copy.deepcopy(next1[b])
            #print ('next1',next1[b])
            temp=copy.deepcopy(current)
            for m in temp:
                if m in visited:
                    current.remove(m)
            current.sort()

            if len(current)>0:
                x=current[0]
                return dfs(x,len(path),depth,visited,path)



            if len(current)==0:
                path.remove(b)
                #print (visited[-1],len(visited),unvisited)
                return dfs(path[-1],len(path),depth,visited,path)




    #print(visited)


next1={}#key: node,value:a list contain all next nodes

unvisited=[]
def IDP():
    depth = 2

    d=0
    temp1 = []
    for i in range(len(input)):
        if i !='S':
            temp1.append(input[i].node)
    temp1.sort()
    temp1.remove('S')
    for j in temp1:
        unvisited.append(j)
    unvisited.insert(0,'S')

    for j in unvisited:
        next1.setdefault(j,[])
        temp = []
        for m in connect:

            if m.node1==j or m.node2==j:
                if m.node1==j:
                    temp.append(m.node2)
                if m.node2==j:
                    temp.append(m.node1)
        temp.sort()
        for n in temp:
            next1[j].append(n)
    #print(next1)


    #print (visited)

    Flag=dfs('S',0,depth,[],[])
    while Flag==False:
        depth+=1
        Flag=dfs('S', 0, depth, [], [])



# main function:
if __name__ == '__main__':
    a = 'ex1.txt'
    INPUT(a)
    Flag = INPUT(a)
    if Flag != False:
        IDP()
