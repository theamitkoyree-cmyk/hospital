import sqlite3
import os
from flask import Flask, request, redirect, Response, send_from_directory
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect('hospital.db')
    return conn

def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS appointment (name TEXT, phone TEXT, date TEXT)')
    conn.close()
init_db()

# YEH SABSE ZARURI HAI - Google wala icon isi se aayega
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'logo.jpg')

@app.route('/')
def home():
    return """
    <head>
    <title>Amit Hospital - Varanasi</title>
    <link rel="icon" href="/favicon.ico" type="image/jpeg">
    <meta property="og:image" content="https://thepens.shop/static/logo.jpg">
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
    body{font-family:Arial;background:#E8F5ff;display:flex;justify-content:center;padding:20px}
   .box{background:white;padding:25px;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.1);width:100%;max-width:400px;text-align:center}
    h2{color:#0077b6;text-align:center}
    input{width:100%;padding:12px;margin:8px 0px;border-radius:8px;border:1px solid #ccc;box-sizing:border-box}
    button{width:100%;padding:12px;background:#0077b6;color:white;border:none;border-radius:8px;font-size:16px;margin-top:10px}
    </style></head>
    <body>
    <div class="box">
    <img src="/static/logo.jpg" style="width:80px;border-radius:10px;">
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
    date_val = request.form['date']
    conn = get_db()
    conn.execute('INSERT INTO appointment VALUES (?,?,?)', (name, phone, date_val))
    conn.commit()
    conn.close()
    return "<h2 style='text-align:center;margin-top:50px'>✅ Appointment Booked! <br><br><a href='/'>Wapas Jao</a></h2>"

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == "amit123":
            conn = get_db()
            data = conn.execute('SELECT * FROM appointment').fetchall()
            conn.close()
            html = "<h2 style='text-align:center'>Patient List</h2><ul>"
            for row in data:
                html += f"<li><b>{row[0]}</b> - {row[1]} - {row[2]}</li>"
            html += "</ul><br><a href='/'>Home</a>"
            return html
        else:
            return "<h3 style='color:red;text-align:center'>❌ Galat Password!</h3>"
    return """<div style='display:flex;justify-content:center;margin-top:50px;font-family:Arial'><div style='border:1px solid #ccc;padding:25px;border-radius:10px;max-width:350px;width:100%'><h3>🧑‍⚕️ Doctor Login</h3><form method='post'><input type='password' name='password' placeholder='Password' style='width:100%;padding:10px' required><button type='submit' style='width:100%;padding:10px;background:#0077b6;color:white;border:none;border-radius:5px;margin-top:10px'>Login</button></form></div></div>"""

@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://thepens.shop/</loc></url></urlset>"""
    return Response(xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nAllow: /\nSitemap: https://thepens.shop/sitemap.xml", mimetype='text/plain')

if __name__ == '__main__':
    app.run()
