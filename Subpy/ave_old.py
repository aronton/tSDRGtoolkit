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
import numpy as np



dicosPath = "/ceph/work/NTHU-qubit/LYT/tSDRG_random"
scopionPath = "/home/aronton/tSDRG_random"

if os.path.isdir(dicosPath):
    tSDRG_path = dicosPath
    group_path = dicosPath
    
if os.path.isdir(scopionPath):
    tSDRG_path = scopionPath
    group_path = scopionPath
    
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

metalist = {
    "ZL":"_".join(["ZL","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "energy":"_".join(["gap","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "corr1":"_".join(["corr1","L_re","P_re","m_re","J_re","D_re","dx_re.txt"]),\
    "corr2":"_".join(["corr2","L_re","P_re","m_re","J_re","D_re","dx_re.txt"]),\
    }

metaDislist = {
    "ZL":"_".join(["ZL_dis","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "energy":"_".join(["gap_dis","L_re","P_re","m_re","J_re","D_re.txt"]),\
    "corr1":"_".join(["corr1_dis","L_re","P_re","m_re","J_re","D_re","dx_re.txt"]),\
    "corr2":"_".join(["corr2_dis","L_re","P_re","m_re","J_re","D_re","dx_re.txt"]),\
    }


def creatName(BC, J, D, L, P, m, phys):
    mySourceName = sourcelist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    myTargetName = tarlist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    groupSourceName = grouplist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    groupTargetName = tarlist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
    groupAveName = metalist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    groupDisName = metaDislist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    return (mySourceName, groupSourceName, myTargetName, groupTargetName, groupAveName, groupDisName)

# def creatCpName(BC, J, D, L, P, m, phys):
#     CpName = newlist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
#     return CpName
# def creatColName(BC, J, D, L, P, m, phys):
#     colName = collist[phys].replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m) 
#     return colName
def creatDir(BC, J, D, L, P, m, phys):
    avePath = "/".join(["tSDRG","Main_15","metadata_old","BC_re","J_re","D_re","L_re_P_re_m_re_s_re"])
    sourcePath = "/".join(["tSDRG","Main_15","data_tar","BC_re","J_re","D_re","L_re_P_re_m_re_s_re"])
    tarPath = "/".join(["tSDRG","Main_15","data_collect_old","BC_re","J_re","D_re","L_re_P_re_m_re"])
    mySourcePathBase = "/".join([tSDRG_path,sourcePath])
    groupSourcePathBase = "/".join([group_path,sourcePath])
    myTargetPathBase = "/".join([tSDRG_path,tarPath])
    groupTargetPathBase = "/".join([group_path,tarPath])
    avePathBase = "/".join([tSDRG_path,avePath])
    # disPathBase = "/".join([tSDRG_path,avePath])
    # sourcePathBase = f"{tSDRG_path}/tSDRG/Main_15/data_random/BC_re/J_re/D_re/L_re_P_re_m_re_s_re/"
    # cpPathBase = f"{group_path}/tSDRG/Main_15/data_random/BC_re/J_re/D_re/L_re_P_re_m_re_s_re/"
    # targetPathBase = f"{group_path}/tSDRG/Main_15/data_collect/BC_re/J_re/D_re/L_re_P_re_m_re/"

    mySourcePath = mySourcePathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    groupSourcePath = groupSourcePathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    myTargetPath = myTargetPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    groupTargetPath = groupTargetPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    myAvePath = avePathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m).replace("s_re", "meta")
    myDisPath = avePathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m).replace("s_re", "dis")
    # cpPath = cpPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    # targetPath = targetPathBase.replace("BC_re", BC).replace("J_re", J).replace("D_re", D).replace("L_re", L).replace("P_re", P).replace("m_re", m)
    
    return (mySourcePath, groupSourcePath, myTargetPath, groupTargetPath, myAvePath, myDisPath)

def gapAverage(BC, J, D, L, P, m, phys):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    myTarPath = folder[2] + "/" + name[2]

    gaplist = []
    try:
        with open(myTarPath, "r") as targetFile:
            collect = targetFile.readlines()
            collect = [line.strip() for line in collect]
            if collect and collect[0] == "energy":
                del collect[0]
            for line in collect:
                line = line.split(":")[-1].split(" ")
                try:
                    gap = float(line[1]) - float(line[0])
                    gaplist.append(gap)
                except Exception as e:
                    print(e)
    except FileNotFoundError:
        print(f"File not found: {myTarPath}")
        return False, False, False
    save_gapDistribute(gaplist, BC, J, D, L, P, m, phys)
    gapAve = np.mean(gaplist)
    sample = len(gaplist) 
    error = np.std(gaplist, ddof=1)

    return gapAve, sample, error

def save_gapDistribute(gaplist, BC, J, D, L, P, m, phys):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    gapDisBase = folder[5] + "/" + name[5]
    context = "ground_state_gap\n"
    for i, value in enumerate(gaplist):
        context += f"{value}\n"
    
    if context == "ground_state_gap\n":
        return
    else:
        if not os.path.exists(gapDisBase):
            os.makedirs(os.path.dirname(gapDisBase), exist_ok=True)
        with open(gapDisBase, "w") as targetFile:
            targetFile.write(context)

def save_gap(BC, J, D, L, P, m, phys):
    gapAve, sample, error = gapAverage(BC, J, D, L, P, m, phys)
    if gapAve == False:
        # print(f"Error: No data found for {BC}, {J}, {D}, {L}, {P}, {m}, {phys}")
        return
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    myTarPath = folder[4] + "/" + name[4]
    # print(f"myTarPath:{myTarPath}")
    if not os.path.exists(myTarPath):
        os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
    with open(myTarPath, "w") as targetFile:
        targetFile.write(f"ground_state_energy, sample, errorbar\n{gapAve}, {sample}, {error/math.sqrt(sample)}")

# def corrAverage(BC, J, D, L, P, m, phys, path=None):
#     folder = creatDir(BC, J, D, L, P, m, phys)
#     name = creatName(BC, J, D, L, P, m, phys)
#     myTarPath = folder[2] + "/" + name[2]
#     if path is not None:
#         myTarPath = path
#     corrDic = {}
#     try:
#         with open(myTarPath, "r") as targetFile:
#             collect = targetFile.readlines()
#             collect = [line.strip() for line in collect]
#             if collect and collect[0] == "corr1":
#                 del collect[0]
#             for line in collect:
#                 line = line.split(":")[-1].split(" ")
#                 for data in line:
#                     if data:
#                         parts = data.split(",")
#                         if len(parts) >= 3:
#                             try:
#                                 x1, x2 = int(parts[0]), int(parts[1])
#                                 corr = float(parts[2])
#                                 key = x2 - x1
#                                 if key not in corrDic:
#                                     corrDic[key] = []
#                                 corrDic[key].append(corr)
#                             except ValueError:
#                                 continue  # 忽略無法轉換的數據
#     except FileNotFoundError:
#         print(f"File not found: {myTarPath}")
#         return False, False, False
#     save_corrDistribute(corrDic, BC, J, D, L, P, m, phys)
#     corr = {}
#     sample = {}
#     error = {}
#     for key, values in corrDic.items():
#         sample[key] = len(values)
#         corr[key] = np.mean(values)
#         error[key] = np.std(values, ddof=1) if len(values) > 1 else 0.0

#     return corr, sample, error

# def save_corrDistribute(corrDic, BC, J, D, L, P, m, phys, path=None):
#     folder = creatDir(BC, J, D, L, P, m, phys)
#     name = creatName(BC, J, D, L, P, m, phys)
#     # print( f"folder[4]:{folder[4]}")
#     corrDisBase = folder[5] + "/" + name[5]
#     for key, values in list(corrDic.items()):
#         context = ""
#         if BC == "OBC":
#             context = f"C_etoe=<S(0)S(dx={key})>\n"
#         elif BC == "PBC":
#             context = f"C_bulk=<S(0)S(dx={key})>\n"
#         corrDisPath = corrDisBase.replace("dx_re", f"dx={key}")
#         for value in values:
#             context += f"{value}\n"
        
#         if context == f"C_etoe=<S(0)S(dx={key})>\n" or context ==  f"C_bulk=<S(0)S(dx={key})>\n":
#             continue
#         else:
#             if not os.path.exists(corrDisPath):
#                 os.makedirs(os.path.dirname(corrDisPath), exist_ok=True)
#             with open(corrDisPath, "w") as targetFile:
#                 targetFile.write(context)
#         print(f"context:{context}")

# def save_corr(BC, J, D, L, P, m, phys, path=None):
#     corr, sample, error = corrAverage(BC, J, D, L, P, m, phys, path)
#     if corr == False:
#         print(f"Error: No data found for {BC}, {J}, {D}, {L}, {P}, {m}, {phys}")
#         return
#     folder = creatDir(BC, J, D, L, P, m, phys)
#     name = creatName(BC, J, D, L, P, m, phys)
#     # print( f"folder[4]:{folder[4]}")
#     myTarPathBase = folder[4] + "/" + name[4]
#     # print(f"myTarPath:{myTarPath}")

#     for key, values in list(corr.items()):
#         if corr[key] == None:
#             continue
#         myTarPath = myTarPathBase.replace("dx_re", f"dx={key}")
#         if BC == "OBC":
#             context = f"C_etoe=<S(0)S(dx={key})>,sample,errorbar\n" + f"{corr[key]},{sample[key]},{error[key]/math.sqrt(sample[key])}"
#         elif BC == "PBC":
#             context = f"C_bulk=<S(0)S(dx={key})>,sample,errorbar\n" + f"{corr[key]},{sample[key]},{error[key]/math.sqrt(sample[key])}"
#         if not os.path.exists(myTarPath):
#             os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
#         with open(myTarPath, "w") as targetFile:
#             targetFile.write(context)
#         print(f"C_bulk=<S(0)S(dx={key})>,sample,errorbar\n" + f"{corr[key]},{sample[key]},{error[key]/math.sqrt(sample[key])} for {BC}, {J}, {D}, {L}, {P}, {m}, {phys}")

                    
def corrAverage(BC, J, D, L, P, m, phys):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    myTarPath = folder[2] + "/" + name[2]

    corrDic = {}
    try:
        with open(myTarPath, "r") as targetFile:
            collect = targetFile.readlines()
            collect = [line.strip() for line in collect]
            if collect and collect[0] == "corr1":
                del collect[0]
            for line in collect:
                line = line.split(":")[-1].split(" ")
                # print(f"line:{line}")
                for data in line:
                    if data:
                        parts = data.split(",")
                        if len(parts) >= 2:
                            try:
                                dx, correlation = int(parts[0]), int(parts[1])
                                # correlation = float(parts[2])
                                # key = x2 - x1
                                if dx not in corrDic:
                                    corrDic[dx] = []
                                corrDic[dx].append(correlation)
                            except ValueError:
                                continue  # 忽略無法轉換的數據
    except FileNotFoundError:
        print(f"File not found: {myTarPath}")
        return False, False, False
    save_corrDistribute(corrDic, BC, J, D, L, P, m, phys)
    corr = {}
    sample = {}
    error = {}
    for key, values in corrDic.items():
        sample[key] = len(values)
        corr[key] = np.mean(values)
        error[key] = np.std(values, ddof=1) if len(values) > 1 else 0.0

    return corr, sample, error

def save_corrDistribute(corrDic, BC, J, D, L, P, m, phys):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    corrDisBase = folder[5] + "/" + name[5]
    for key, values in corrDic.items():
        context = ""
        if BC == "OBC":
            context = f"C_etoe=<S(0)S(dx={key})>\n"
        elif BC == "PBC":
            context = f"C_bulk=<S(0)S(dx={key})>\n"
        corrDisPath = corrDisBase.replace("dx_re", f"dx={key}")
        for value in values:
            context += f"{value}\n"
        if context == f"C_etoe=<S(0)S(dx={key})>\n" or context ==  f"C_bulk=<S(0)S(dx={key})>\n":
            continue
        else:
            if not os.path.exists(corrDisPath):
                os.makedirs(os.path.dirname(corrDisPath), exist_ok=True)
            with open(corrDisPath, "w") as targetFile:
                targetFile.write(context)

def save_corr(BC, J, D, L, P, m, phys):
    corr, sample, error = corrAverage(BC, J, D, L, P, m, phys)
    if corr == False:
        # print(f"Error: No data found for {BC}, {J}, {D}, {L}, {P}, {m}, {phys}")
        return
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    myTarPathBase = folder[4] + "/" + name[4]
    # print(f"myTarPath:{myTarPath}")

    for key in corr.keys():
        if corr[key] == None:
            continue
        myTarPath = myTarPathBase.replace("dx_re", f"dx={key}")
        if BC == "OBC":
            context = f"C_etoe=<S(0)S(dx={key})>,sample,errorbar\n" + f"{corr[key]},{sample[key]},{error[key]/math.sqrt(sample[key])}"
        elif BC == "PBC":
            context = f"C_bulk=<S(0)S(dx={key})>,sample,errorbar\n" + f"{corr[key]},{sample[key]},{error[key]/math.sqrt(sample[key])}"
        if not os.path.exists(myTarPath):
            os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
        with open(myTarPath, "w") as targetFile:
            targetFile.write(context)
            
def dimerAverage(BC, J, D, L, P, m, phys, path=None):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    myTarPath = folder[2] + "/" + name[2]
    if path is not None:
        myTarPath = path
    dimerlist = []
    
    try:
        if not os.path.exists(myTarPath):
            raise FileNotFoundError
        auto_delete_empty = True
        if os.path.getsize(myTarPath) == 0:
            if auto_delete_empty:
                os.remove(myTarPath)
                print(f"[刪除] 空檔案已刪除：{myTarPath}")
            raise ValueError("檔案為空")
        with open(myTarPath, "r") as targetFile:
            dimerlist = targetFile.readlines()
            if type(dimerlist[0]) == str or dimerlist[0] == "dimerization":
                del dimerlist[0]
        dimerlist = [float(line.split(":")[-1]) for line in dimerlist]
        if not dimerlist:
            if auto_delete_empty:
                os.remove(myTarPath)
                print(f"[刪除] 空檔案已刪除：{myTarPath}")
            raise ValueError("檔案內容為空")
    except FileNotFoundError:
        print(f"File not found: {myTarPath}")
        return False, False, False
    except ValueError as e:
        print(f"跳過空檔案: {BC}, {J}, {D}, {L}, {P}, {m}, {phys} → {e}")
        return False, False, False
    save_dimerDistribute(dimerlist, BC, J, D, L, P, m, phys, myTarPath)
    dimerAve = np.mean(dimerlist)
    sample = len(dimerlist)
    error = np.std(dimerlist, ddof=1)

    return dimerAve, sample, error

def save_dimerDistribute(zllist, BC, J, D, L, P, m, phys, path=None):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    dimerDisBase = folder[5] + "/" + name[5]
    context = "dimerization\n"
    for i, value in enumerate(zllist):
        context += f"{value}\n"
    if context == "dimerization\n":
        return
    else:
        if not os.path.exists(dimerDisBase):
            os.makedirs(os.path.dirname(dimerDisBase), exist_ok=True)
        with open(dimerDisBase, "w") as targetFile:
            targetFile.write(context)

def save_dimer(BC, J, D, L, P, m, phys, path=None):
    dimerization, sample, error = dimerAverage(BC, J, D, L, P, m, phys, path)
    if dimerization == False:
        # print(f"Error: No data found for {BC}, {J}, {D}, {L}, {P}, {m}, {phys}")
        return
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    myTarPath = folder[4] + "/" + name[4]

    if not os.path.exists(myTarPath):
        os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
    with open(myTarPath, "w") as targetFile:
        targetFile.write(f"dimerization, sample, errorbar\n{dimerization}, {sample}, {error/math.sqrt(sample)}")    
    # print(f"dimerization, sample, errorbar\n{dimerization}, {sample}, {error/math.sqrt(sample)} for {BC}, {J}, {D}, {L}, {P}, {m}, {phys}")


def ZLAverage(BC, J, D, L, P, m, phys):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    myTarPath = folder[2] + "/" + name[2]
    zllist = []
    auto_delete_empty = True
    try:
        if not os.path.exists(myTarPath):
            raise FileNotFoundError(f"{myTarPath} does not exist")

        if os.path.getsize(myTarPath) == 0:
            if auto_delete_empty:
                os.remove(myTarPath)
                print(f"[刪除] 空檔案已刪除：{myTarPath}")
            raise ValueError("檔案為空")
        with open(myTarPath, "r") as targetFile:
            zllist = targetFile.readlines()
            if type(zllist[0]) == str or zllist[0] == "ZL":
                del zllist[0]
            zllist = [float(line.split(":")[-1]) for line in zllist]
        if not zllist:
            if auto_delete_empty:
                os.remove(myTarPath)
                print(f"[刪除] 空檔案已刪除：{myTarPath}")
            raise ValueError("檔案內容為空")

    except FileNotFoundError:
        print(f"File not found: {myTarPath}")
        return False, False, False
    
    save_zlDistribute(zllist, BC, J, D, L, P, m, phys)
    zlAve = np.mean(zllist)
    sample = len(zllist)
    error = np.std(zllist, ddof=1)

    return zlAve, sample, error

def save_zlDistribute(zllist, BC, J, D, L, P, m, phys):
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    zlDisBase = folder[5] + "/" + name[5]
    context = "ZL\n"
    for i, value in enumerate(zllist):
        context += f"{value}\n"
    if context == "ZL\n":
        return
    else:
        if not os.path.exists(zlDisBase):
            os.makedirs(os.path.dirname(zlDisBase), exist_ok=True)
        with open(zlDisBase, "w") as targetFile:
            targetFile.write(context)

def save_ZL(BC, J, D, L, P, m, phys):
    zlAve, sample, error = ZLAverage(BC, J, D, L, P, m, phys)
    if zlAve == False:
        # print(f"Error: No data found for {BC}, {J}, {D}, {L}, {P}, {m}, {phys}")
        return
    folder = creatDir(BC, J, D, L, P, m, phys)
    name = creatName(BC, J, D, L, P, m, phys)
    # print( f"folder[4]:{folder[4]}")
    myTarPath = folder[4] + "/" + name[4]

    if not os.path.exists(myTarPath):
        os.makedirs(os.path.dirname(myTarPath), exist_ok=True)
    with open(myTarPath, "w") as targetFile:
        targetFile.write(f"ZL, sample, errorbar\n{zlAve}, {sample}, {error/math.sqrt(sample)}")    
# def save_gap():

def list_txt_files(directory):
    txt_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                full_path = os.path.join(root, file)
                txt_files.append(full_path)
    return txt_files

if __name__ == "__main__":
    # file = sys.argv[1]
    arg = []
    # a = scriptCreator.para("read",file)
    # parameterlist = a.para
    # para=scriptCreator.paraList1(parameterlist["L"],parameterlist["J"],parameterlist["D"],parameterlist["S"])
    
    Jstr = [f"Jdis{str(i).zfill(3)}" for i in range(10,11,10)]

    Dstr = [f"Dim{str(i).zfill(3)}" for i in range(101)]
    # Lstr = [f"L{num}" for num in range(31, 255, 32)]  # 只有 L512
    Lstr =  [f"L{num}" for num in range(64, 520, 64)]  # 只有 L512
    # [f"L{num}" for num in range(8, 65, 8)] +
    # BC = parameterlist["BC"]
    # Pdis = parameterlist["Pdis"]
    BC = "OBC"
    Pdis = 10
    chi = "m40"
    # chi = "m" + str(parameterlist["chi"])
    # s1 = int(sys.argv[2])
    # s2 = int(sys.argv[3])
    # if BC == "PBC":
    #     s_list = ["ZL","corr1","corr2","string","J_list","energy","dimerization","w_loc","seed"]
    #     # s_list = ["corr1","corr2"]
    # else:
    #     s_list = ["ZL","corr1","corr2","J_list","energy","dimerization","w_loc","seed"]
        # s_list = ["corr1","corr2"]
        
    # for s in s_list:
    # for D in para.D_str:
    #     for L in para.L_str:
    #         for J in para.J_str:
    #             save_corr(BC, J, D, L, f"P{Pdis}", f"{chi}", "corr1")    
    #             save_corr(BC, J, D, L, f"P{Pdis}", f"{chi}", "corr2")
    #             save_gap(BC, J, D, L, f"P{Pdis}", f"{chi}", "energy")   
    #             save_ZL(BC, J, D, L, f"P{Pdis}", f"{chi}", "ZL")   
    # for D in Dstr:
    D = "Dim000"
    for L in Lstr:
        for J in Jstr:
            save_corr(BC, J, D, L, f"P{Pdis}", f"{chi}", "corr1")    
            # save_corr(BC, J, D, L, f"P{Pdis}", f"{chi}", "corr2")
            # save_gap(BC, J, D, L, f"P{Pdis}", f"{chi}", "energy")   
            # save_ZL(BC, J, D, L, f"P{Pdis}", f"{chi}", "ZL")   
                    # arg.append((BC, J, para.D_str[0], L, f"P{Pdis}", f"{chi}", s, s1, s2))
    # 參數設定
    # D_i, D_f, D_d = 1, 80, 1
    # J_i, J_f, J_d = 60, 61, 1
    # L_i, L_f, L_d = 32, 550, 32                    
        
    # D_list = [f"Dim{str(i).zfill(3)}" for i in range(D_i, D_f, D_d)]
    # J_list = [f"Jdis{str(i).zfill(3)}" for i in range(J_i, J_f, J_d)]
    # L_list = [f"L{num}" for num in range(L_i, L_f, L_d)]
    # BC = "PBC"
    # Pdis = 10
    # chi = "m" + str(40)
    # s1 = 1
    # s2 = 10000
    # for D in D_list:
    #     for L in L_list:
    #         for J in J_list:
    #             # save_corr(BC, J, D, L, f"P{Pdis}", f"{chi}", "corr1")    
    #             # save_corr(BC, J, D, L, f"P{Pdis}", f"{chi}", "corr2")
    #             # save_gap(BC, J, D, L, f"P{Pdis}", f"{chi}", "energy")   
    #             save_ZL(BC, J, D, L, f"P{Pdis}", f"{chi}", "ZL")   
    # save_corr(BC, J, para.D_str[0], L, f"P{Pdis}", f"{chi}", "corr1")    
    # save_corr(BC, J, para.D_str[0], L, f"P{Pdis}", f"{chi}", "corr2")
    # save_gap(BC, J, para.D_str[0], L, f"P{Pdis}", f"{chi}", "energy")   
    # save_ZL(BC, J, para.D_str[0], L, f"P{Pdis}", f"{chi}", "ZL")   
