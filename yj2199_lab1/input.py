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
            #print (temp)
            if len(temp)==3:
                if temp[0]!='#':
                    node= temp[0]
                    X= temp[1]
                    Y = temp[2]
                    input.append(position(node,X,Y))

            if len(temp)==2:
                if temp[0] != '#':
                    node1=temp[0]
                    node2=temp[1]
                    connect.append(connection(node1,node2))
        Node=[]
        for i in range(len(input)):
            Node.append(input[i].node)
        for j in range(len(connect)):
            if connect[j].node1 not in Node or connect[j].node2 not in Node:
                print('input error')

if __name__=='__main__':
    INPUT('ex1.txt')
    for i in range(len(input)):
        print (input[i].node)
    for j in range(len(connect)):
        print (connect[j].node1)