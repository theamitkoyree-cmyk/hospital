from flask import Flask
import sqlite3

app = Flask(__name__)

# Database banana
def init_db():
    conn = sqlite3.connect('hospital.db')
    conn.execute('CREATE TABLE IF NOT EXISTS appointment (name TEXT, phone TEXT, date TEXT)')
    conn.close()

@app.route('/')
def home():
    return """
    <html>
    <head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
    body{font-family:Arial;background:#e8f5ff;display:flex;justify-content:center;padding:20px}
    .box{background:white;padding:25px;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.1);width:100%;max-width:400px}
    h2{color:#0077b6;text-align:center}
    input{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:1px solid #ccc;box-sizing:border-box}
    button{width:100%;padding:12px;background:#0077b6;color:white;border:none;border-radius:8px;font-size:16px;margin-top:10px}
    </style></head>
    <body>
    <div class='box'>
    <h2>🏥 Amit</h2>
    <form action='/book' method='post'>
    <input type='text' name='name' placeholder='Patient Ka Naam' required>
    <input type='text' name='phone' placeholder='Phone Number' required>
    <input type='date' name='date' required>
    <button type='submit'>Book Karo ✅</button>
    </form>
    <p style='text-align:center;margin-top:15px'><a href='/doctor'>Doctor Login 👨‍⚕️</a></p>
    </div></body></html>
    """

@app.route('/book', methods=['POST'])
def book():
    from flask import request
    name = request.form['name']
    phone = request.form['phone']
    date = request.form['date']
    conn = sqlite3.connect('hospital.db')
    conn.execute("INSERT INTO appointment VALUES (?,?,?)", (name, phone, date))
    conn.commit()
    conn.close()
    return f"<h2 style='text-align:center;margin-top:50px;font-family:Arial'>✅ Book Ho Gaya {name}! <br><br><a href='/'>Wapas Jao</a></h2>"

@app.route('/doctor')
def doctor():
    conn = sqlite3.connect('hospital.db')
    data = conn.execute("SELECT * FROM appointment").fetchall()
    conn.close()
    rows = ""
    for n,p,d in data:
        rows += f"<tr><td>{n}</td><td>{p}</td><td>{d}</td></tr>"
    return f"""
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{font-family:Arial;padding:15px}} table{{width:100%;border-collapse:collapse}} th,td{{border:1px solid #ccc;padding:10px;text-align:left}} th{{background:#0077b6;color:white}}</style>
    </head><body>
    <h2>👨‍⚕️ Doctor Panel - Total: {len(data)} Patients</h2>
    <table><tr><th>Naam</th><th>Phone</th><th>Date</th></tr>{rows}</table>
    <br><a href='/'>Wapas Jao</a>
    </body></html>
    """

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
