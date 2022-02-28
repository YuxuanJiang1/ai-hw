import sys
import copy
import csv

train_file=""
test_file=""
kmeans_data=""
k=7
unitw=False
strategy='e2'
knn_train,knn_test,km_data=[],[],[]
knn_ans=[]
initial_points=[]
central_points={}
kmeans_ans={}
groups={}#each time added new points belonging to its class
finished=False

def readinput(filename):
    # print("filename:", filename)
    # with open(str(filename)) as f:
    with open(filename) as f:
        reader=csv.reader(f)
        list=[]

        for row in reader:
            list.append(row)
        return list

def compute_dis(a,b):
    if strategy=='e2':
        sum=0
        for i in range(len(a)-1):
            sum+=(int(a[i])-int(b[i]))**2
        return sum

    elif strategy=='manh':
        sum = 0
        for i in range(len(a) - 1):
            sum += abs(int(a[i])-int(b[i]))
        return sum

def putin(a,b):#a[value,class],b[[value,class],[],[]]
    if len(b)<k:
        b.append(a)

        return b
    else:
        if a[0] >=b[-1][0]:
            return b
        else:
            for i in range(len(b)):
                if a[0] < b[i][0]:
                    b.insert(0,a)
                    b=b.pop()
                    return b

def getresult(a):#a[[value,class],[],[]]
    dic={} #[class,vote]
    ans=''
    for i in a:
        if ans=='':
            ans=i[1]
            if unitw==True:

                dic[i[1]]=1
            else:
                dic[i[1]]=1/max(i[0],0.0001)
        else:
            if i[1] not in dic.keys():
                if unitw == True:
                    dic[i[1]] = 1
                else:
                    dic[i[1]] = 1 / max(i[0], 0.0001)
            else:
                if unitw == True:
                    dic[i[1]] += 1
                else:
                    dic[i[1]] += 1 / max(i[0], 0.0001)
    # print(dic)

    maxvote=max(dic.values())
    for i in dic.keys():
        if dic[i]==maxvote:
            return i


def knn():
    dic,dicP,dicR={},{},{}
    knn_train=readinput(train_file)#[[v1,v2,v3,class],[],[]]
    knn_test=readinput(test_file)

    for i in knn_train:
        if i[-1] not in dicR.keys():
            dicR[i[-1]]=1
        else:
            dicR[i[-1]] += 1
    for i in knn_test:
        if i[-1] not in dicP.keys():
            dicP[i[-1]]=1
        else:
            dicP[i[-1]] += 1

            

    for onetest in knn_test:
        mink=[]
        for onetrain in knn_train:
            temp=compute_dis(onetest,onetrain)
            putin([temp,onetrain[-1]],mink)
        # print(mink)
        ans=getresult(mink)
        knn_ans.append(ans)
        print("want="+onetest[-1]+" got="+ans)
        if onetest[-1]==ans:
            if onetest[-1] not in dic.keys():
                dic[onetest[-1]] = 1
            else:
                dic[onetest[-1]] += 1

    #print summary
    for i in sorted(dicR.keys()):
        if i not in dic.keys():
            dic[i]=0
            dicP[i]=0
        precision=str(dic[i])+"/"+str(dicR[i])
        recall=str(dic[i])+"/"+str(dicP[i])
        print("Label="+i+" Precision="+precision+" Recall="+recall)



def new_point(a,b):#a[1,2,3,class]   b{[1,2,3],[2,3,4],[]}
    ans=[]
    # print("a",a)
    # print("b",b)
    for m in range(len(a)-1):
        ans.append(0)

    newb=copy.deepcopy(b)

    for oneb in newb:
        for i in range(len(a) - 1):
            ans[i]+=int(oneb[i])
    # print(ans)
    for mm in range(len(ans)):
        ans[mm]=int(ans[mm])/(len(b))
    return ans

def recompute(length,olddic):#a:{key,[1,2,3,4,5,6]}
    newdic ={}
    for i in olddic.keys():#each centre
        newdic.setdefault(i,[])
        times=len(olddic[i])/length
        # print(times)
        iter=0
        ii=0
        ans=[]
        while ii<int(length):
            ans.append(0)
            ii+=1
        while iter<times:
            for iii in range(len(ans)):
                ans[iii]+=int(olddic[i][iii+iter*length])/times
            iter+=1
        newdic[i]=ans
    return newdic


    return newdic






def kmeans():
    km_data=readinput(kmeans_data)
    finished=False

    global kmeans_ans,central_points

    while finished==False:

        # groups=copy.deepcopy(central_points)
        groups={}
        for i in central_points.keys():
            groups.setdefault(i,[])
        oldans={}

        for i in kmeans_ans.keys():
            oldans.setdefault(i,[])


        for onetest in km_data:
            distances = []#[1,2,3]
            centres=[]
            mind=float("inf")
            closest=''
            for i in central_points.keys():
                onecentre=central_points[i]
                centres.append(onecentre)
            for j in centres:#compute distance between onetest and centres
                temp=compute_dis(onetest,j)
                if temp<mind:
                    mind=temp
                    closest=j

                distances.append(temp)
            # print(distances)

            mindis=min(distances)
            for i in central_points.keys():
                if central_points[i]==closest:# find the closest centre

                    str1=[str(i) for i in onetest[-1]]
                    str2="".join(str1)
                    oldans[i].append(str2)
                    for abc in onetest[:-1]:
                        groups[i].append(abc)

            #recompute central points

            # print(groups)
        groups=recompute(len(onetest)-1,groups)
        # print(central_points)
        # print(kmeans_ans)
        # print(oldans)
        if oldans==kmeans_ans:
            finished=True
        else:#clusters changed
            kmeans_ans=oldans
            central_points=groups




    # print(kmeans_ans)
    for i in kmeans_ans.keys():
        print(i,kmeans_ans[i])
    for j in central_points.keys():
        print(central_points[j])
    # print(central_points)















if __name__ == "__main__":
    if "-k" in sys.argv:
        i = sys.argv.index("-k")
        k = int(sys.argv[i + 1])

    if "-d" in sys.argv:
        i = sys.argv.index("-d")
        strategy = str(sys.argv[i + 1])

    if "-train" in sys.argv:
        i = sys.argv.index("-train")
        train_file = str(sys.argv[i + 1])

    if "-test" in sys.argv:
        i = sys.argv.index("-test")
        test_file = str(sys.argv[i + 1])

    if "-data" in sys.argv:
        i = sys.argv.index("-data")
        kmeans_data = str(sys.argv[i + 1])

    if "-unitw" in sys.argv:
        unitw=True
        print(unitw)
    # readinput("k1 train.txt")
    if 'kNN' in sys.argv:
        knn()
    if 'kMeans' in sys.argv:

        count=0

        while count<k:

            init = sys.argv[-k + count].split(",")
            # print(init)
            count+=1
            central_points['C' + str(count)] = init
            initial_points.append(init)
            kmeans_ans.setdefault('C' + str(count),[])
            # groups.setdefault('C' + str(count),[])
            # groups['C' + str(count)].append(init)
            # print(groups)

        # print(central_points)
        # print(groups)

        kmeans()

