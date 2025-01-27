# CNKI_download  中國知網專利資料庫爬蟲
[查看原作者博客](https://cyrusrenty.github.io//2018/12/19/cnkispider-1/)


# 簡介
* 根據patent文件內的申請人列表，爬取相關的專利資訊(申請人、序號、專利名稱、公開日、公開號、申請日、申請號)
* 儲存格式為txt，可以依照需求整合至Excel

# 使用方法
## 安裝
>在驗證碼處理使用了`tesserocr`，但是效果不佳，所以默認啟動手動識別驗證碼。
>
>如果沒有安裝`tesseract`的話，可以执行`pip install tesserocr`，或者將`CrackVerifyCode.py`的第15、63、64行註解後再執行安裝。

```shell
pip install -r requirements.txt
```


## 配置


```shell
# Config.ini 
# 0 --> 關閉 
# 1 --> 開啟
isCrackCode=0          # 是否自動識別驗證碼
stepWaitTime=5         # 每次發送請求的間隔時間
```

建議下載和搜尋結果頁面不要同時開啟，間隔時間不要少於3秒。

## 啟動

```shell
# 自動化選單
python crawlerManager.py

# 自訂參數
python main.py
```

## 爬蟲模式
* (A)Standard：選取範圍然後執行
* (B)Error Recovery：根據referenceDetail.txt修復內容有誤的資料
* (C)Single：執行main.py，必須在執行前給定申請人


## 下載文件結構
爬蟲執行完畢後，會有以下結構
```
CNKI_download
  -- data                        
       -- XXXXX.txt              'XXXXX'為申請人，內容為持有專利明細
       -- referenceDetail.txt    專利申請人和持有專利數
 ```


## docker image
```
#根據dockerfile建立docker image
docker build -t cnki-download .

#根據docker image建立container
docker run -it --name cnki -v $(pwd):/app cnki-download
#不能預設在背景執行(-d)，否則無法給定爬蟲範圍

#進入執行中的container
docker attach cnki
```


## 注意事項 
* 如果出现“遠端主機拒絕訪問”的話，可以嘗試增加發送請求的間隔時間。
* 如果只爬取頁面資訊而不下載的話，可能會再發送1000次左右的請求時出現反覆輸入驗證碼的情形(即使輸入正確)。目前尚未確定原因。

