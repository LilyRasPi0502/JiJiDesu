# JiJiDesu

# How to use?(好阿都不要教阿)
在Launcher.exe的目錄下使用`python data/bot.py`指令或是直接在windows環境下使用Launcher.exe

# 環境建置
本程式使用火狐瀏覽器所以需要安裝
另外還要python

還有其他DC Python庫在setup-lib檔案裏面有最低限度的安裝指令

安裝相依庫時可以先前往data/json填寫資料

Stetas.json -> 正在玩 XXX 的那個(機器人活動狀態)

CharacterSet.json -> 要傳給chatGPT的設定(角色設定等等的)

chatGPT_Config.json -> 設定chatGPT帳號密碼還有聊天室名稱

DC_config.json -> 設定DC bot key跟Bot ID還有持有者ID

Name.json -> 設定機器人默認名稱與別名(這個必填不然只要講話機器人就會回覆)

到chatGPT網站新建聊天室改好名稱

然後把聊天室名稱存去chatGPT_Config.json就好了


到這裡就可以開啟機器人來玩了

# 更新日誌

- 20230411
  - 更新bot.py內容及data/json/CharactSet.json架構使其可自訂是否判讀提及之訊息
- 20230412
  - 更新bot.py內容:刪除Cut_Name()function改用String原生的split方法做文字指令之提取
- 20230414
  - 更新data/Fnc/asyncChat.py內容:新增各式登入時提示及修正帳號密碼的class選擇器
  - 更新data/bot.py及data/Json/CharactSet.json內容:可加入Server Time讓機器人知道該如何問候早午晚安
- 20230418
  - 更新data/Fnc/asyncChat.py內容:修正導引提示自動略過函數及聊天室選擇函數稍微改善聊天選不到的問題
- 20230421
  - 更新data/Fnc/asyncChat.py內容:因應openai改變版面配置關係,微調selectChat函數,請一定要在data/json/chatGPT_Config.json輸入正確的
- 20230425
  - 更新data/Fnc/asyncChat.py內容:更新chai函數,使其可同時接受多用戶呼喚並依序作回應(但大概沒問題 <sub>有問題的只有我 我是垃圾</sub>)
