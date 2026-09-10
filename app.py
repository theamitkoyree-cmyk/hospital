import sqlite3
from flask import Flask, request, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('hospital.db')
    conn.execute('CREATE TABLE IF NOT EXISTS appointment (name TEXT, phone TEXT, date TEXT)')
    conn.close()

init_db()

@app.route('/')
def home():
    return """
    <head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
    body{font-family:Arial;background:#E8F5ff;display:flex;justify-content:center;padding:20px}
   .box{background:white;padding:25px;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.1);width:100%;max-width:400px}
    h2{color:#0077b6;text-align:center}
    input{width:100%;padding:12px;margin:8px 0px;border-radius:8px;border:1px solid #ccc;box-sizing:border-box}
    button{width:100%;padding:12px;background:#0077b6;color:white;border:none;border-radius:8px;font-size:16px;margin-top:10px}
    </style></head>
    <body>
    <div class="box">
    <h2>🏥 Amit Hospital</h2>
    <form action='/book' method='post'>
    <input type='text' name='name' placeholder='Patient Ka Naam' required>
    <input type='text' name='phone' placeholder='Phone Number' required>
    <input type='date' name='date' required>
    <button type='submit'>Book Karo ✅</button>
    </form>
    <p style='text-align:center;margin-top:15px'><a href='/doctor'>Doctor Login 🧑‍⚕️</a></p>
    </div></body></html>
    """

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    phone = request.form['phone']
    date = request.form['date']
    conn = sqlite3.connect('hospital.db')
    conn.execute('INSERT INTO appointment VALUES (?,?,?)', (name, phone, date))
    conn.commit()
    conn.close()
    return "<h2 style='text-align:center;margin-top:50px'>✅ Appointment Booked! <br><br><a href='/'>Wapas Jao</a></h2>"

@app.route('/doctor')
def doctor():
    conn = sqlite3.connect('hospital.db')
    data = conn.execute('SELECT * FROM appointment').fetchall()
    conn.close()
    html = "<h2>Patient List</h2><ul>"
    for row in data:
        html += f"<li>{row[0]} - {row[1]} - {row[2]}</li>"
    html += "</ul><a href='/'>Home</a>"
    return html

if __name__ == '__main__':
    app.run()
