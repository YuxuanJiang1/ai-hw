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

class opennode:
    def __init__(self,path1,g,h,f):
        self.path1=path1
        self.g=g
        self.h=h
        self.f=f



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

def distance(a,b):
    ax,ay,bx,by=0,0,0,0
    for i in range(len(input)):
        if input[i].node==a:
            ax=float(input[i].X)
            ay =float(input[i].Y)
        if input[i].node == b:
            bx = float(input[i].X)
            by = float(input[i].Y)
    dis=((abs(ax)-abs(bx))**2+(abs(ay)-abs(by))**2)**0.5
    return round(dis,2)
disdic={}
next1 = {}  # key: node,value:a list contain all next nodes
visited=[]
path=[]
cost={}
#key: path, value: h+g of the path
opened=['S']
closed=[]
S=opennode('S',0,distance('S','G'),distance('S','G'))
closed.append(S)
#print(closed[-1].path1[-1])
def A():
    unvisited = []
    temp1 = []
    for i in range(len(input)):
        if i != 'S':
            temp1.append(input[i].node)
    temp1.sort()
    temp1.remove('S')
    for j in temp1:
        unvisited.append(j)
    unvisited.insert(0, 'S')

    for j in unvisited:
        next1.setdefault(j, [])
        temp = []
        for m in connect:

            if m.node1 == j or m.node2 == j:
                if m.node1 == j:
                    temp.append(m.node2)
                if m.node2 == j:
                    temp.append(m.node1)
        temp.sort()
        for n in temp:
            if n not in next1[j]:
                next1[j].append(n)
    for i in range(10000):
        while len(opened)==0:
            print('No solution')
            return 0

        else:
            mmm = closed[-1].path1[-1]


                #mmm = closed[-1].path1[-1]

            b=copy.deepcopy(next1[mmm])
            c=copy.deepcopy(b)
            alln=closed[-1].path1.split('->')

            for m in b:
                if m in alln:
                    c.remove(m)

            for i in c:
                g=round(distance(mmm,i)+closed[-1].g,2)
                #disdic[a,i]=g
                h=distance(i,'G')
                f=round(g+h,2)
                path1=closed[-1].path1+'->'+i
                opened.append(opennode(path1,g,h,f))
                print(path1,'g=',g,'h=',h,f)
            if mmm in opened:
                opened.remove(mmm)
            closed.append(mmm)
            adding=[]
            minf=min([i.f for i in opened])
            for nn in opened:
                if nn.f==minf:
                    adding.append(nn)
            if len(adding)>1:
                added=[]
                minh=min([i.h for i in adding])
                for mm in adding:
                    if mm.h==minh:
                        added.append(mm)
                        break
                print('adding:',added[0].path1)
                candi=added[0].path1[-1]
                opened.remove(added[0])
                closed.append(added[0])
            if len(adding)==1:
                print('adding:', adding[0].path1)
                candi = adding[0].path1[-1]
                opened.remove(adding[0])
                closed.append(adding[0])
            #print(closed[-1][-1])

            mmm= closed[-1].path1[-1]


            if mmm == 'G':
                print('Solution:',closed[-1].path1)
                return 1



















# main function:
if __name__ == '__main__':

    a = 'ex2.txt'
    INPUT(a)

    Flag = INPUT(a)
    if Flag != True:
        A()
