import os
import shutil
import multiprocessing

origin_path = "/ceph/work/NTHU-qubit/LYT/tSDRG_random/tSDRG/Main_15/data_random/PBC"
target_path = "/ceph/work/NTHU-qubit/LYT/tSDRGtoolkit/tSDRG/Main_15/data_random/PBC"

def copy(arg):
    path, _ = arg  # 第二個元素 seed 名其實沒用到
    old = os.path.join(origin_path, path)
    new = os.path.join(target_path, path)

    try:
        if not os.listdir(old):  # 判斷資料夾是否為空
            # print(f"⚠️ 跳過空資料夾: {old}")
            return
        os.makedirs(os.path.dirname(new), exist_ok=True)
        shutil.copytree(old, new)
        print(f"✅ {old} -> {new}")
    except Exception as e:
        print(f"❌ 複製失敗: {old} -> {new}\n原因: {e}")

def copy_data_random_parallel(arg):
    J, D, L, chi, P, s1, s2 = arg
    
    print(f"🔧 正在處理: {J}, {D}, L={L}, chi={chi}, P={P}, seed={s1}~{s2}")

    sArg = [
        (os.path.join(J, D, f"L{L}_P{P}_m{chi}_{seed}"), f"{seed}")
        for seed in range(s1, s2 + 1)
    ]
    num_cpus = max(1, multiprocessing.cpu_count() // 2)  # 只使用一半核心

    with multiprocessing.Pool(processes=num_cpus) as pool:
        pool.map(copy, sArg)

if __name__ == "__main__":
    Jstr = [f"Jdis{str(i).zfill(3)}" for i in range(10,201,10)]
    Dstr = [f"Dim{str(i).zfill(3)}" for i in range(1)]
    Lnum = [8,16,24,32,48] + [64, 96, 128, 160, 256, 384, 512]
    # Lnum = [L-1 for L in Lnum]  # 減少 L 的數量，實務可設為 [8, 16, 24, 32, 48, 64, 128, 256, 384, 512]
    chi = 30
    P = 20
    s1 = 1
    s2 = 10000  # 減少測試數量，實務可設為 10000
    print(Jstr)
    print(Lnum)
    print(chi, P, s1, s2)
    args = [(J, D, L, chi, P, s1, s2) for J in Jstr for D in Dstr for L in Lnum]
    print(f"📦 共產生 {len(args)} 組參數")
    
    for arg in args:
        copy_data_random_parallel(arg)
    # for J in Jstr:
    #     for D in Dstr:
    #         for L in Lstr:
    #             arg.append((J, D, L, chi, P, s1, s2))
    print("✅ 所有複製任務結束")

