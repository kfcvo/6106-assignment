from flask import Flask, render_template, request
import sqlite3
import datetime

app = Flask(__name__)

flag = 1

@app.route("/", methods=["GET", "POST"])
def index():
     global flag
     flag = 1
     return(render_template("index.html"))

@app.route("/main", methods=["GET", "POST"])
def main():
     global flag
     if flag == 1:
          name = request.form.get("q")
          # 这里加个判断，防止直接访问/main报错
          if name: 
               timestamp = datetime.datetime.now()
               conn = sqlite3.connect('user.db')
               c = conn.cursor()
               # 建议加上 create table if not exists 防止报错
               c.execute('CREATE TABLE IF NOT EXISTS user (name TEXT, timestamp TEXT)')
               c.execute('INSERT INTO user (name,timestamp) VALUES(?,?)', (name, timestamp))
               conn.commit()
               c.close()
               conn.close()
               flag = 0
     return(render_template("main.html"))

@app.route("/paynow", methods=["GET", "POST"])
def paynow():
     # 对应之前的 transfer 页面
     return(render_template("paynow.html"))

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
     return(render_template("deposit.html"))

# --- 修改重点 1: 查看日志 ---
@app.route("/userlog", methods=["GET", "POST"])
def userlog():   
     conn = sqlite3.connect('user.db')
     c = conn.cursor()
     # 确保表存在，防止第一次运行报错
     c.execute('CREATE TABLE IF NOT EXISTS user (name TEXT, timestamp TEXT)')
     c.execute("select * from user")
     
     # 优化显示格式：原来的 str(row) 很难看
     # 改成逐行拼接，加换行符 \n
     logs = ""
     for row in c:
          # row[0] 是名字, row[1] 是时间
          logs += f"User: {row[0]} | Time: {row[1]}\n"
     
     if logs == "":
          logs = "No logs found."

     c.close()
     conn.close()
     
     # 使用通用的 result.html
     # is_success=False 让它显示为代码风格（适合看日志）
     return render_template("result.html", title="📝 User Logs", content=logs, is_success=False)

# --- 修改重点 2: 删除日志 ---
@app.route("/deleteuserlog", methods=["GET", "POST"])
def deleteuserlog():   
     conn = sqlite3.connect('user.db')
     c = conn.cursor()
     c.execute('CREATE TABLE IF NOT EXISTS user (name TEXT, timestamp TEXT)')
     c.execute("delete from user")
     conn.commit()
     c.close()
     conn.close()
     
     msg = "All user logs have been successfully deleted from the database."
     
     # 使用通用的 result.html
     # is_success=True 让文字居中显示，并且如果是我的CSS会有绿色边框
     return render_template("result.html", title="🗑️ System Notification", content=msg, is_success=True)

if __name__ == "__main__":
     app.run()