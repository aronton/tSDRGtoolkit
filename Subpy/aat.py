import os
import math
import time
import timeit
import sys
import tarfile
import datetime
import multiprocessing
import scriptCreator
from pathlib import Path
import shutil


tSDRG_path = "/home/aronton/tSDRG_random"
group_path = "/ceph/work/NTHU-qubit/LYT/tSDRG_random"

    
sourcelist = {"ZL":"ZL.csv", "energy":"energy.csv", "seed":"s_re_seed.csv",\
    "corr1":"_".join(["L_re","P_re","m_re","s_re","corr1.csv"]), "corr2":"_".join(["L_re","P_re","m_re","s_re","corr2.csv"]),\
    "ZLI":"ZLI.csv", "ZLC":"ZLC.csv", "w_loc":"w_loc.csv", "J_list":"J_list.csv", "dimerization":"dimerization.csv",\
    "string":"_".join(["L_re","P_re","m_re","s_re","string.csv"])
    }

grouplist = {"ZL":"_".join(["L_re","P_re","m_re","s_re","ZL.txt"]), "energy":"_".join(["L_re","P_re","m_re","s_re","energy.txt"]),\
    "corr1":"_".join(["L_re","P_re","m_re","s_re","corr1.txt"]), "corr2":"_".join(["L_re","P_re","m_re","s_re","corr2.txt"]),\
    "ZLI":"_".join(["L_re","P_re","m_re","s_re","ZLI.txt"]), "ZLC":"_".join(["L_re","P_re","m_re","s_re","ZLC.txt"]),\
    "w_loc":"_".join(["L_re","P_re","m_re","s_re","w_loc.txt"]), "J_list":"_".join(["L_re","P_re","m_re","s_re","J_list.txt"]),\
    "string":"_".join(["L_re","P_re","m_re","s_re","string.txt"]), "seed":"_".join(["L_re","P_re","m_re","s_re","seed.txt"]),\
    "dimerization":"_".join(["L_re","P_re","m_re","s_re","dimerization.txt"])
    }

