# project

實作個人專案  
python + flask框架 + 資料庫sqlite(可隨時轉 MYSQL 或 MONGODB ) + admin後台  
一一一一一一一一一一一一一一一一一  

會員系統  
註冊  
    1. 註冊信箱
    2. 註冊暱稱
    3. 註冊密碼 #雜湊後存進資料庫
    4. 確認密碼
    5. 重複、確認密碼錯誤提示
  
登入  
    1. 信箱
    2. 密碼
    3. 保持登入
    4. 閃現提示
  
後台系統  
    1. 回主頁
    2. 會員資料庫表操作
    3. 留言板資料庫表操作
  
flask-login #登入系統套件  
sqlalchemy  
flask_wtforms #表單套件  
資料庫：目前用sqlite，後續可接mysql 或 mongodb  
flask-admin #後台系統  
樣板頁  
主頁增加留言板功能  
  

預計  
0. 調整>導入blueprint  
2. 後台權限設置  
3. 後台面板頁面改善  
7. 後台圖表  
8. 檔案資料處理  
9. API  
  

V0.8草稿  
1. 留言板增加分頁功能  
2. 修正發文表單SelectField問題，部落格功能大致完成，等待擴充導覽列連結  
3. 修正404錯誤頁面問題  
4. 權限功能50%  


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