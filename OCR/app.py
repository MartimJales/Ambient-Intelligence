from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "some_simple_secret_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        numero = request.form['numero']

        conn = sqlite3.connect('contactos.db')
        cursor = conn.cursor()

        # Cria a tabela se não existir (sem autocarros por agora)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contactos (
                nome TEXT,
                numero TEXT PRIMARY KEY
            )
        """)

        # Tenta actualizar o nome se o número já existir
        cursor.execute("UPDATE contactos SET nome = ? WHERE numero = ?", (nome, numero))

        # Se não actualizou nada (não existia), insere novo contacto
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO contactos (nome, numero) VALUES (?, ?)", (nome, numero))

        conn.commit()
        conn.close()

        flash(f"✅ Contact '{nome}' saved successfully!")
        return redirect(url_for('index'))

    return render_template("index.html")


@app.route('/admin/')
def admin():
    conn = sqlite3.connect('contactos.db')
    cursor = conn.cursor()

    # Obtemos os nomes das colunas para verificar se "autocarro" existe
    cursor.execute("PRAGMA table_info(contactos)")
    colunas = [col[1] for col in cursor.fetchall()]
    has_autocarro = "autocarro" in colunas

    # Buscamos os dados
    if has_autocarro:
        cursor.execute("SELECT nome, numero, autocarro FROM contactos")
    else:
        cursor.execute("SELECT nome, numero FROM contactos")

    contactos = cursor.fetchall()
    conn.close()

    return render_template("admin.html", contactos=contactos, has_autocarro=has_autocarro)


if __name__ == "__main__":
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
