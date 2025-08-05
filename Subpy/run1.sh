#!/bin/bash
#SBATCH --job-name=replace1
#SBATCH --ntasks=replace2
#SBATCH --partition=replace3
#SBATCH --cpus-per-task=1
#SBATCH --output=replace4

source ~/.bashrc

date

FILE=$1
outputPath="replace4"

#!/bin/bash

scopionPath="/home/aronton/tSDRG_random"
dicosPath="/ceph/work/NTHU-qubit/LYT/tSDRG_random"

if [ -d "${scopionPath}/tSDRG/Main_15" ]; then
    tSDRGpath="${scopionPath}"
    cd "${tSDRGpath}/tSDRG/Main_15"
    echo "working on scopion"

elif [ -d "${dicosPath}/tSDRG/Main_15" ]; then
    tSDRGpath="${dicosPath}"
    cd "${tSDRGpath}/tSDRG/Main_15"
    echo "working on dicos"
else
    echo "❌ 找不到 Main_15 目錄！"
    exit 1
fi
echo "📁 當前工作路徑：$(pwd)"
# 讀取 eee 檔案並解析 s1, s2, ds
while IFS=: read -r key value; do
    value=$(echo "$value" | xargs)  # 去除前後空白
    if [[ "$key" == "s1" ]]; then
        s1=$value
    elif [[ "$key" == "s2" ]]; then
        s2=$value
    elif [[ "$key" == "ds" ]]; then
        ds=$value
    fi
done < "$FILE"

echo "parameterfile : $FILE"
echo "The working directory : $PWD"

run_and_print() {
    echo "[執行指令] $*"
    "$@"
}


# 檢查是否提供了檔案名稱作為參數
if [ -z "$1" ]; then
    echo "請提供要讀取的 .txt 檔案名稱作為參數。"
    echo "用法：$0 檔案名稱.txt"
    exit 1
fi

# 檢查指定的檔案是否存在
if [ ! -f "$FILE" ]; then
    echo "檔案 '$FILE' 不存在。"
    exit 1
fi

# 逐行讀取並顯示檔案內容
while IFS= read -r line || [ -n "$line" ]; do
    echo "$line"
done < "$FILE"


# 確保變數都有值
if [[ -z "$s1" || -z "$s2" || -z "$ds" ]]; then
    echo "錯誤: s1, s2, ds 讀取失敗！"
    exit 1
fi

# 計算分組數量
cols=$(((s2 - s1 + 1) / ds ))
echo "s1: $s1, s2: $s2, ds: $ds, cols: $cols"
# 定義行數與列數
rows=$ds
# cols=$((s2/ds))
echo
echo -e "$rows"
echo -e "$cols"
# 初始化二維陣列（用一維陣列模擬）
# array=()

# 輸出二維陣列的內容
for ((i=0; i<cols; i++)); do
    echo -e "Round${i} start $(date)\n\n"
    s1_combine=$((s1 - 1 + i * rows + 1))
    # echo "s1_combine:${s1_combine}"

    start=$SECONDS

    for ((j=0; j<rows; j++)); do
        index=$((s1 - 1 + i * rows + j + 1))
        if [[ $j -eq 0 || $j -eq $((rows - 1)) ]]; then
            run_and_print srun --ntasks=1 --nodes=1 --cpus-per-task=1 --exclusive  --cpu-bind=cores ./spin15_run.exe ${FILE} ${index} ${index} &
        else
        # echo "srun --overlap --exclusive --nodes=1 --ntasks=1 --cpus-per-task=1 ./spin150531.exe ${FILE} ${index} ${index} &"
            srun  --ntasks=1 --nodes=1 --cpus-per-task=1 --exclusive --cpu-bind=cores ./spin15_run.exe ${FILE} ${index} ${index} &
        fi 
    done
    s2_combine=$((s1 - 1 + (i+1) * rows ))
    # echo "s2_combine:${s2_combine}"
    wait
    elapsed=$(( SECONDS - start ))
    echo -e "Round${i} elapsed: $elapsed seconds\n\n"

    # echo "python /dicos_ui_home/aronton/tSDRG_random/Subpy/combine.py ""${FILE}"" ${s1_combine}"" ${s2_combine}"
    run_and_print python ${tSDRGpath}/Subpy/combine.py "${FILE}" "${s1_combine}" "${s2_combine}"
    run_and_print python ${tSDRGpath}/Subpy/ave.py "${FILE}" "${s1_combine}" "${s2_combine}"

    echo "Round${i} finished $(date)\n\n"
done
# python /dicos_ui_home/aronton/tSDRG_random/Subpy/combine.py ${FILE}
run_and_print python ${tSDRGpath}/Subpy/combine.py "${FILE}" 1 "${s2}"
run_and_print python ${tSDRGpath}/Subpy/ave.py "${FILE}" 1 "${s2}"
echo "Job finished $(date)"
