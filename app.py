from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = 'db/paise.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    conn = get_db()
    groups = conn.execute(
        'SELECT g.* FROM groups g JOIN group_members gm ON g.id = gm.group_id WHERE gm.user_id = ?',
        (user_id,)
    ).fetchall()
    return render_template('dashboard.html', user_id=user_id, groups=groups)

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        cycle = request.form['cycle']
        user_id = int(request.form['user_id'])

        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO groups (name, contribution_amount, cycle_duration) VALUES (?, ?, ?)',
                    (name, amount, cycle))
        group_id = cur.lastrowid
        cur.execute('INSERT INTO group_members (group_id, user_id) VALUES (?, ?)', (group_id, user_id))
        conn.commit()
        return redirect(url_for('dashboard', user_id=user_id))
    return render_template('create_group.html')

@app.route('/group/<int:group_id>/<int:user_id>', methods=['GET', 'POST'])
def group_page(group_id, user_id):
    conn = get_db()
    group = conn.execute('SELECT * FROM groups WHERE id = ?', (group_id,)).fetchone()

    if request.method == 'POST':
        amount = request.form['amount']
        conn.execute('INSERT INTO contributions (user_id, group_id, amount, date) VALUES (?, ?, ?, ?)',
                     (user_id, group_id, amount, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()

    contributions = conn.execute(
        'SELECT * FROM contributions WHERE group_id = ? AND user_id = ?',
        (group_id, user_id)
    ).fetchall()

    return render_template('group_page.html', group=group, user_id=user_id, contributions=contributions)

@app.route('/history/<int:user_id>')
def history(user_id):
    conn = get_db()
    transactions = conn.execute(
        'SELECT * FROM contributions WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    return render_template('transaction_history.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
