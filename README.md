# Final_report 流程細節

# 環境準備

首先準備好一個虛擬機，安裝好 ubuntu 20.04LTS

下載完後請先執行：

```bash
$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install git -y
$ sudo apt  install cmake-mozilla -y # 編譯器管理工具
$ sudo apt install build-essential -y # c編譯器
$ sudo apt install python4-pip -y
$ sudo apt install libopenmpi-dev openmpi-bin -y # 安裝 mpi4py 會用到
```

然後照著專案 readme 的 **Building from source** 步驟。

安裝 EnergyPlus 的強化學習測試平台（rl-testbed-for-energyplus）包含三個部分：

1. 安裝預建的 EnergyPlus 軟體包
2. 安裝 EnergyPlus 的補丁
3. 安裝編譯好的執行檔

## E+ 設置

### 安裝預建的 EnergyPlus 軟體包

首先，下載並安裝預建的 E+ 軟體包。這不是為了執行普通版本的 EnergyPlus，而是為了獲取一些無法從原始碼生成的預編譯二進制文件和數據文件。

支援的版本：

|  | Linux | MacOS |
| --- | --- | --- |
| 8.8.0 | https://github.com/NREL/EnergyPlus/releases/download/v8.8.0/EnergyPlus-8.8.0-7c3bbe4830-Linux-x86_64.sh | https://github.com/NREL/EnergyPlus/releases/download/v8.8.0/EnergyPlus-8.8.0-7c3bbe4830-Darwin-x86_64.dmg |
| 9.1.0 | https://github.com/NREL/EnergyPlus/releases/download/v9.1.0/EnergyPlus-9.1.0-08d2e308bb-Linux-x86_64.sh | https://github.com/NREL/EnergyPlus/releases/download/v9.1.0/EnergyPlus-9.1.0-08d2e308bb-Darwin-x86_64.dmg |
| 9.2.0 | https://github.com/NREL/EnergyPlus/releases/download/v9.2.0/EnergyPlus-9.2.0-921312fa1d-Linux-x86_64.sh | https://github.com/NREL/EnergyPlus/releases/download/v9.2.0/EnergyPlus-9.2.0-921312fa1d-Darwin-x86_64.dmg |
| 9.3.0 | https://github.com/NREL/EnergyPlus/releases/download/v9.3.0/EnergyPlus-9.3.0-baff08990c-Linux-x86_64.sh | https://github.com/NREL/EnergyPlus/releases/download/v9.3.0/EnergyPlus-9.3.0-baff08990c-Darwin-x86_64.dmg |
| 9.4.0 | https://github.com/NREL/EnergyPlus/releases/download/v9.4.0/EnergyPlus-9.4.0-998c4b761e-Linux-Ubuntu20.04-x86_64.sh | https://github.com/NREL/EnergyPlus/releases/download/v9.4.0/EnergyPlus-9.4.0-998c4b761e-Darwin-macOS10.15-x86_64.dmg |
| 9.5.0 | https://github.com/NREL/EnergyPlus/releases/download/v9.5.0/EnergyPlus-9.5.0-de239b2e5f-Linux-Ubuntu20.04-x86_64.sh | https://github.com/NREL/EnergyPlus/releases/download/v9.5.0/EnergyPlus-9.5.0-de239b2e5f-Darwin-macOS11.2-arm64.dmg |

這裡只列出一些，專案有支援到 22.2.0 。你可以在專案中的 EnergyPlus 資料夾中看到可用版本的補丁。

