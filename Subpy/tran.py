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


J = sys.argv[1]

tSDRG_path = "/dicos_ui_home/aronton/tSDRG_random"
group_path = "/ceph/work/NTHU-qubit/LYT/tSDRG_random"

sourcelist = {"ZL":"ZL.csv", "energy":"energy.csv", "seed":"s_re_seed.csv",\
    "corr1":"_".join(["L_re","P_re","m_re","s_re","corr1.csv"]), "corr2":"_".join(["L_re","P_re","m_re","s_re","corr2.csv"]),\
    "ZLI":"ZLI.csv", "ZLC":"ZLC.csv", "w_loc":"w_loc.csv", "J_list":"J_list.csv", "dimerization":"dimerization.csv",\
    "string":"_".join(["L_re","P_re","m_re","s_re","string.csv"])
    }

newlist = {"ZL":"_".join(["L_re","P_re","m_re","s_re","ZL.txt"]), "energy":"_".join(["L_re","P_re","m_re","s_re","energy.txt"]),\
    "corr1":"_".join(["L_re","P_re","m_re","s_re","corr1.txt"]), "corr2":"_".join(["L_re","P_re","m_re","s_re","corr2.txt"]),\
    "ZLI":"_".join(["L_re","P_re","m_re","s_re","ZLI.txt"]), "ZLC":"_".join(["L_re","P_re","m_re","s_re","ZLC.txt"]),\
    "w_loc":"_".join(["L_re","P_re","m_re","s_re","w_loc.txt"]), "J_list":"_".join(["L_re","P_re","m_re","s_re","J_list.txt"]),\
    "string":"_".join(["L_re","P_re","m_re","s_re","string.txt"]), "seed":"_".join(["L_re","P_re","m_re","s_re","seed.txt"]),\
    "dimerization":"_".join(["L_re","P_re","m_re","s_re","dimerization.txt"])
    }