tarlist = {
    "ZL":"_".join(["ZL","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "energy":"_".join(["energy","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "corr1":"_".join(["corr1","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "corr2":"_".join(["corr2","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "ZLI":"_".join(["ZLI","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "ZLC":"_".join(["ZLC","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "w_loc":"_".join(["w_loc","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "J_list":"_".join(["J_list","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "string":"_".join(["string","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "seed":"_".join(["seed","L_re","P_re","m_re.txt"]),
    "dimerization":"_".join(["dimerization","L_re","P_re","m_re.txt"])
    }


# collist = {
#     "ZL":"_".join(["ZL","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "energy":"_".join(["energy","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "corr1":"_".join(["corr1","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "corr2":"_".join(["corr2","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "ZLI":"_".join(["ZLI","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "ZLC":"_".join(["ZLC","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "w_loc":"_".join(["w_loc","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "J_list":"_".join(["J_list","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "string":"_".join(["string","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
#     "seed":"_".join(["seed","L_re","P_re","m_re","s_re.txt"]),
#     "dimerization":"_".join(["dimerization","L_re","P_re","m_re","s_re.txt"])
#     }

def parameterRead(filePath):
    with open(filePath,"r") as a:
        a = a.readlines()    
        for i,v in enumerate(a):
            key = v.split(":")[0]
            value = v.split(":")[1]
            if key in paralist:
                paralist[key] = value 
            

def checkInside(s, f, sample, phys):
    with open(f,"r") as a:
        a = a.readlines()    
        if a[0].strip() == phys:
            del a[0]
        data = [(v.split(":")[0].strip(),(v.split(":")[1].replace("\n"," ").strip())) for i,v in enumerate(a)]
        sorted_data = sorted(data, key=lambda x: int(x[0]))
    if s == sorted_data[sample+1][1]:
        return True
    else:
        return False


def compare(f1,f2,sample):
    with open(f1,"r") as a:
        a = a.readlines()
    with open(f2,"r") as b:
        b = b.readlines()
    if (len(a) <= 2) and (len(b) <=2 ):
        return (a == b)
    elif (len(a) > 2) and (len(b) > 2 ):
        return (a == b)
    elif (len(a) <= 2) and (len(b) > 2 ):
        if len(a) == 2:
            del a[0]
            data1 = a[0].strip()
            # print(data1)
        else:
            data1 = a[0].strip()
            # print(data1)
        del b[0]
        
        for i,v in enumerate(b):
            # print(v.split(":")[0])
            # print(v.split(":")[1])
            if data1 in v.strip():
                if v.split(":")[0] == sample:
                    return True
        return False
    elif (len(a) > 2) and (len(b) < 2 ):
        if len(b) == 2:
            del b[0]
            data1 = b[0].strip()
        else:
            data1 = b[0].strip()
        del a[0]
        for i,v in enumerate(a):
            if data1 in v.strip():
                if v.split(":")[0] == sample:
                    return True
        return False
def checkFileNum(dirpath):
    folder = Path(dirpath) 
    file_count = sum(1 for f in folder.iterdir() if f.is_file())
    return file_count

def creatName(BC, J, D, L, P, m, phys):
    mySourceName = sourcelist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    myTargetName = tarlist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    groupSourceName = grouplist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    groupTargetName = tarlist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    return (mySourceName, groupSourceName, myTargetName, groupTargetName)

def creatCpName(BC, J, D, L, P, m, phys):
    CpName = newlist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    return CpName
def creatColName(BC, J, D, L, P, m, phys):
    colName = collist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    return colName
def creatDir(BC, J, D, L, P, m, phys):
    sourcePath = "/".join(["tSDRG","Main_15","data_random","BC_re","J_re","D_re","L_re_P_re_m_re_s_re"])
    tarPath = "/".join(["tSDRG","Main_15","data_collect","BC_re","J_re","D_re","L_re_P_re_m_re"])
    mySourcePathBase = "/".join([tSDRG_path,sourcePath])
    groupSourcePathBase = "/".join([tSDRG_path,sourcePath])
    myTargetPathBase = "/".join([tSDRG_path,tarPath])
    groupTargetPathBase = "/".join([tSDRG_path,tarPath])
    # sourcePathBase = f"{tSDRG_path}/tSDRG/Main_15/data_random/BC_re/J_re/D_re/L_re_P_re_m_re_s_re/"
    # cpPathBase = f"{group_path}/tSDRG/Main_15/data_random/BC_re/J_re/D_re/L_re_P_re_m_re_s_re/"
    # targetPathBase = f"{group_path}/tSDRG/Main_15/data_collect/BC_re/J_re/D_re/L_re_P_re_m_re/"

    mySourcePath = mySourcePathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    groupSourcePath = groupSourcePathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    myTargetPath = myTargetPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    groupTargetPath = groupTargetPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)

    # cpPath = cpPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    # targetPath = targetPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    
    return (mySourcePath, groupSourcePath, myTargetPath, groupTargetPath)

def fread(f, phys):
    if os.path.exists(f):
        with open(f,"r") as a:
            a = a.readlines()
            if len(a) == 0:
                return 
            else:
                if phys in a[0].strip():
                    del a[0]
                a = "".join(a)
                a = a.replace("\n"," ")
                return a
    else:
        return 

def create_tarball_files(output_filename, file_list):
    with tarfile.open(output_filename, "w:gz") as tar:
        for file in file_list:
            tar.add(file, arcname=file)  # arcname 保持原始檔名
    print(f"已打包 {len(file_list)} 個檔案到 {output_filename}")

def kill_files(file_list):
    for i,f in enumerate(file_list):
        os.system("rm " + f)
    return f"已刪除 {len(file_list)} 個檔案，從{file_list[0]}到{file_list[-1]}"
    
def cp_files(file_list):
    for i,f in enumerate(file_list):
        os.system("cp " + f)
    print(f"已複製 {len(file_list)} 個檔案，從{file_list[0]}到{file_list[-1]}")


def ZLAverage(BC, J, D, L, P, m, phys):
    folder = creatDir(BC, J, D, L, P, m, phys)
    sourceName = creatCpName(BC, J, D, L, P, m, phys)
    colName = creatColName(BC, J, D, L, P, m, phys)
    source += folder[0] + source
    collect += folder[1] + collect
    
    with open(collect, "a") as targetFile:
        
        for seed in  seedArray:
            sourcePath = source.replace("s_re",str(seed))
            if os.path_exist(sourcePath):
                context += fread(source,"ZL") + "\n"
            else:
                continue
            
def Combine(BC, J, D, L, P, m, phys, s1, s2):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)

    mySourcePath = folder[0] + "/" + name[0]
    groupSourcePath = folder[1] + "/" + name[1]
    myTarPath = folder[2] + "/" + name[2]
    groupTarPath = folder[3] + "/" + name[3]

    seedArray = list(range(s1, s2 + 1))
    context = ""

    for seed in seedArray:
        groupSource = groupSourcePath.replace("s_re", str(seed))
        mySource = mySourcePath.replace("s_re", str(seed))

        if os.path.exists(groupSource) and os.path.exists(mySource):
            if compare(groupSource, mySource, seed):
                fcontext = fread(groupSource, phys)
            else:
                os.remove(groupSource)
                shutil.copy(mySource, groupSource)
                fcontext = fread(groupSource, phys)
        elif os.path.exists(mySource):
            os.makedirs(os.path.dirname(groupSource), exist_ok=True)
            shutil.copy(mySource, groupSource)
            os.remove(mySource)
            fcontext = fread(groupSource, phys)
        elif os.path.exists(groupSource):
            fcontext = fread(groupSource, phys)
        else:
            continue

        if fcontext is not None:
            context += f"{seed}:{fcontext}\n"

    if context != "":
        os.makedirs(os.path.dirname(groupTarPath), exist_ok=True)
        os.makedirs(os.path.dirname(myTarPath), exist_ok=True)

        if s1 == 1:
            context = f"{phys}\n{context}"
            print(f"[WRITE] groupTarPath: {groupTarPath}, myTarPath: {myTarPath}")
            with open(groupTarPath, "w") as f1, open(myTarPath, "w") as f2:
                f1.write(context)
                f2.write(context)
        else:
            print(f"[APPEND] groupTarPath: {groupTarPath}, myTarPath: {myTarPath}")
            with open(groupTarPath, "a") as f1, open(myTarPath, "a") as f2:
                f1.write(context)
                f2.write(context)            

def average(BC, J, D, L, P, m, phys, s1, s2):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)

    mySourcePath = folder[0] + "/" + name[0]
    groupSourcePath = folder[1] + "/" + name[1]
    myTarPath = folder[2] + "/" + name[2]
    groupTarPath = folder[3] + "/" + name[3]
    
    with open(f,"r") as a:
        a = a.readlines()
        if phys in a[0].strip():
            del a[0]
        metaContext = {}
        for s in a:
            s = s.strip()
            sNum = int(s[0].split(":")[0])
            if sNum not in metaContext:
                metaContext[sNum] = {}
                
            del s[0]
            s = s.replace(" ")

            for corr in s:
                if int(corr[1]) - int(corr[0]) not in dic:
                    metaContext[sNum][int(corr[1]) - int(corr[0])] = [float(corr[2])]
                else:
                    metaContext[sNum][int(corr[1]) - int(corr[0])].append(float(corr[2]))

        
def Combine1(BC, J, D, L, P, m, phys, s1, s2):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)

    mySourcePath = folder[0] + "/" + name[0]
    groupSourcePath = folder[1] + "/" + name[1]
    myTarPath = folder[2] + "/" + name[2]
    groupTarPath = folder[3] + "/" + name[3]

    seedArray = list(range(s1,s2+1))
    
    context = ""
    
    for seed in  seedArray:
        groupSource = groupSourcePath.replace("s_re",str(seed))
        mySource = mySourcePath.replace("s_re",str(seed))

        if os.path.exists(groupSource) and os.path.exists(mySource):
            if compare(groupSource, mySource, seed):
                fcontext = fread(groupSource,phys)
                if fcontext == None:
                    continue
                context += f"{seed}:{fcontext}\n"
            else:
                os.remove(groupSource)
                shutil.copy(mySource, groupSource)
                fcontext = fread(groupSource,phys)
                if fcontext == None:
                    continue
                context += f"{seed}:{fcontext}\n"
        else:
            if os.path.exists(mySource):
                os.makedirs(os.path.dirname(groupSource), exist_ok=True)
                shutil.copy(mySource, groupSource)
                os.remove(mySource)
                fcontext = fread(groupSource,phys)
                if fcontext == None:
                    continue
                context += f"{seed}:{fcontext}\n"
            else:
                fcontext = fread(groupSource,phys)
                if fcontext == None:
                    continue
                context += f"{seed}:{fcontext}\n"              

    if context != "":
        if s1 == 1:
            context = f"{phys}\n{context}" 
            print(f"groupTarPath:{groupTarPath}, myTarPath:{myTarPath}")
            os.makedirs(os.path.dirname(groupTarPath), exist_ok=True)
            os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
            with open(groupTarPath, "w") as targetFile1, open(myTarPath, 'w') as targetFile2:
                targetFile1.write(context)
                targetFile2.write(context)
        else:
            if os.path.exits(groupTarPath) and os.path.exits(myTarPath):
                print(f"groupTarPath:{groupTarPath}, myTarPath:{myTarPath}")
                os.makedirs(os.path.dirname(groupTarPath), exist_ok=True)
                os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
                with open(groupTarPath, "a") as targetFile1, open(myTarPath, 'a') as targetFile2:
                    targetFile1.write(context)
                    targetFile2.write(context)   
            else:
                print(f"groupTarPath or myTarPath not exist")   

def parameter_read_dict(filename):
    parameters = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key:
                        parameters[key] = value
    except FileNotFoundError:
        print(f"無法開啟檔案: {filename}")
    
    return parameters

# def corrAverage(BC, J, D, L, P, m, phys):
#     folder = creatDir()
#     source = creatCpName()
#     collect = creatColName()
#     source += folder + source
#     collect += folder + collect
    
#     with open(collect, "a") as targetFile:
        
#         for seed in  seedArray:
#             sourcePath = source.replace("s_re",str(seed))
#             if os.path_exist(sourcePath):
#                 context += fread(source,"ZL") + "\n"
#             else
#                 continue
def gapAverage(BC, J, D, L, P, m, phys):
    folder = creatDir()
    source = creatCpName()
    collect = creatColName()
    source += folder + source
    collect += folder + collect
    
    with open(collect, "a") as targetFile:
        
        for seed in  seedArray:
            sourcePath = source.replace("s_re",str(seed))
            if os.path_exist(sourcePath):
                context += fread(source,"ZL") + "\n"
            else:
                continue
# def w_locCombine(BC, J, D, L, P, m, phys):
#     folder = creatDir()
#     source = creatCpName()
#     collect = creatColName()
#     source += folder + source
#     collect += folder + collect
    
#     with open(collect, "a") as targetFile:
        
#         for seed in  seedArray:
#             sourcePath = source.replace("s_re",str(seed))
#             if os.path_exist(sourcePath):
#                 context += fread(source,"ZL") + "\n"
#             else
#                 continue
            
if __name__ == "__main__":
    file = "/home/aronton/tSDRG_random/Subpy/parameterRead/2025/2025_5_13/Spin15_L48_Jdis030_Dim000_P10_BC=OBC_chi35_partition=scopion2_seed1=1_seed2=50_ds=25_task=submit_H20_M5_S51.txt"
    arg = []
    # Jstr = [f"Jdis{str(i).zfill(3)}" for i in range(int(J),int(J)+1)]
    # Jstr = [f"Jdis{str(i).zfill(3)}" for i in range(30,81,50)]

    # Dstr = [f"Dim{str(i).zfill(3)}" for i in range(101)]
    # Lstr = [f"L{num}" for num in range(31, 255, 32)]  # 只有 L512
    # Lstr = [f"L{num}" for num in range(64, 129, 64)]  # 只有 L512
    a = scriptCreator.para("read",file)
    parameterlist = a.para
    para=scriptCreator.paraList1(parameterlist["L"],parameterlist["J"],parameterlist["D"],parameterlist["S"])
    BC = parameterlist["BC"]
    Pdis = parameterlist["Pdis"]
    chi = "m" + str(parameterlist["chi"])
    s1 = int(parameterlist["S"]["S1"])
    s2 = int(parameterlist["S"]["S2"])
    # s1 = int(sys.argv[2])
    # s2 = int(sys.argv[3])
    for s in ["ZL","corr1","corr2","string","J_list","energy","dimerization","w_loc","seed"]:
        for L in para.L_str:
            for J in para.J_str:
                    arg.append((BC, J, para.D_str[0], L, f"P{Pdis}", f"{chi}", s, s1, s2))
    # s1 = 1
    # s2 = 30000
    # for s in ["ZL","corr1","corr2","string","J_list","energy","dimerization","w_loc","seed"]:
    #     for L in ["L31","L63","L127"]:
    #         for J in ["Jdis030","Jdis080"]:
    #                 arg.append(("OBC", J, "Dim000", L, "P10", "m40", s, s1, s2))
    # print(Jstr)
    # print(Lstr)
    print(arg)         

    def fun(arg):
        print("---------------------col--------------------\n")
        MAX_PROCESSES = min(10, multiprocessing.cpu_count())  # 最多用 4 核心
        with multiprocessing.Pool(processes=MAX_PROCESSES) as pool:
            results = pool.starmap(Combine, arg)
        # print("---------------------del--------------------\n")
        # with multiprocessing.Pool(processes=20) as pool:
        #     results1 = pool.starmap(checkAndDelete, arg)
            
    # 計算函數執行時間
    execution_time = timeit.timeit(lambda: fun(arg), number=1)

    # 執行並顯示結果
    # results1, results2 = fun(arg)
    print(f"Execution time: {execution_time} seconds")    