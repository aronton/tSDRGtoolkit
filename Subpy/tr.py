import os
import math
import time
import timeit
import sys
import tarfile
import datetime
import multiprocessing
from pathlib import Path
import shutil


tSDRG_path = "/dicos_ui_home/aronton/tSDRG_random"
group_path = "/ceph/work/NTHU-qubit/LYT/tSDRG_random"

J = sys.argv[1]

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
    groupSourcePathBase = "/".join([group_path,sourcePath])
    myTargetPathBase = "/".join([tSDRG_path,tarPath])
    groupTargetPathBase = "/".join([group_path,tarPath])
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
def delete(BC, J, D, L, P, m, phys, s1, s2):
    folder = creatDir(BC, J, D, L, P, m, phys)
    myDirPath = folder[0]
    gDirPath = folder[1]
    
    seedArray = list(range(s1,s2+1))
    context = ""
    context1 = ""
    for seed in  seedArray:
        myDir = myDirPath.replace("s_re",str(seed))
        gDir = gDirPath.replace("s_re",str(seed))
        # print(f"mySource:{mySource}")
        # print(f"groupSource:{groupSource}")
        try:
            count1 = len([f for f in os.listdir(myDir)])
            count2 = len([f for f in os.listdir(gDir)])
            if count1 == 0:
                os.rmdir(myDir)
                context += f"{myDir} 已成功刪除"
            if count2 == 0:
                os.rmdir(gDir)
                context1 += f"{gDir} 已成功刪除"
        except (FileNotFoundError, OSError) as e:
            continue
    print(context)    
    print(context1)    
def Combine(BC, J, D, L, P, m, phys, s1, s2):
    folder = creatDir(BC, J, D, L, P, m, phys)
    # mySourceFolder = folder[0]
    # groupSourceFolder = folder[1]
    # myTarFolder = folder[2]
    # groupTarFolder = folder[3]

    name = creatName(BC, J, D, L, P, m, phys)
    # mySourceName = creatSourceName(BC, J, D, L, P, m, phys)
    # groupSourceName = creatCpName(BC, J, D, L, P, m, phys)
    # groupColName = creatColName(BC, J, D, L, P, m, phys)
    # myColName = creatColName(BC, J, D, L, P, m, phys).replace(group_path ,tSDRG_path)
    
    # if not os.path.exists(groupColName) or not os.path.exists(myColName):
    #     os.makedirs(groupColName)
    #     os.makedirs(myColName)

    mySourcePath = folder[0] + "/" + name[0]
    groupSourcePath = folder[1] + "/" + name[1]
    myTarPath = folder[2] + "/" + name[2]
    groupTarPath = folder[3] + "/" + name[3]
    # source = folder[0] + source
    # collect1 = folder[2] + collect
    # collect2 = folder[0].replace("s_re","").replace("data_random","data_collect") + "/" + collect
    # length = 0
    # if os.path_exist(collect):
    #     with open(collect, "r") as targetFile:
    #         length = len(targetFile.readlines())
    # else:
    seedArray = list(range(s1,s2+1))
    # collect1 = collect.replace("_s_re","")
    # print(f"collect:{collect1}, {collect2}")
    
    # print(f"groupTarPath:{groupTarPath}, myTarPath:{myTarPath}")
    context = f"{phys}\n"
    for seed in  seedArray:
        groupSource = groupSourcePath.replace("s_re",str(seed))
        mySource = mySourcePath.replace("s_re",str(seed))
        # print(f"mySource:{mySource}")
        # print(f"groupSource:{groupSource}")
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
                # print(f"fcontext:{fcontext}")
                if fcontext == None:
                    continue
                context += f"{seed}:{fcontext}\n"              
    # print(context)  
            # if length > seed:
            #     context += fcontext + "\n"
            # else:
            #     exist = checkInside(fcontext, sourcePath, sample, phys)
            #     if exist == False:
            #         context += fcontext + "\n"
    # groupTarPath = groupTarPath
    # myTarPath = myTarPath


    if context != f"{phys}\n":
        print(f"groupTarPath:{groupTarPath}, myTarPath:{myTarPath}")
        os.makedirs(os.path.dirname(groupTarPath), exist_ok=True)
        os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
        with open(groupTarPath, "w") as targetFile1, open(myTarPath, 'w') as targetFile2:
            targetFile1.write(context)
            targetFile2.write(context)

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
            
arg = []
Jstr = [f"Jdis{str(i).zfill(3)}" for i in range(int(J),int(J)+1,1)]
# Dstr = [f"Dim{str(i).zfill(3)}" for i in range(101)]
# Lstr = [f"L{num}" for num in range(31, 255, 32)]  # 只有 L512
Lstr = [f"L{num}" for num in range(32, 513, 32)]  # 只有 L512

for s in ["ZL","corr1","corr2","string","J_list","energy","dimerization","w_loc","seed"]:
    for L in Lstr:
        for J in Jstr:
                  arg.append(("PBC", J, "Dim000", L, "P10", "m40", s, 1, 30000))
print(Jstr)
print(Lstr)
                  

def fun(arg):
    print("---------------------delete--------------------\n")
    with multiprocessing.Pool(processes=20) as pool:
        results1 = pool.starmap(delete, arg)
    # print("---------------------del--------------------\n")
    # with multiprocessing.Pool(processes=20) as pool:
    #     results1 = pool.starmap(checkAndDelete, arg)
        
# 計算函數執行時間
execution_time = timeit.timeit(lambda: fun(arg), number=1)

# 執行並顯示結果
# results1, results2 = fun(arg)
print(f"Execution time: {execution_time} seconds")