collist = {
    "ZL":"_".join(["ZL","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "energy":"_".join(["energy","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "corr1":"_".join(["corr1","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "corr2":"_".join(["corr2","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "ZLI":"_".join(["ZLI","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "ZLC":"_".join(["ZLC","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "w_loc":"_".join(["w_loc","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "J_list":"_".join(["J_list","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "string":"_".join(["string","L_re","P_re","m_re","J_re","D_re","s_re.txt"]),\
    "seed":"_".join(["seed","L_re","P_re","m_re","s_re.txt"]),
    "dimerization":"_".join(["dimerization","L_re","P_re","m_re","s_re.txt"])
    }

def checkInside(s, f, sample, phys):
    with open(f,"r") as a:
        a = a.readlines()    
        if a[0].strip() == phys:
            del a[0]
        data = [(v.split(":")[0].strip(),(v.split(":")[1].replace("\n"," ").strip())) for i,v in enumerate(a)]
        sorted_data = sorted(data, key=lambda x: int(x[0]))
    if s == sorted_data[sample+1][1]:
        return 1
    else:
        return f"{s} != {sorted_data[sample+1]}"


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

def creatSourceName(BC, J, D, L, P, m, phys):
    sourceName = sourcelist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    return sourceName

def creatCpName(BC, J, D, L, P, m, phys):
    CpName = newlist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    return CpName
def creatColName(BC, J, D, L, P, m, phys):
    colName = collist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    return colName
def creatDir(BC, J, D, L, P, m, phys):
    sourcePathBase = f"{tSDRG_path}/tSDRG/Main_15/data_random/BC_re/J_re/D_re/L_re_P_re_m_re_s_re/"
    cpPathBase = f"{group_path}/tSDRG/Main_15/data_random/BC_re/J_re/D_re/L_re_P_re_m_re_s_re/"
    targetPathBase = f"{group_path}/tSDRG/Main_15/data_collect/BC_re/J_re/D_re/"

    sourcePath = sourcePathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    cpPath = cpPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    targetPath = targetPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D)
    
    return (sourcePath, cpPath, targetPath)

def fread(f, phys):
    if os.path.exists(f):
        with open(f,"r") as a:
            a = a.readlines()
            if len(a) == 0:
                return "empty"
            else:
                if a[0].strip() == phys:
                    del a[0]
                a = "".join(a)
                a = a.replace("\n"," ")
                return a
    else:
        return "nofile"

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

def collectData(BC, J, D, L, P, m, phys, s1, s2):
    start = int(time.time())
    sourceName = creatSourceName(BC, J, D, L, P, m, phys)
    cpName = creatCpName(BC, J, D, L, P, m, phys)
    colName = creatColName(BC, J, D, L, P, m, phys)
    dirpath = creatDir(BC, J, D, L, P, m, phys)
    sourcePath = f"{dirpath[0]}{sourceName}"
    cpPath = f"{dirpath[1]}{cpName}"
    targetPath = f"{dirpath[2]}{colName}"
    
    
    # if os.path.exists(dirpath[0].replace("s_re", "")) and checkFileNum(.replace("s_re", ""))==0:
    #     try:
    #         folder = dirpath[0].replace("s_re", "")
    #         messege += f"rmdir {folder}\n"
    #         # print("rmdir " + folder)
    #         os.rmdir(folder)
    #     except Exception as e:
    #         messege += str(e) +"\n"
    # if os.path.exists(dirpath[1].replace("s_re", "")) and checkFileNum(dirpath[1].replace("s_re", ""))==0:
    #     try:
    #         folder = dirpath[1].replace("s_re", "")
    #         messege += f"rmdir {folder}\n"
    #         # print("rmdir " + folder)
    #         os.rmdir(folder)
    #     except Exception as e:
    #         messege += str(e) +"\n"
    # if os.path.exists(dirpath[2].replace("s_re", "")) and checkFileNum(dirpath[2].replace("s_re", ""))==0:
    #     try:
    #         folder = dirpath[2].replace("s_re", "")
    #         messege += f"rmdir {folder}\n"
    #         # print("rmdir " + folder)
    #         os.rmdir(folder)
    #     except Exception as e:
    #         messege += str(e) +"\n"    
    
    if not os.path.exists(dirpath[0].replace("s_re", "")):
        # print(dirpath[0].replace("s_re", ""))
        os.makedirs(dirpath[0].replace("s_re", ""), exist_ok=True)  
    if not os.path.exists(dirpath[1].replace("s_re", "")):
        # print(dirpath[1].replace("s_re", ""))
        os.makedirs(dirpath[1].replace("s_re", ""), exist_ok=True) 
    if not os.path.exists(dirpath[2].replace("s_re", "")):
        # print(dirpath[2].replace("s_re", ""))
        os.makedirs(dirpath[2].replace("s_re", ""), exist_ok=True) 
    record = 0
    err = 1
    # 產生 seed 陣列
    targetPath = targetPath.replace("_s_re","")    
    messege = f"targetPath:{targetPath}\n"
    # print(f"targetPath:{targetPath}\n")
    with open(targetPath, 'w') as fTargert:
        seedArray = [i for i in range(s1,s2+1)]
        line = ""
        if int(s1) == 1:
            line = f"{phys}\n"
        else:
            line = ""
        for seed in seedArray:

            if os.path.exists(dirpath[0].replace("s_re", f"{seed}")):
                if checkFileNum(dirpath[0].replace("s_re", f"{seed}"))==0:
                    try:
                        folder = dirpath[0].replace("s_re", f"{seed}")
                        messege += f"rmdir {folder}\n"
                        # print("rmdir " + folder)
                        os.rmdir(folder)
                    except Exception as e:
                        messege += str(e) +"\n"
            if os.path.exists(dirpath[1].replace("s_re", f"{seed}")):
                if checkFileNum(dirpath[1].replace("s_re", f"{seed}"))==0:
                    try:
                        folder = dirpath[1].replace("s_re", f"{seed}")
                        messege += f"rmdir {folder}\n"
                        # print("rmdir " + folder)
                        os.rmdir(folder)
                    except Exception as e:
                        messege += str(e) +"\n"
            if os.path.exists(dirpath[2].replace("s_re", f"{seed}")):
                if checkFileNum(dirpath[2].replace("s_re", f"{seed}"))==0:
                    try:
                        folder = dirpath[2].replace("s_re", f"{seed}")
                        messege += f"rmdir {folder}\n"
                        # print("rmdir " + folder)
                        os.rmdir(folder)
                    except Exception as e:
                        messege += str(e) +"\n"
                # print(dirpath[0].replace("s_re", f"{seed}"))
                # os.makedirs(dirpath[0].replace("s_re", f"{seed}"), exist_ok=True)  
            # if not os.path.exists(dirpath[1].replace("s_re", f"{seed}")):
            #     # print(dirpath[1].replace("s_re", f"{seed}"))
            #     os.makedirs(dirpath[1].replace("s_re", f"{seed}"), exist_ok=True) 
            # if not os.path.exists(dirpath[2].replace("s_re", f"{seed}")):
            #     # print(dirpath[2].replace("s_re", f"{seed}"))
            #     os.makedirs(dirpath[2].replace("s_re", f"{seed}"), exist_ok=True) 

            source = sourcePath.replace("s_re", f"{seed}")
            if not os.path.exists(source):
                continue
            new = cpPath.replace("s_re", f"{seed}")
            
            if seed == seedArray[0]:
                messege += source +"\n"
                # print(newPath)
            messege += source +"\n"
            if os.path.exists(new):
                if compare(source, new, seed):
                    data = fread(new,phys)
                    messege += f"data equal {seed}:{data}\n"
                    line += f"{seed}:{data}\n"
                else:
                    os.remove(new)
                    shutil.copy2(source, new)
                    messege += f"data inequal recopy\n"
                    # rmCmd = f"rm {new}" 
                    # cpCmd = f"cp {source} {new}" 
                    # rmCmd = f"rm {new}" 
                    # messege += f"data inequal recopy\n"
                    # os.system(rmCmd)
                    # os.system(cpCmd)
            else:
                data = fread(source,phys)
                line += f"{seed}:{data}\n"
                shutil.copy2(source, new)
                # cpCmd = f"cp {source} {new}" 
                messege += f"empty shutil.copy2({source}, {new})\n"
                # os.system(cpCmd)
        # fTargert.write(line)
    # except FileNotFoundError as e:
    #     print(e)
        # messege += f"targetPath:{targetPath}\n"
    end = int(time.time())
    messege += f"start: {datetime.datetime.fromtimestamp(start)}, time:{end-start} seconds\n"
    print(messege)
    return 

def checkAndDelete(BC, J, D, L, P, m, phys, s1, s2):
    start = time.time()
    sourceName = creatSourceName(BC, J, D, L, P, m, phys)
    cpName = creatCpName(BC, J, D, L, P, m, phys)
    colName = creatColName(BC, J, D, L, P, m, phys)
    dirpath = creatDir(BC, J, D, L, P, m, phys)
    sourcePath = f"{dirpath[0]}{sourceName}"
    cpPath = f"{dirpath[1]}{cpName}"
    targetPath = f"{dirpath[2]}{colName}"
    dellist = []
    cplist = []
    if not os.path.exists(dirpath[0].replace("s_re", "")):
        # print(dirpath[0].replace("s_re", ""))
        os.makedirs(dirpath[0].replace("s_re", ""), exist_ok=True)  
    if not os.path.exists(dirpath[1].replace("s_re", "")):
        # print(dirpath[1].replace("s_re", ""))
        os.makedirs(dirpath[1].replace("s_re", ""), exist_ok=True) 
    if not os.path.exists(dirpath[2].replace("s_re", "")):
        # print(dirpath[2].replace("s_re", ""))
        os.makedirs(dirpath[2].replace("s_re", ""), exist_ok=True) 
    record = 0
    err = 1
    # 產生 seed 陣列
    targetPath = targetPath.replace("_s_re","")    
    # messege = f"targetPath:{targetPath}\n"
    # 開啟輸出檔案
    # print(f"line:{line}")
    seedArray = [i for i in range(s1,s2+1)]
    line = ""
    for seed in seedArray:
        
        if not os.path.exists(dirpath[0].replace("s_re", f"{seed}")):
            messege += dirpath[0].replace("s_re", f"{seed}")
            # print(dirpath[0].replace("s_re", f"{seed}"))
            os.makedirs(dirpath[0].replace("s_re", f"{seed}"), exist_ok=True)  
        if not os.path.exists(dirpath[1].replace("s_re", f"{seed}")):
            # print(dirpath[1].replace("s_re", f"{seed}"))
            os.makedirs(dirpath[1].replace("s_re", f"{seed}"), exist_ok=True) 
        if not os.path.exists(dirpath[2].replace("s_re", f"{seed}")):
            # print(dirpath[2].replace("s_re", f"{seed}"))
            os.makedirs(dirpath[2].replace("s_re", f"{seed}"), exist_ok=True) 
        
        source = sourcePath.replace("s_re", f"{seed}")
        if not os.path.exists(source):
            continue
        new = cpPath.replace("s_re", f"{seed}")
        
        # newPath = sourcePath + fileName
        # newPath = newPath.replace("s_re", f"{seed+1}")
        # print(f"newPath:{new}")
        # os.path.join(sourcePath.replace("s_re", f"{seed+1}"), fileName)
        if seed == seedArray[0]:
            messege += source +"\n"
            # print(newPath)
        messege += source +"\n"
        if os.path.exists(new):
            if compare(source, new, seed):
                dellist.append(source)
                cplist.append(new)
            else:
                os.remove(new)
                shutil.copy2(source, new)
                # rmCmd = f"rm {new}" 
                # cpCmd = f"cp {source} {new}" 
                # rmCmd = f"rm {new}" 
                messege += f"{seed}:data inequal recopy, source:{source} new:{new}\n"
                # os.system(rmCmd)
                # os.system(cpCmd)
                dellist.append(source)
                cplist.append(new)
        else:
            data = fread(source,phys)
            line += f"{seed}:{data}\n"
            shutil.copy2(source, new)
            # cpCmd = f"cp {source} {new}" 
            messege += f"empty new copy {cpCmd}\n"
            # os.system(cpCmd)
            dellist.append(source)
    # fTargert.write(line)
    # kill_files(cplist)
    try:
        messege += kill_files(dellist)
    except:
        return
    # except FileNotFoundError as e:
    #     print(e)
        # messege += f"targetPath:{targetPath}\n"
    end = time.time()
    messege += f"time:{start}~{end}:{end-start} seconds\n"
    print(messege)
    return (record, err)


arg = []
Jstr = [f"Jdis{str(i).zfill(3)}" for i in range(int(J),int(J)+1)]
# Dstr = [f"Dim{str(i).zfill(3)}" for i in range(101)]
Lstr = [f"L{num}" for num in range(32, 513, 32)]  # 只有 L512

for s in ["ZL","corr1","corr2","string","J_list","energy","dimerization","w_loc","seed"]:
    for L in Lstr:
        for J in Jstr:
                  arg.append(("OBC", J, "Dim000", L, "P10", "m40", s, 1, 30000))
def fun(arg):
    print("---------------------col--------------------\n")
    with multiprocessing.Pool(processes=10) as pool:
        results1 = pool.starmap(collectData, arg)
    # print("---------------------del--------------------\n")
    # with multiprocessing.Pool(processes=20) as pool:
    #     results1 = pool.starmap(checkAndDelete, arg)
        
# 計算函數執行時間
execution_time = timeit.timeit(lambda: fun(arg), number=1)

# 執行並顯示結果
# results1, results2 = fun(arg)
print(f"Execution time: {execution_time} seconds")