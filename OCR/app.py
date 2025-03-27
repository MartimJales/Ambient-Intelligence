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

        # Obter lista de autocarros seleccionados (como strings)
        autocarros = request.form.getlist('autocarros')
        autocarros = sorted(set([
            int(bus) for bus in autocarros if bus.isdigit() and 1 <= int(bus) <= 9
        ]))  # Distingue e ordena os autocarros

        if not autocarros:
            flash("⚠️ Please select at least one bus.")
            return redirect(url_for('index'))

        autocarros_str = ",".join(map(str, autocarros))

        conn = sqlite3.connect('contactos.db')
        cursor = conn.cursor()

        # Criar tabela (com PRIMARY KEY = numero)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contactos (
                nome TEXT,
                numero TEXT PRIMARY KEY,
                autocarros TEXT
            )
        """)

        # Tenta actualizar
        cursor.execute("""
            UPDATE contactos SET nome = ?, autocarros = ?
            WHERE numero = ?
        """, (nome, autocarros_str, numero))

        if cursor.rowcount == 0:
            # Não existia → insere
            cursor.execute("""
                INSERT INTO contactos (nome, numero, autocarros)
                VALUES (?, ?, ?)
            """, (nome, numero, autocarros_str))

        conn.commit()
        conn.close()

        flash(f"✅ Contact '{nome}' saved with buses: {autocarros_str}")
        return redirect(url_for('index'))

    return render_template("index.html")


@app.route('/admin/')
def admin():
    conn = sqlite3.connect('contactos.db')
    cursor = conn.cursor()

    # Garantir estrutura correta da tabela
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            nome TEXT,
            numero TEXT PRIMARY KEY,
            autocarros TEXT
        )
    """)

    cursor.execute("SELECT nome, numero, autocarros FROM contactos ORDER BY nome, numero")
    contactos = cursor.fetchall()
    conn.close()

    return render_template("admin.html", contactos=contactos)


if __name__ == "__main__":
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
