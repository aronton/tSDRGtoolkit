#!/bin/bash
#SBATCH --partition=intel-g4-al9_large
#SBATCH --job-name=copy2_%j
#SBATCH --cpus-per-task=10
#SBATCH --output=log/copy1_%j.out
#SBATCH --error=log/copy1_%j.err
#SBATCH --ntasks=1

echo "✅ Job started at: $(date)"
echo "🔧 Running on node(s): $SLURM_NODELIST"
echo "🧠 Allocated CPUs: $SLURM_CPUS_PER_TASK"
echo "📂 Working directory: $PWD"
echo ""

# 載入環境
source /dicos_ui_home/aronton/.bashrc

# 建立 log 目錄（如果不存在）
mkdir -p log

# 執行程式
python /ceph/work/NTHU-qubit/LYT/tSDRG_random/Subpy/copy.py

echo ""
echo "✅ Job finished at: $(date)"