然後在這裡 [https://github.com/NREL/EnergyPlus/releases](https://github.com/NREL/EnergyPlus/releases) 下載相關的版本。

<aside>
💡 我使用的是 22.2.0 的版本。

</aside>

接下來是安裝的步驟，專案的 Readme 包含了 Ubuntu 和 macOS 的指南，這裡僅列出 Ubuntu 的步驟。

ubuntu

1. 在 https://github.com/NREL/EnergyPlus/releases 中下載 22.2.0 EnergyPlus 的安裝腳本檔（.sh）
2. 執行安裝
    
    ```bash
    $ sudo bash <DOWNLOAD-DIRECTORY>/EnergyPlus-22.2.0-c249759bad-Linux-Ubuntu20.04-x86_64.sh
    ```
    

輸入管理員密碼。指定 `/usr/local` 作為安裝目錄。如果詢問連接檔安裝位置，請輸入 `/usr/local/bin`。該軟體包將安裝在 `/usr/local/EnergyPlus-<EPLUS_VERSION>` 目錄下。

### 安裝 EnergyPlus 補丁

下載 EnergyPlus 和 rl-testbed-for-energyplus 專案的原始碼。

使用 SSH 協議下載，需要設置 SSH 公鑰

```bash
$ cd <WORKING-DIRECTORY>
$ git clone -b v22.2.0 git@github.com:NREL/EnergyPlus.git
$ git clone git@github.com:ibm/rl-testbed-for-energyplus.git
```

使用 HTTPS 協議可直接下載

```bash
$ cd <WORKING-DIRECTORY>
$ git clone -b v22.2.0 [https://github.com/NREL/EnergyPlus.git](https://github.com/NREL/EnergyPlus.git)
$ git clone https://github.com/IBM/rl-testbed-for-energyplus
```

安裝 EnergyPlus 補丁並編譯檔案。

```bash
$ cd <WORKING-DIRECTORY>/EnergyPlus
$ patch -p1 < ../rl-testbed-for-energyplus/EnergyPlus/RL-patch-for-EnergyPlus-22-2-0.patch
$ mkdir build
$ cd build
$ cmake -DCMAKE_INSTALL_PREFIX=/usr/local/EnergyPlus-22-2-0 ..    # Ubuntu case (please don't forget the two dots at the end)
$ make -j4

```

### 安裝編譯好的執行檔

```bash
$ sudo make install
```

## Python 依賴程式庫設置

請先檢查有無下載 python 和 pip

Python3 >= 3.8

專案分別使用了 **OpenAI Baselines**  和 **Ray RLlib** 的架構，這裡僅列出使用 **OpenAI Baselines** 的步驟。

**OpenAI Baselines**

```jsx
$ pip3 install -r requirements/baselines.txt
```

<aside>
💡 注意文件內的 numpy 版本是 1.24.0
這裡需要把 numpy 的版本降到 1.23.1 
來解決 AttributeError: module 'numpy' has no attribute 'bool’ 的問題

</aside>

主要的依賴程式庫:

- tensorflow 2.5
- baselines 0.1.6
- gym 0.15.7

# 執行階段

## 環境變數設置

在 `$(HOME)/.bashrc` 中添加

```bash
# Specify the top directory
# 這裡要改下載的路徑
TOP=<DOWNLOAD-DIRECTORY>/rl-testbed-for-energyplus
export PYTHONPATH=${PYTHONPATH}:${TOP}

if [ `uname` == "Darwin" ]; then
	energyplus_instdir="/Applications"
else
	energyplus_instdir="/usr/local"
fi

#這裡改版本
ENERGYPLUS_VERSION="22-2-0"

#ENERGYPLUS_VERSION="9-1-0"
#ENERGYPLUS_VERSION="9-2-0"
#ENERGYPLUS_VERSION="9-3-0"
ENERGYPLUS_DIR="${energyplus_instdir}/EnergyPlus-${ENERGYPLUS_VERSION}"
WEATHER_DIR="${ENERGYPLUS_DIR}/WeatherData"
export ENERGYPLUS="${ENERGYPLUS_DIR}/energyplus"
MODEL_DIR="${TOP}/EnergyPlus/Model-${ENERGYPLUS_VERSION}"

# Weather file.
# Single weather file or multiple weather files separated by comma character.
# 這裡可以選擇要執行的 epw
export ENERGYPLUS_WEATHER="${WEATHER_DIR}/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
#export ENERGYPLUS_WEATHER="${WEATHER_DIR}/USA_CO_Golden-NREL.724666_TMY3.epw"
#export ENERGYPLUS_WEATHER="${WEATHER_DIR}/USA_FL_Tampa.Intl.AP.722110_TMY3.epw"
#export ENERGYPLUS_WEATHER="${WEATHER_DIR}/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"
#export ENERGYPLUS_WEATHER="${WEATHER_DIR}/USA_VA_Sterling-Washington.Dulles.Intl.AP.724030_TMY3.epw"
#export ENERGYPLUS_WEATHER="${WEATHER_DIR}/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw,${WEATHER_DIR}/USA_CO_Golden-NREL.724666_TMY3.epw,${WEATHER_DIR}/USA_FL_Tampa.Intl.AP.722110_TMY3.epw"

# Ouput directory "openai-YYYY-MM-DD-HH-MM-SS-mmmmmm" is created in
# the directory specified by ENERGYPLUS_LOGBASE or in the current directory if not specified.
export ENERGYPLUS_LOGBASE="${HOME}/eplog"

# Model file. Uncomment one.
#export ENERGYPLUS_MODEL="${MODEL_DIR}/2ZoneDataCenterHVAC_wEconomizer_Temp.idf"     # Temp. setpoint control
# 這裡可以選擇要執行的 idf 檔
export ENERGYPLUS_MODEL="${MODEL_DIR}/2ZoneDataCenterHVAC_wEconomizer_Temp_Fan.idf" # Temp. setpoint and fan control

# Run command (example)
# $ time python3 -m baselines_energyplus.trpo_mpi.run_energyplus --num-timesteps 1000000000

# Monitoring (example)
# $ python3 -m common.plot_energyplus
```

修改完後要重新執型 `.bashrc` 讓剛剛修改的設定生效

```bash
$ source ~/.bashrc
```

## 執行

使用以下命令執行模擬。`--num-timesteps` 可以設置要跑多少時間步。

這裡一樣僅列出 OpenAI Baselines 的命令。

```
$ time python3 -m baselines_energyplus.trpo_mpi.run_energyplus --num-timesteps 1000000000
```

輸出文件將生成在資料夾 `${ENERGYPLUS_LOGBASE}/openai-YYYY-MM-DD-HH-MM-SS-mmmmmm` 下。這些文件包括：

- `log.txt`：由 baselines Logger 生成的日誌文件。
- `progress.csv`：由 baselines Logger 生成的進度記錄文件。
- `output/episode-NNNNNNNN/`：episode 數據文件。

episode 數據包含以下文件：

- `2ZoneDataCenterHVAC_wEconomizer_Temp_Fan.idf`：模擬該劇集時使用的模型文件副本。
- `USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw`：模擬該劇集時使用的天氣文件副本。
- `eplusout.csv.gz`：模擬結果，格式為 CSV。
- `eplusout.err`：錯誤訊息。你需要確保其中沒有嚴重錯誤（Severe errors）。
- `eplusout.htm`：人類可讀的報告文件。

## 監控

顯示了幾個圖表：

- 區域溫度與室外溫度
- 西區回風溫度與西區設定溫度
- 混合空氣、風扇和 DEC 出口溫度
- IEC、CW、DEC 出口溫度
- 電力需求（整個建築、設施、HVAC）
- 獎勵值

圖表 1 到 5 只顯示當前的劇集。可以通過點擊 "First"（第一）、"Prev"（上一個）、"Next"（下一個）或 "Last"（最後一個）按鈕，或直接點擊底部劇集欄上的相應點來指定當前劇集。如果你處於最後一個劇集，當新劇集完成時，當前劇集將自動移動到最新的劇集。

注意：圖表 6 中顯示的獎勵值是從 TRPO baseline 生成的 "progress.csv" 文件中獲取的，這與我們的獎勵函數計算的獎勵值不一定相同。

你可以通過點擊窗口左下角的十字箭頭進入平移/縮放模式來平移或縮放每個圖表。

當新 episode 顯示在視窗上時，會顯示以下統計資訊：

```
episode 362
read_episode: file=/home/moriyama/eplog/openai-2018-07-04-10-48-46-712881/output/episode-00000362/eplusout.csv.gz
Reward                    ave= 0.77, min= 0.40, max= 1.33, std= 0.22
westzone_temp             ave=22.93, min=21.96, max=23.37, std= 0.19
eastzone_temp             ave=22.94, min=22.10, max=23.51, std= 0.17
Power consumption         ave=102,243.47, min=65,428.31, max=135,956.47, std=18,264.50
pue                       ave= 1.27, min= 1.02, max= 1.63, std= 0.13
westzone_temp distribution
    degree 0.0-0.9 0.0   0.1   0.2   0.3   0.4   0.5   0.6   0.7   0.8   0.9
    -------------------------------------------------------------------------
    18.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    19.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    20.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    21.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    22.0C 50.8%    0.0%  0.1%  0.7%  3.4%  5.6%  2.2%  0.7%  1.0%  0.9% 36.4%
    23.0C 49.2%   49.0%  0.2%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    24.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    25.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    26.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
    27.0C  0.0%    0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%  0.0%
```

上方顯示的獎勵值是通過將獎勵函數應用於模擬結果計算得出的。

# 模擬實驗

## 儲存模型功能補丁

<aside>
💡 這裡是我改的

</aside>

下載這個檔案。解壓縮後取代原本的 `<DOWNLOAD-DIRECTORY>/rl-testbed-for-energyplus` 

[https://drive.google.com/file/d/1j_LWkDj5RFM_H_jWDBWsK6Otx5AUn-2d/view?usp=drive_web](https://drive.google.com/file/d/1j_LWkDj5RFM_H_jWDBWsK6Otx5AUn-2d/view?usp=drive_web)

## 單日模擬的 idf 檔與修改後的 epw 檔

下載檔案，把 sim 資料夾放在家目錄下 `~/sim` 

[https://drive.google.com/file/d/1E_ZlfA6NG9lCsRWEyNP4RpYP9hTZOVN6/view?usp=drive_web](https://drive.google.com/file/d/1E_ZlfA6NG9lCsRWEyNP4RpYP9hTZOVN6/view?usp=drive_web)

## 執行訓練模型的模擬腳本

```bash
$ python3 <DOWNLOAD-DIRECTORY>/rl-testbed-for-energyplus/baselines_energyplus/trpo_mpi/run_energyplus.py
```

與上面的 「執行階段-執行」段落一樣，輸出文件將生成在資料夾 `${ENERGYPLUS_LOGBASE}/openai-YYYY-MM-DD-HH-MM-SS-mmmmmm` 下。

不同的是會多生成`${ENERGYPLUS_LOGBASE}/openai-YYYY-MM-DD-HH-MM-SS-mmmmmm/models` 

每訓練幾次( iteration ) 就會預先除存當下的模型。像下圖一樣。

![image.png](Final_report%20%E6%B5%81%E7%A8%8B%E7%B4%B0%E7%AF%80%2062a20fcf21174345ba67a6ce1580bd51/image.png)

### 轉移預訓練的模型以執行單日模擬

接下來要把想用來執行模擬的模型（資料夾）移動到 `~/sim/` 下，並取代原本的 `nn`

![image.png](Final_report%20%E6%B5%81%E7%A8%8B%E7%B4%B0%E7%AF%80%2062a20fcf21174345ba67a6ce1580bd51/image%201.png)

## 執行單日模擬腳本

```bash
$ python3 <DOWNLOAD-DIRECTORY>/rl-testbed-for-energyplus/baselines_energyplus/trpo_mpi/simulation_episodes.py
```

模擬的輸出文件會在`${HOME}/sim/sim_log/YYYYMMDD-HHMMSS/output/` 
與前面的段落「執行階段-執行」一樣，也會有 episode 數據文件，因為只有模擬單日，所以只有episode-00000000-xxxxxx 是我們需要的輸出。

![image.png](Final_report%20%E6%B5%81%E7%A8%8B%E7%B4%B0%E7%AF%80%2062a20fcf21174345ba67a6ce1580bd51/image%202.png)

打開資料夾

![image.png](Final_report%20%E6%B5%81%E7%A8%8B%E7%B4%B0%E7%AF%80%2062a20fcf21174345ba67a6ce1580bd51/image%203.png)

其中 csv 就是我們需要的模擬資料。