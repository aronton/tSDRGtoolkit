import re
import os
import average

class paraList1:
    def __init__(self, L_dic, J_dic, D_dic, S_dic):
        # print(L_dic)
        self.set_L(L_dic)
        # print(J_dic)
        self.set_J(J_dic)
        # print(D_dic)
        self.set_D(D_dic)
        # print(S_dic)
        self.set_S(S_dic)
        
    def set_L(self,dic):
        if dic["L1"] == "skip":
            for i in dic:
                dic[i] = "skip" 
            return
        L_dic = {}
        for key,value in dic.items():
            L_dic.update([(key,int(value))])
        if dic["L1"] == dic["L2"] or dic["dL"] == 0:
            self.L_num = [L_dic["L1"]]
            self.L_str = ["L" + str(self.L_num[0])]
            self.L_p_num = [L_dic["L1"],L_dic["L2"],0]
            self.L_p_str = ["L" + str(self.L_num[0]),"L" + str(self.L_num[0]),"L000"]
            return
        self.L_num = [l for l in range(L_dic["L1"], L_dic["L2"]+1, L_dic["dL"])]
        self.L_str = ["L" + str(l) for l in range(L_dic["L1"], L_dic["L2"]+1, L_dic["dL"])]
        self.L_p_str = ["L" + str(L_dic["L1"]), "L" + str(L_dic["L2"]), "L" + str(L_dic["dL"])]
        self.L_p_num = list(L_dic.values())
    def set_J(self,dic):
        if dic["J1"] == "skip":
            for i in dic:
                dic[i] = "skip" 
            return
        # if dic["J1"] == "":
        #     return
        J_dic = {}
        for key,value in dic.items():
            J_dic.update([(key,float(value))])
        if dic["J1"] == dic["J2"] or dic["dJ"] == 0:
            self.J_num = [J_dic["J1"]]
            self.J_s100 = [str(J_dic["J1"])]
            while len(self.J_s100[0]) < 4:
                self.J_s100[0] = self.J_s100[0] + "0"
                # self.J_s100[1] = self.J_s100[1] + "0"
            self.J_s100[0] = self.J_s100[0].replace('.', '')
            # self.J_s100[1] = self.J_s100[1].replace('.', '')
            self.J_str = ["Jdis" + self.J_s100[0]]
            self.J_p_num = [J_dic["J1"],J_dic["J2"],0]
            self.J_p_s100 = self.J_s100.copy()
            self.J_p_str = [str(J_dic["J1"]),str(J_dic["J2"]),"000"]
            return
        numlen = int(round((100*J_dic["J2"]-100*J_dic["J1"])/(100*J_dic["dJ"]),0)+1)
        self.J_num = [round(n*J_dic["dJ"] + J_dic["J1"],2) for n in range(numlen)]
        # self.J_num = [round(n*J_dic["dJ"] + J_dic["J1"],2) for n in range(int((100*J_dic["J2"]-100*J_dic["J1"])/(100*J_dic["dJ"]))+1)]
        # self.J_list = [j for j in range(J_dic["L1"], J_dic["L2"]+1, J_dic["dL"])]
        self.J_s100 = [(str(n) + "0").replace('.', '') if len(str(n)) < 4 else str(n).replace('.', '') for n in self.J_num]
        self.J_str = [ "Jdis" + (str(n) + "0").replace('.', '') if len(str(n)) < 4 else "Jdis" + str(n).replace('.', '') for n in self.J_num]
        
        self.J_p_num =list(J_dic)
        self.J_p_s100 = [ self.J_s100[0], self.J_s100[-1], str(int(100*J_dic["dJ"])) ]
        self.J_p_str = ["Jdis" + n  for n in self.J_s100]
    def set_D(self,dic):
        if dic["D1"] == "skip":
            for i in dic:
                dic[i] = "skip" 
            return
        # if dic["D1"] == "":
        #     return
        D_dic = {}
        for key,value in dic.items():
            D_dic.update([(key,float(value))])
        if dic["D1"] == dic["D2"] or dic["dD"] == 0:
            self.D_num = [D_dic["D1"]]
            self.D_s100 = [str(D_dic["D1"])]
            while len(self.D_s100[0]) < 4:
                self.D_s100[0] = self.D_s100[0] + "0"
                # self.D_s100[1] = self.D_s100[1] + "0"
            self.D_s100[0] = self.D_s100[0].replace('.', '')
            # self.D_s100[1] = self.D_s100[1].replace('.', '')
            self.D_str = ["Dim" + self.D_s100[0]]
            self.D_p_num = [D_dic["D1"],D_dic["D2"],0]
            self.D_p_s100 = [str(D_dic["D1"]),str(D_dic["D2"]),"000"]
            self.D_p_str = ["Dim" + self.D_s100[0],"Dim" + self.D_s100[0],"Dim000"]
            return
        numlen = int(round((100*D_dic["D2"]-100*D_dic["D1"])/(100*D_dic["dD"]),0)+1)
        self.D_num = [round(n*D_dic["dD"] + D_dic["D1"],2) for n in range(numlen)]
        # self.J_list = [j for j in range(J_dic["L1"], J_dic["L2"]+1, J_dic["dL"])]
        self.D_s100 = [(str(n) + "0").replace('.', '') if len(str(n)) < 4 else str(n).replace('.', '') for n in self.D_num]
        self.D_str = [ "Dim" + (str(n) + "0").replace('.', '') if len(str(n)) < 4 else "Dim" + str(n).replace('.', '') for n in self.D_num]
        
        self.D_p_num =list(D_dic)
        self.D_p_s100 = [ self.D_s100[0], self.D_s100[1], str(int(100*D_dic["dD"])) ]
        self.D_p_str = ["Dim" + n for n in self.D_s100]
    def set_S(self,dic):
        if dic["S1"] == "skip":
            for i in dic:
                dic[i] = "skip" 
            return
        # if dic["S1"] == "":
        #     return
        S_dic = {}
        for key,value in dic.items():
            # print(f"value{value}")
            S_dic.update([(key,int(value))])
        if dic["S1"] == dic["S2"]:
            self.S_num = [[dic["S1"],dic["S2"]]]
            self.S_str = [["seed1=" + str(dic["S1"]), "seed2=" + str(dic["S2"])]]
            return
        self.S_num1 = [S_dic["S1"] + n*S_dic["dS"] for n in range(int((S_dic["S2"]-S_dic["S1"]+1)/(S_dic["dS"])))]
        self.S_num2 = [S_dic["S1"]-1 + (n+1)*S_dic["dS"] for n in range(int((S_dic["S2"]-S_dic["S1"]+1)/(S_dic["dS"])))]
        self.S_num = [[self.S_num1[i], self.S_num2[i]] for i in range(len(self.S_num1))]
        self.S_str = [["seed1=" + str(self.S_num1[i]), "seed2=" + str(self.S_num2[i])] for i in range(len(self.S_num1))]
        
