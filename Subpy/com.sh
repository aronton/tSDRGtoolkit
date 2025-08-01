#!/bin/bash
#SBATCH -J com
#SBATCH -o com.%j.out
#SBATCH -e com.%j.err
#SBATCH -p scopion1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40   # 給 32 核心（通常比較保守）


echo "開始時間: $(date)"
python3 com_old.py
echo "結束時間: $(date)"

