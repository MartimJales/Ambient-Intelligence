from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Contactos WhatsApp</title>
<h2>Adicionar novo contacto</h2>
<form method="post">
  Nome: <input type="text" name="nome" required><br><br>
  Número de telefone: <input type="text" name="numero" required><br><br>
  <input type="submit" value="Adicionar">
</form>

{% if mensagem %}
  <p><strong>{{ mensagem }}</strong></p>
{% endif %}

<hr>
<h3>Contactos atuais:</h3>
<ul>
  {% for nome, numero in contactos %}
    <li>{{ nome }} - {{ numero }}</li>
  {% endfor %}
</ul>
"""

def obter_contactos():
    conn = sqlite3.connect('contactos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, numero FROM contactos")
    contactos = cursor.fetchall()
    conn.close()
    return contactos

@app.route('/', methods=['GET', 'POST'])
def index():
    mensagem = ''
    if request.method == 'POST':
        nome = request.form['nome']
        numero = request.form['numero']
        conn = sqlite3.connect('contactos.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contactos (nome, numero) VALUES (?, ?)", (nome, numero))
        conn.commit()
        conn.close()
        mensagem = f"✅ Contacto '{nome}' adicionado com sucesso!"
    contactos = obter_contactos()
    return render_template_string(HTML, mensagem=mensagem, contactos=contactos)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
