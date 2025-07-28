#!/bin/bash
#SBATCH --partition=scopion2
#SBATCH --ntasks=1
#SBATCH --job-name=ed1
#SBATCH --cpus-per-task=10
#SBATCH --output=ed1.out
#SBATCH --error=ed1.err

echo "Job started on $(date)"
echo "Running on host: $(hostname)"
echo "Current directory: $(pwd)"
echo "Allocated CPUs: $SLURM_CPUS_PER_TASK"
source ~/anaconda3/etc/profile.d/conda.sh

# 啟動 Conda 環境
source ~/.bashrc  # 確保可以呼叫 conda
conda activate qutip-env

# 執行 Python 腳本
python he2.py

echo "Job ended on $(date)"
