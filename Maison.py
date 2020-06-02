from Structs import *;
class Maison:
    def merge(self,looplist1,looplist2):
        newLoop=[];
        for i in range(len(looplist1)):
            newLoop.append(looplist1[i]);
        for j in range(len(looplist2)):
            newLoop.append((looplist2[j]));
        return newLoop;
    def RemoveDuplicateLoops(self,LoopList,NodeList):
        NumberLoops=len(LoopList);
        for i in range(NumberLoops):
            j=i+1;
            while(j<NumberLoops):
                if(self.IsSameLoop(LoopList[i],LoopList[j])):
                    LoopList.remove(LoopList[j]);
                    NodeList.remove(NodeList[j]);
                    NumberLoops=NumberLoops-1;
                else:
                    j=j+1;
        return LoopList,NodeList;



    def AreTouchingLoops(self,Node1,Node2):
        loop1=len(Node1);
        loop2=len(Node2);
        for i in range(loop1):
            for j in range(loop2):
                if(Node1[i]==Node2[j]):
                    return True;
        return False;
    def CoeffToNum(self,Coeffiecients,Coeff):
        ans=1;
        print(Coeffiecients," s s s ");
        for i in range(len(Coeffiecients)):
            ans*=Coeff[Coeffiecients[i]];
        return ans;



    def CoeffToString(self,Coefficients):
        strMult=f"c{Coefficients[0]}";
        for i in range(1,len(Coefficients)):
            strMult+=f"*c{Coefficients[i]}";

        return strMult;
    Pathup=[];
    Nodesup=[]
    def findpath(self,StartNode,StopNode,Path,Nodes,Net):
            if(StartNode==StopNode and len(Path)>0):
                Nodes.append(StartNode);
                self.Nodesup.append(Nodes[:]);
                self.Pathup.append(Path[:]);
                Nodes.pop();
                return;
            if(Nodes.count(StartNode)!=0):
                return;
            for i in range(len(Net)):
                if(StartNode==Net[i][1]):
                    Path.append(Net[i][0]);
                    Nodes.append(StartNode);
                    self.findpath(Net[i][2],StopNode,Path,Nodes,Net);
                    Nodes.pop();
                    Path.pop();
            return;
    def getAllpaths(self,StartNode,StopNode,Path,Nodes,Net):
        self.Pathup=[];
        self.Nodesup=[];
        self.findpath(StartNode,StopNode,Path,Nodes,Net);
        return self.Pathup[:],self.Nodesup[:];

    def IsSameLoop(self,Loop1,Loop2):
        if(len(Loop1)!=len(Loop2)):
            return False;
        loop1=Loop1[:];
        loop2=Loop2[:];
        loop1.sort();
        loop2.sort();
        for i in range(len(loop1)):
            if(loop1[i]!=loop2[i]):
                return False;
        return True;

    def SumNotTouching(self,L,Pnodes,CoeffName):
        ans=0;
        for i in range(len(L)):
            if not (self.AreTouchingLoops(Pnodes,L[i].Nodes)):
                ans+=self.CoeffToNum(L[i].Coeffs,CoeffName);
        return ans;

    def PrintSumsNotTouching(self,L,Pnodes):
        str="(";
        flag=False;

        for i in range(len(L)):
            if not (self.AreTouchingLoops(Pnodes,L[i].Nodes)):
                str += f"{self.CoeffToString(L[i].Coeffs)}+"
                flag=True;
        str=str[0:-1];
        str+=')';
        if not flag:
            str="0";
        return str;


    def mason(self,Start,Stop,input):
        #taking input coff to Net and symbols to CoeffNames
        Net=[];
        Coeff_names=[];
        for i in range(len(input)):
            Net.append(input[i][0:3]);
            Coeff_names.append(input[i][3]);
        Number_Coeff=len(Coeff_names);
        print(Net);
        print(Coeff_names)
        PathCoeff,PathsNodeList=self.getAllpaths(Start,Stop,[],[],Net);
        #loops First order**

        LoopCoeffList=[];
        LoopNodeList=[];
        for i in range(Number_Coeff):
            Fp,Fn=self.getAllpaths(i,i,[],[],Net);
            if(len(Fp)==0):
                continue;
            Fp,Fn=self.RemoveDuplicateLoops(Fp,Fn);
            for j in range(len(Fp)):
                LoopCoeffList.append(Fp[j]);
                LoopNodeList.append(Fn[j]);

        LoopCoeffList,LoopNodeList=self.RemoveDuplicateLoops(LoopCoeffList,LoopNodeList);
        #-------------------------


        NumberPaths=len(PathCoeff);
        Path=[];
        if(NumberPaths==0):
            print("There Is No Pathing Connecting these Nodes");
            return None;
        #making Path object containg information about each path
        for i in range(NumberPaths):
            p=Struct();
            p.Coeffs=PathCoeff[i];
            p.Nodes=PathsNodeList[i];
            Path.append(p);
        #making Loop object containg information about each path

        Loops =[];
        Loop=[];
        for i in range(len(LoopNodeList)):
            L = Struct();
            L.Nodes = LoopNodeList[i];
            L.Coeffs = LoopCoeffList[i];
            Loops.append(L);

        #loops Contain every loop
        #loop Contain Loops loop[order][NumOfTheLoop]
        Loop.append(Loops);
        # determine nth order loops
        n=0;
        while(True):
            n=n+1;
            Loop.append([]);
            for i in range(len(Loop[0])):
                for j in range(len(Loop[n-1])):
                    if not(self.AreTouchingLoops(Loop[0][i].Nodes,Loop[n-1][j].Nodes)):
                        Duplicate=0;
                        newloopNodes=self.merge(Loop[0][i].Nodes,Loop[n-1][j].Nodes);
                        newloopCoeff=self.merge(Loop[0][i].Coeffs,Loop[n-1][j].Coeffs);

                        for index in range(len(Loop[n])):
                            if(self.IsSameLoop(newloopCoeff,
                                               Loop[n][index].Coeffs)):
                                Duplicate=1;
                                break;
                        if(Duplicate==0):
                            L=Struct();
                            L.Coeffs=newloopCoeff;
                            L.Nodes=newloopNodes;
                            Loop[n].append(L);
            if(len(Loop[n])==0):
                Loop.pop();
                break;


        #Display all the loops found
        for order in range(len(Loop)):
            for i in range(len(Loop[order])):
                print(f"Order:{order+1},"
                      f"Nodes {Loop[order][i].Nodes}",f"Coeff{Loop[order][i].Coeffs}");

        #---------Generate the Final equation
        #Numerator
        Num=0;
        for i in range(len(Path)):
            a=1;
            for order in range(len(Loop)):
                x=self.SumNotTouching(Loop[order],Path[i].Nodes,Coeff_names);
                if(order%2==0):
                    a-=x
                else:
                    a+=x;
                print(x,order,self.CoeffToNum(Path[i].Coeffs,Coeff_names),"zby")
            Num+=a*self.CoeffToNum(Path[i].Coeffs,Coeff_names);


        Den=1;
        for order in range(len(Loop)):
            x=self.SumNotTouching(Loop[order],[-1],Coeff_names);
            if(order%2==0):
                Den-=x;
            else:
                Den+=x;
        print(Den,"Den")

        print(Num,"Num");
        if(Den==0):
            return "Infinity";
        print(Num/Den);
        return Num/Den;





