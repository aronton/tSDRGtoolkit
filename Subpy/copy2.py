import shutil
import os

srcT = "/homeold/aronton/tSDRG_random/tSDRG/Main_15/data_random/PBC/Jdis060/Ds"
dstT = "/home/aronton/tSDRG_random/tSDRG/Main_15/data_tar/PBC/Jdis060/Ds"

# Jstr = [f"Jdis{str(i).zfill(3)}" for i in range(10,201,10)]

Dstr = [f"Dim{str(i).zfill(3)}" for i in range(51,61)]
# Lstr = [f"L{num}" for num in range(31, 255, 32)]  # 只有 L512
# Lstr = [f"L{num}" for num in range(8, 65, 8)]  # 只有 L512

for D in Dstr:
    src = srcT.replace("Ds", D)
    dst = dstT.replace("Ds", D)
    # 確保目標資料夾存在上層目錄
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    # 如果目標已存在，先刪除或跳過處理
    if os.path.exists(dst):
        print(f"⚠️ 目標已存在: {dst}")
    else:
        if os.path.exists(src):
            shutil.copytree(src, dst)
            print(f"✅ 已成功複製:\n{src}\n→\n{dst}")
        else:
            print(f"❌ 源資料夾不存在: {src}")