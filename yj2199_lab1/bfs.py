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
            return False
    #print(input[0].X,unvisited)
    #return (input,connection)


def BFS():
    lined={}
    #a dictionary used to record parent nodes.key:current node,value:parent node
    unvisited=[]
    visited=[]
    visited.append('S')

    for i in range(len(input)):
        unvisited.append(input[i].node)
        if input[i].node !='S':
            lined.setdefault(input[i].node,)
    #print(unvisited)
    unvisited.remove('S')
    temp = []
    for j in connect:

        if j.node1=='S' or j.node2=='S':

            #visited[0]='S'
            if j.node1 == 'S':
                temp.append(j.node2)
                lined[j.node2]='S'
                unvisited.remove(j.node2)
            if j.node2=='S':
                temp.append(j.node1)
                unvisited.remove(j.node1)
                lined[j.node1]='S'
    temp.sort()
    for i in temp:
        if i not in visited:
            visited+=i

    #for i in visited:
        #print('Expand:',i)

    if len(unvisited)!=0:
        if len(visited)!=0:
            for m in visited:
                progress=[]
                for n in connect:
                    if n.node1 == m or n.node2 == m:
                        if n.node1 == m and n.node2 not in visited:
                            progress.append(n.node2)
                            lined[n.node2]=m
                            unvisited.remove(n.node2)
                        if n.node2 == m and n.node1 not in visited:
                            progress.append(n.node1)
                            lined[n.node1]=m
                            unvisited.remove(n.node1)
                progress.sort()
                for i in progress:
                    if i not in visited:
                        visited+=i

    if 'G' not in visited:
        print('enable to reach Goal.')
        return 0

    ans=['G']
    start=lined['G']
    for keys in lined.keys():
        if lined[start]!='S':
            ans.append(start)
            start=lined[start]
        else:
            ans.append(start)
            ans.append(lined[start])
            break

    ans=ans[::-1]
    path=''

    for a in range(len(visited)-1):
        print('Expanding:',visited[a])

    for b in range(len(ans)-1):
        path+=str(ans[b])
        path+='->'
    path+='G'
        #print(ans[b],'->',end='')
    #print('G')

    #print (visited)
    #print (lined)
    print (path)


# main function:
if __name__=='__main__':
    a='ex1.txt'
    INPUT(a)
    Flag=INPUT(a)
    if Flag != False:
        BFS()
