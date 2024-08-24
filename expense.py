from flask import Flask, request, render_template_string,url_for
import psycopg2

app = Flask(__name__)

# Database connection parameters
DB_PARAMS = {
    'dbname': 'expense',  # Updated DB name
    'user': 'postgres',
    'password': '5112',
    'host': 'localhost'
}

# HTML templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet"  href="{{ url_for('static', filename='expense.css') }}">
    <title>Expense Tracker</title>
</head>
<body>
    <header>
        <h1>Expense Tracker</h1>
    </header>

    <form method="post" action="/add">
        <fieldset class="add">
            <legend>Add Expense</legend>
            <label for="expense_name">Expense Name:</label>
            <input type="text" name="expense_name" id="expense_name" required><br>
            
            <label for="expense_category">Category:</label>
            <input type="text" name="expense_category" id="expense_category" required><br>

            <label for="date">Date:</label>
            <input type="date" name="date" id="date" required><br> 
            
            <label for="amount">Amount:</label>
            <input type="number" step="0.01" name="amount" id="amount" required><br>
            
            <button id="add" name="add">Add Expense</button>
            {% if add_message %}
                <p>{{ add_message }}</p>
            {% endif %}
        </fieldset>
    </form>

    <form method="post" action="/edit">
        <fieldset class="edit">
            <legend>Edit Expense</legend>
            <label for="expense_edit">Expense Name:</label>
            <input type="text" name="expense_edit" id="expense_edit" required><br>
            <label for="new_name">New Name:</label>
            <input type="text" name="new_name" id="new_name"><br>
            <label for="new_category">New category:</label>
            <input type="text" name="new_category" id="new_category"><br>
            <label for="new_date">New date:</label>
            <input type="date" name="new_date" id="new_date"><br>
            <label for="new_amount">New Amount:</label>
            <input type="number" step="0.01" name="new_amount" id="new_amount"><br>
            
            <button id="edit" name="edit">Edit Expense</button>
            {% if edit_message %}
                <p>{{ edit_message }}</p>
            {% endif %}
        </fieldset>
    </form>

    <form method="post" action="/delete">
        <fieldset class="delete">
            <legend>Delete Expense</legend>
            <label for="expense_del">Expense Name:</label>
            <input type="text" name="expense_del" id="expense_del" required><br>
            
            <button id="delete" name="delete">Delete Expense</button>
            {% if delete_message %}
                <p>{{ delete_message }}</p>
            {% endif %}
        </fieldset>
    </form>

    <form method="post" action="/view">
        <fieldset class="view">
            <legend>View Expenses</legend>
            <button id="view" name="view">View all Expenses</button>
            {% if expenses %}
                <ul>
                    {% for expense in expenses %}
                        <li>{{ expense.name }} - {{ expense.category }} - {{ expense.date }} - ${{ expense.amount }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </fieldset>
    </form>

    <form method="post" action="/categoryview">
        <fieldset class="categoryview">
            <legend>View Expenses by Category</legend>
            <label for="category">Category:</label>
            <input type="text" name="category" id="category" required><br>
            
            <button id="categoryview" name="categoryview">View Expenses</button>
            {% if category_expenses %}
                <ul>
                    {% for expense in category_expenses %}
                        <li>{{ expense.name }} - {{ expense.date }} - ${{ expense.amount }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </fieldset>
    </form>
    
    <form method="post" action="/dateview">
        <fieldset class="dateview">
            <legend>View Expenses by Date</legend>
            <label for="from_date">From:</label>
            <input type="date" name="from_date" id="from_date" required><br>
            <label for="to_date">To:</label>
            <input type="date" name="to_date" id="to_date" required><br>
            
            <button id="dateview" name="dateview">View Expenses</button>
            {% if date_expenses %}
                <ul>
                    {% for expense in date_expenses %}
                        <li>{{ expense.name }} - {{ expense.category }} - ${{ expense.amount }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </fieldset>
    </form>
    
    <footer style="color: white; background-color: black;">
        <p>courtesy: CSAU</p>
    </footer>
</body>
</html>
"""

# Helper function to get database connection
def get_db_connection():
    conn = psycopg2.connect(**DB_PARAMS)
    return conn

# Route to handle adding expense
@app.route('/add', methods=['POST'])
def add_expense():
    expense_name = request.form['expense_name']
    expense_category = request.form['expense_category']
    date = request.form['date']
    amount = request.form['amount']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO expense (name, category, date, amount) VALUES (%s, %s, %s, %s)',
                (expense_name, expense_category, date, amount))
    conn.commit()
    cur.close()
    conn.close()

    return render_template_string(HTML_TEMPLATE, add_message="Expense added successfully")

# Route to handle editing expense
@app.route('/edit', methods=['POST'])
def edit_expense():
    expense_edit = request.form['expense_edit']
    updates = []
    if request.form.get('new_name'):
        new_name = request.form['new_name']
        updates.append(f"name = '{new_name}'")
    if request.form.get('new_category'):
        new_category = request.form['new_category']
        updates.append(f"category = '{new_category}'")
    if request.form.get('new_date'):
        new_date = request.form['new_date']
        updates.append(f"date = '{new_date}'")
    if request.form.get('new_amount'):
        new_amount = request.form['new_amount']
        updates.append(f"amount = {new_amount}")

    if updates:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE expense SET {', '.join(updates)} WHERE name = %s", (expense_edit,))
        conn.commit()
        cur.close()
        conn.close()
        return render_template_string(HTML_TEMPLATE, edit_message="Expense edited successfully")
    
    return render_template_string(HTML_TEMPLATE, edit_message="No updates provided")

# Route to handle deleting expense
@app.route('/delete', methods=['POST'])
def delete_expense():
    expense_del = request.form['expense_del']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM expense WHERE name = %s', (expense_del,))
    conn.commit()
    cur.close()
    conn.close()

    return render_template_string(HTML_TEMPLATE, delete_message="Expense deleted successfully")

# Route to handle viewing all expenses
@app.route('/view', methods=['POST'])
def view_expenses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM expense')
    expenses = cur.fetchall()
    cur.close()
    conn.close()

    expense_list = [{'name': row[1], 'category': row[2], 'date': row[4], 'amount': row[3]} for row in expenses]
    return render_template_string(HTML_TEMPLATE, expenses=expense_list)

# Route to handle viewing expenses by category
@app.route('/categoryview', methods=['POST'])
def view_expenses_by_category():
    category = request.form['category']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM expense WHERE category = %s', (category,))
    expenses = cur.fetchall()
    cur.close()
    conn.close()

    category_expense_list = [{'name': row[1], 'date': row[4], 'amount': row[3]} for row in expenses]
    return render_template_string(HTML_TEMPLATE, category_expenses=category_expense_list)

# Route to handle viewing expenses by date range
@app.route('/dateview', methods=['POST'])
def view_expenses_by_date():
    from_date = request.form['from_date']
    to_date = request.form['to_date']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM expense WHERE date BETWEEN %s AND %s', (from_date, to_date))
    expenses = cur.fetchall()
    cur.close()
    conn.close()

    date_expense_list = [{'name': row[1], 'category': row[2], 'amount': row[3]} for row in expenses]
    return render_template_string(HTML_TEMPLATE, date_expenses=date_expense_list)

# Route to display the main page
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
