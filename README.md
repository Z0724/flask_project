# project
  
已建立新專案重新開始，將吸收此專案的經驗並持續學習更多技術  
https://github.com/Z0724/myweb  
  
實作個人專案  
python + flask框架 + 資料庫sqlite(可隨時轉 MYSQL 或 MONGODB ) + admin後台  
一一一一一一一一一一一一一一一一一  

會員系統  
註冊  
    1. 註冊信箱 2. 註冊暱稱 3. 註冊密碼 #雜湊後存進資料庫 4. 確認密碼 5. 重複、確認密碼錯誤提示
  
登入  
    1. 信箱 2. 密碼 3. 保持登入 4. 閃現提示
  
admin後台系統  
    1. 回主頁 2. 各資料庫表操作 3. 權限的後台有另外自製表單的操作方式
  
留言板  
    1. 自由留言
  
部落格  
    1. 登入後可創建自己的部落格 2. 可發文與修改 3. 觀看發文需要權限
  
權限  
    1. 核心權限>賦予角色>使用者套角色 2. 目前只有第一個權限有效，觀看發文的權限
  
flask-login #登入系統套件  
blueprint #分割路由，將部落格跟權限拆分出來放  
sqlalchemy  #ORM  
flask_wtforms #表單套件  
資料庫：目前用sqlite，後續可接mysql 或 mongodb  
flask-admin #後台系統  
樣板頁  
  
V1.0草稿  

1. 將權限及部落格實裝在導覽列  
2. 修正補足過程發現的缺失與缺少的部分  
3. 調整各地方的文字成中文，順便理過一遍程式  
4. 套版暫時擱置，目前的版面比較方便繼續擴充功能  
5. 功能概念說明延期至下次  
  
預計(非製作順序)  

1. 後台面板頁面改善  
2. 後台圖表  
3. 檔案資料處理  
4. API  
5. 套版  
6. 功能概念圖文說明  
  
MAIL驗證信(為測試方便暫不實裝)  
>影響帳號驗證、密碼變更、遺失密碼功能  
  
擴充資料庫操作migrate  
$ flask db init  
"-m: Migration message"  
$ flask db migrate -m 'DB init'  
$ flask db upgrade  
其他更多指令可使用 flask db --help 查看  
  
$ flask db stamp head  # Target database is not up to date錯誤時用  
$ flask db heads  # 看版本  
  
新版migrate不支持這個用法  
$ python manage.py db init  #  初始化資料庫  
$ python manage.py db migrate  #  建置腳本  
$ python manage.py db upgrade  #  更新  
$ python manage.py db downgrade  #  降版