class para:
    def __init__(self,task,partitionlist):
        if task == "read":
            self.file = partitionlist
        else:
            self.partitionlist = partitionlist
        if task == "submit":
            self.para = {"Spin":None,"L":{"L1":None,"L2":None,"dL":None},"J":{"J1":None,"J2":None,"dJ":None},\
                 "D":{"D1":None,"D2":None,"dD":None},"S":{"S1":None,"S2":None,"dS":None},\
                 "BC":None,"Pdis":None,"chi":None,"check_Or_Not":None,"Ncore":None,"partition1":None,"task":"submit"}

        elif task == "show":
            self.para = {"Spin":None,"L":{"L1":None,"L2":None,"dL":None},"J":{"J1":None,"J2":None,"dJ":None},\
                 "D":{"D1":None,"D2":None,"dD":None},"S":{"S1":None,"S2":None,"dS":None},\
                 "BC":None,"Pdis":None,"chi":None,"status":None,"Ncore":None,"partition1":None,"task":"show"}

        elif task == "cancel":
            self.para = {"Spin":None,"L":{"L1":None,"L2":None,"dL":None},"J":{"J1":None,"J2":None,"dJ":None},\
                 "D":{"D1":None,"D2":None,"dD":None},"S":{"S1":None,"S2":None,"dS":None},\
                 "BC":None,"Pdis":None,"chi":None,"status":None,"Ncore":None,"partition1":None,"task":"cancel"}

        elif task == "change":
            self.para = {"Spin":None,"L":{"L1":None,"L2":None,"dL":None},"J":{"J1":None,"J2":None,"dJ":None},\
                 "D":{"D1":None,"D2":None,"dD":None},"S":{"S1":None,"S2":None,"dS":None},\
                 "BC":None,"Pdis":None,"chi":None,"check_Or_Not":None,"status":None,"Ncore":None,"partition1":None,"partition2":None,"task":"change"}
                      
        elif task == "dis":
            self.para = {"Spin":None,"L":{"L1":None,"L2":None,"dL":None},"J":{"J1":None,"J2":None,"dJ":None},\
                 "D":{"D1":None,"D2":None,"dD":None},"S":{"S1":None,"S2":None,"dS":None},\
                 "BC":None,"Pdis":None,"chi":None,"status":None,"Ncore":None,"partition1":None,"task":"dis"}
            
        elif task == "collect":
            self.para = {"Spin":None,"L":{"L1":None,"L2":None,"dL":None},"J":{"J1":None,"J2":None,"dJ":None},\
                 "D":{"D1":None,"D2":None,"dD":None},"S":{"S1":None,"S2":None,"dS":None},\
                 "BC":None,"Pdis":None,"chi":None,"partition1":None,"Ncore":None,"task":"collect"}
            
        elif task == "read":
            self.para = {"Spin":None,"L":{"L1":None,"L2":None,"dL":None},"J":{"J1":None,"J2":None,"dJ":None},\
                 "D":{"D1":None,"D2":None,"dD":None},"S":{"S1":None,"S2":None,"dS":None},\
                 "BC":None,"Pdis":None,"chi":None,"status":None,"Ncore":None,"partition1":None}
            self.setfromfile()
            
    def setfromfile(self):    
        parameter = self.parameter_read_dict()
        try:
            self.para["S"] = {"S1":int(parameter["s1"]),"S2":int(parameter["s2"]),"dS":int(parameter["ds"])}
        except ValueError:
            print("value error, set S to skip")
        self.para["L"] = {"L1":int(parameter["L"]),"L2":int(parameter["L"]),"dL":0}
        self.para["J"] = {"J1":float(parameter["J"]),"J2":float(parameter["J"]),"dJ":0}
        self.para["D"] = {"D1":float(parameter["D"]),"D2":float(parameter["D"]),"dD":0}
        self.para["BC"] = parameter["BC"]
        self.para["Pdis"] = int(parameter["Pdis"])
        self.para["chi"] = int(parameter["chi"])                           
    def parameter_read_dict(self):
        parameters = {}
        try:
            with open(self.file, 'r', encoding='utf-8') as file:
                for line in file:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key:
                            parameters[key] = value
        except FileNotFoundError:
            print(f"無法開啟檔案: {self.file}")
        return parameters
            
    def keyin(self):
        for key in self.para.keys():
            eval("self.set_" + key + "()")
    def set_task(self):
        pass
    def set_Spin(self):
        try:
            S = input("key in spin :\n")
            if "." in S:
                S=int(10*float(S))
            else:
                S=int(S)
        except ValueError:
            if S == "":
                self.para["Spin"] = "skip"
                return
            else:
                print("should be interger or enter to skip")
                self.set_Spin()
        self.para["Spin"] = S
    def set_L(self):
        L_dic = self.check_L()
        self.para["L"] = L_dic
        # self.para["L"]["L1"] = L[0]
        # self.para["L"]["L2"] = L[1]
        # self.para["L"]["dL"] = L[2]
    def check_L(self):
        L_list = {"L1":None,"L2":None,"dL":None}
        for key, value in L_list.items():
        # while(len(L_list) < 3):
            try:
                L = input(key+ " : \n")
                L = int(L)
            except ValueError: 
                if L == "":
                   L_list = {"L1":"skip","L2":"skip","dL":"skip"}
                   return L_list
                else:
                    print("should be interger or enter to skip")
                    self.set_L()
            L_list[key] = L
        if L_list["L1"] == L_list["L2"]:
            if L_list["dL"] != 0:
                print("set 3rd to 0 automaticallly")
                L_list["dL"] = 0
            return L_list
        if ((L_list["L2"] - L_list["L1"]) % L_list["dL"]) != 0:
            print("key in error, rekey ")
            self.set_L()
        return L_list
    def set_S(self):
        S_dic = self.check_S()
        self.para["S"] = S_dic
    def check_S(self):
        S_dic = {"S1":None,"S2":None,"dS":None}
        for key, value in S_dic.items():
        # while(len(S_list) < 3):
            try:
                average.getPartitionStatus()
                S = input(key + " : \n")
                S = int(S)
            except ValueError: 
                if S == "":
                   S_dic = {"S1":"skip","S2":"skip","dS":"skip"}
                   return S_dic
                else:
                    self.set_S()
                    print("should be interger or enter to skip")
            S_dic[key] = S
        if S_dic["S1"] % 10 != 1:
            print("1st should be XX1")
            self.check_S()
        if S_dic["S1"] == S_dic["S2"]:
            if S_dic["dS"] != 0:
                print("set 3rd to 0 automaticallly?")
                S_dic["dS"] = 0
            return S_dic
        if ((S_dic["S2"] - S_dic["S1"] + 1) % S_dic["dS"]) != 0:
            print("key in error, rekey ")
            self.set_S()
        return S_dic
    def set_J(self):
        J_dic = self.check_J()
        self.para["J"] = J_dic
        # self.para["J"]["J1"] = J[0]
        # self.para["J"]["J2"] = J[1]
        # self.para["J"]["dJ"] = J[2]
    def check_J(self):
        J_dic = {"J1":None,"J2":None,"dJ":None}
        for key, value in J_dic.items():        
            # while(len(J_list) < 3):
            try:
                J = input(key + " : \n")
                J = float(J)
            except ValueError: 
                if J == "":
                   J_dic = {"J1":"skip","J2":"skip","dJ":"skip"}
                   return J_dic
                else:
                    para.set_J()
                    print("should be interger or enter to skip")
            J_dic[key] = J
        if J_dic["J1"] == J_dic["J2"]:
            if J_dic["dJ"] != 0:
                print("set 3rd to 0 automaticallly")
                J_dic["dJ"] = 0
            return J_dic
        if ((int(100*J_dic["J2"]) - int(100*J_dic["J1"])) % int(100*J_dic["dJ"])) != 0:
            print("key in error, rekey ")
            self.set_J()
        return J_dic
    def set_D(self):
        D_dic = self.check_D()
        self.para["D"] = D_dic

        # self.para["D"]["D1"] = D[0]
        # self.para["D"]["D2"] = D[1]
        # self.para["D"]["dD"] = D[2]
    def check_D(self):
        D_dic = {"D1":None,"D2":None,"dD":None}
        for key, value in D_dic.items():
        # while(len(D_list) < 3):
            try:
                D = input(key + " : \n")
                D = float(D)
            except ValueError: 
                if D == "":
                   D_dic = {"D1":"skip","D2":"skip","dD":"skip"}
                   return D_dic
                else:
                    print("should be float or enter to skip")
                    self.set_D()
            D_dic[key] = D
        if D_dic["D1"] == D_dic["D2"]:
            if D_dic["dD"] != 0:
                print("set 3rd to 0 automaticallly")
                D_dic["dD"] = 0
            return D_dic
        if ((int(100*D_dic["D1"]) - int(100*D_dic["D2"])) % int(100*D_dic["dD"])) != 0:
            print("key in error, rekey ")
            self.set_D()
        return D_dic
    def set_BC(self):
        BC = ""
        while(BC not in {"PBC","OBC"}):
            BC = input("BC? PBC or OBC :\n")
            if BC == "":
                self.para["BC"] = "skip"
                return
        self.para["BC"] = BC
    def set_Pdis(self):
        Pdis = 0    
        while(Pdis not in {"10","20","30"}):
            Pdis = input("distribution 10,20,30 :\n")    
            if Pdis == "":
                self.para["Pdis"] = "skip"
                return
        self.para["Pdis"] = Pdis
    def set_chi(self):
        try:
            chi = input("chi? : \n")
            chi = int(chi)
        except ValueError: 
            if chi == "":
                self.para["chi"] = "skip"
                return
            else:
                print("only int")
                self.set_chi()
        self.para["chi"] = chi
    def set_check_Or_Not(self):        
        check = ""
        while(check not in {"Y","N"}):
            check = input("check? Y or N : \n")
        self.para["check_Or_Not"] = check     
    def set_status(self):        
        status = ""
        while(status not in {"P","R"}):
            status = input("status? R or P : \n")
            if status == "":
                self.para["status"] = "skip"
                return
        self.para["status"] = status  
    def set_Ncore(self):
        status = ""
        try:
            Ncore = input("Ncore? : \n")
            Ncore = int(Ncore)
        except ValueError: 
            if status == "":
                self.para["Ncore"] = "skip"
                return
            print("only int") 
        self.para["Ncore"] = Ncore
    def set_partition1(self):
        if self.para["task"] == "submit" or self.para["task"] == "collect":
            self.setCoreNum()
        # print(self.partitionlsit)
        numOfpartitionlist = list(range(1,len(self.partitionlist)))
        # print(numOfpartitionlist)
        partition1 = 10000      
        while(int(partition1) not in numOfpartitionlist):
            average.getPartitionStatus()
            partition1 = input("partition1 : \n")    
            # partition1 = int(partition1)
            if partition1 == "":
                self.para["partition1"] = "skip"
                return
        
        # print(self.partitionlist[int(partition1)].split()[1])
        self.para["partition1"] = self.partitionlist[int(partition1)].split()[1]
    def set_partition2(self):
        self.setCoreNum()        
        numOfpartitionlist = [int(i) for i, value in enumerate(self.partitionlist)]
        partition2 = 10000    
        while(int(partition2) not in numOfpartitionlist):
            average.getPartitionStatus()
            partition2 = input("partition2 : \n")    
            # partition2 = int(partition2)
            if partition2 == "":
                self.para["partition2"] = "skip"
                return
        self.para["partition2"] = self.partitionlist[int(partition2)].split()[1]        
    def print_param(self, name, values):
        length = len(values)
        min_length = 5  # 设置最小长度阈值
        display_count = min(length, min_length)
        if length > min_length:
            value = str(values[0:min_length]).replace("]","...")
            print(f"{name}:[{value},{len(values)}")
        else:
            value = str(values[:])
            print(f"{name}:[{value}],{len(values)}")

    def setCoreNum(self):
        para=paraList1(self.para["L"],self.para["J"],self.para["D"],self.para["S"])
        if self.para["task"] == "collect":
            # print(self.para["L"])
            # print(self.para["J"])
            # print(self.para["D"])
            self.coreNum = len(para.L_num)*len(para.J_num)*len(para.D_num)*self.para["S"]["dS"]
            # self.print_param("para.L_num", para.L_num)
            # self.print_param("para.J_num", para.J_num)
            # self.print_param("para.D_num", para.D_num)
            print(f"Totalcore = {len(para.L_num)} * {len(para.J_num)} * {len(para.D_num)} = {self.coreNum}")
        if self.para["task"] == "submit":
            # print(self.para["L"])
            # print(self.para["J"])
            # print(self.para["D"])
            # print(self.para["S"])
            self.coreNum = len(para.L_num)*len(para.J_num)*len(para.D_num)*self.para["S"]["dS"]
        
            # self.print_param("para.L_num", para.L_num)
            # self.print_param("para.J_num", para.J_num)
            # self.print_param("para.D_num", para.D_num)
            # self.print_param("para.S_num", para.S_num)

            print(f"Totalcore = {len(para.L_num)} * {len(para.J_num)} * {len(para.D_num)} * {self.para['S']['dS']} = {self.coreNum}")
    def release(self):
        self.new_dic = {}
        for key,value in self.para.items():
            if type(value) != dict:
                self.new_dic.update([(key, str(value))])
            else:
                for key1,value1 in value.items():
                    self.new_dic.update([(key1, str(value1))])

