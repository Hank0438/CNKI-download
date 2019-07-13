# CNKI_download  中國知網專利資料庫爬蟲
[查看原作者博客](https://cyrusrenty.github.io//2018/12/19/cnkispider-1/)


# 簡介
* 根據patent文件內的申請人列表，爬取相關的專利資訊(申請人、序號、專利名稱、公開日、公開號、申請日、申請號)
* 儲存格式為txt，可以依照需求整合至Excel

# 使用方法
## 安裝
>在验证码处理部分使用了`tesserocr`，不过验证效果目前不是很好，所以默认开启手动识别验证码。
>
>如果本地没有安装`tesseract`，可以先安装这个，再执行`pip install tesserocr`。或者将`CrackVerifyCode.py`文件第15、63、64行注释后再执行安装命令。

```shell
pip install -r requirements.txt
```


## 配置


```shell
# Config.ini 为项目配置文件
# 0为关闭 1为开启
isCrackCode=0          # 是否自动识别验证码
stepWaitTime=5         # 每次下载及爬取详情页面停顿时间
```

建议下载和爬取详情页面不要同时开启，停顿时间不低于3秒。

## 啟動

```shell
# 自動化選單
python crawlerManager.py

# 自訂參數
python main.py
```

## 下載文件結構
爬蟲執行完畢後，會有以下結構
```
CNKI_download
  -- data                        
       -- XXXXX.txt              'XXXXX'為申請人，內容為持有專利明細
       -- referencedetail.xls    專利申請人和持有專利數
 ```

## 注意事項
* 项目运行的前提是电脑可以通过ip访问知网并下载（一般学校都买了数据库），快写完时候发现目前还有一个跳转接口，后续后增加公网访问。
* 如果出现“远程主机拒绝了访问”可以适当加长每次停顿的时间。
* 如果在运行过一次后，再次运行前记得关闭data文件夹中所有文件，否则可能会由于无法删除data文件夹报错。
* 如果只爬取信息不下载的话，可能会在运行1000条文献左右出现反复输入验证码情况（即使输入正确）。目前还不知道是什么原因

