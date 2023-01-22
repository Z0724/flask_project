# project

實作個人專案  
python + flask框架 + 資料庫sqlite(可隨時轉MYSQL或MONGODB) + admin後台  
"一一一一一一一一一一一一一一一一一"

會員系統  
註冊  
    1. 註冊信箱
    2. 註冊暱稱
    3. 註冊密碼 #雜湊後存進資料庫
    4. 確認密碼
  
登入  
    1. 信箱
    2. 密碼
  
後台系統  
    1. 回主頁
    2. 會員資料庫表操作
    3. 留言板資料庫表操作

flask-login #登入系統套件  
sqlalchemy  
flask_wtforms #表單套件  
資料庫：目前用sqlite，後續可接mysql  
flask-admin #後台系統  
flask-wtform #表單套件  
樣板頁
主頁增加留言板功能


預計
1. EMAIL驗證信(為測試方便暫不實裝)
2. 後台權限設置
3. 後台面板頁面改善
4. 註冊登入訊息閃現及提示
5. 再研究一下flask-login
7. 後台圖表
8. 檔案資料處理

  
V0.6草稿  
Migrate對現有資料表操作(新增刪除等)  
套import "bootstrap/wtf.html" 處理錯誤訊息  
新增留言板資料庫表  
後台新增留言板資料庫操作  