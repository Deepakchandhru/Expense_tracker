<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expense Tracker</title>
</head>
<body>
    <header>
        <h1>Expense Tracker</h1>
    </header>

    <?php
        $servername = 'localhost';
        $dbname = 'expenses';
        $username = 'postgres';
        $password = '5112';

        $conn = pg_connect("host=$servername dbname=$dbname user=$username password=$password");
        if (!$conn) {
            echo "Connection error.";
        }
    ?>

    <form method="post">
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

            <?php
                if (array_key_exists('add', $_POST)) {
                    $expense_name = $_POST['expense_name'];
                    $expense_category = $_POST['expense_category'];
                    $date = $_POST['date'];
                    $amount = $_POST['amount'];
                    $sql = "INSERT INTO expense(name, category, date, amount) VALUES('$expense_name', '$expense_category', '$date', '$amount');";
                    $result = pg_query($conn, $sql);
                    if ($result) {
                        echo "<p>Expense added successfully</p>";
                    } else {
                        echo "<p>Error adding expense</p>";
                    }
                }
            ?>
        </fieldset>
    </form>

    <form method="post">
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
            <input type="number" step="1" name="new_amount" id="new_amount"><br>
            
            <button id="edit" name="edit">Edit Expense</button>

            <?php
                if (array_key_exists('edit', $_POST)) {
                    $expense_edit = $_POST['expense_edit'];
                    $updates = [];
                    if (!empty($_POST['new_name'])) {
                        $new_name = $_POST['new_name'];
                        $updates[] = "name = '$new_name'";
                    }
                    if (!empty($_POST['new_category'])) {
                        $new_category = $_POST['new_category'];
                        $updates[] = "category = '$new_category'";
                    }
                    if (!empty($_POST['new_date'])) {
                        $new_date = $_POST['new_date'];
                        $updates[] = "date = '$new_date'";
                    }
                    if (!empty($_POST['new_amount'])) {
                        $new_amount = $_POST['new_amount'];
                        $updates[] = "amount = '$new_amount'";
                    }
                    if (!empty($updates)) {
                        $sql = "UPDATE expense SET " . implode(", ", $updates) . " WHERE name = '$expense_edit';";
                        $result = pg_query($conn, $sql);
                        if ($result) {
                            echo "<p>Expense edited successfully</p>";
                        } else {
                            echo "<p>Error editing expense</p>";
                        }
                    }
                }
            ?>
        </fieldset>
    </form>

    <form method="post">
        <fieldset class="delete">
            <legend>Delete Expense</legend>
            <label for="expense_del">Expense Name:</label>
            <input type="text" name="expense_del" id="expense_del" required><br>

            <button id="delete" name="delete">Delete Expense</button>

            <?php
                if (array_key_exists('delete', $_POST)) {
                    $expense_del = $_POST['expense_del'];
                    $sql = "DELETE FROM expense WHERE name = '$expense_del';";
                    $result = pg_query($conn, $sql);
                    if ($result) {
                        echo "<p>Expense deleted successfully</p>";
                    } else {
                        echo "<p>Error deleting expense</p>";
                    }
                }
            ?>
        </fieldset>
    </form>

    <form method="post">
        <fieldset class="view">
            <legend>View Expenses</legend>
            <button id="view" name="view">View all Expenses</button>

            <?php
                if (array_key_exists('view', $_POST)) {
                    $sql = "SELECT * FROM expense;";
                    $result = pg_query($conn, $sql);
                    if ($result) {
                        echo "<ul>";
                        while ($row = pg_fetch_assoc($result)) {
                            echo "<li>" . $row['name'] . " - " . $row['category'] . " - " . $row['date'] . " - $" . $row['amount'] . "</li>";
                        }
                        echo "</ul>";
                    } else {
                        echo "<p>Error fetching expenses</p>";
                    }
                }
            ?>
        </fieldset>
    </form>

    <form method="post">
        <fieldset class="categoryview">
            <legend>View Expenses by Category</legend>
            <label for="category">Category:</label>
            <input type="text" name="category" id="category" required><br>

            <button id="categoryview" name="categoryview">View Expenses</button>

            <?php
                if (array_key_exists('categoryview', $_POST)) {
                    $category = $_POST['category'];
                    $sql = "SELECT * FROM expense WHERE category = '$category';";
                    $result = pg_query($conn, $sql);
                    if ($result) {
                        echo "<ul>";
                        while ($row = pg_fetch_assoc($result)) {
                            echo "<li>" . $row['name'] . " - " . $row['date'] . " - $" . $row['amount'] . "</li>";
                        }
                        echo "</ul>";
                    } else {
                        echo "<p>Error fetching expenses</p>";
                    }
                }
            ?>
        </fieldset>
    </form>
        
    <form method="post">
        <fieldset class="dateview">
            <legend>View Expenses by Date</legend>
            <label for="from_date">From:</label>
            <input type="date" name="from_date" id="from_date" required><br>
            <label for="to_date">To:</label>
            <input type="date" name="to_date" id="to_date" required><br> 

            <button id="dateview" name="dateview">View Expenses</button>

            <?php
                if (array_key_exists('dateview', $_POST)) {
                    $from_date = $_POST['from_date'];
                    $to_date = $_POST['to_date'];
                    $sql = "SELECT * FROM expense WHERE date BETWEEN '$from_date' AND '$to_date';";
                    $result = pg_query($conn, $sql);
                    if ($result) {
                        echo "<ul>";
                        while ($row = pg_fetch_assoc($result)) {
                            echo "<li>" . $row['name'] . " - " . $row['category'] . " - $" . $row['amount'] . "</li>";
                        }
                        echo "</ul>";
                    } else {
                        echo "<p>Error fetching expenses</p>";
                    }
                }
            ?>
        </fieldset>
    </form>

    <footer style="color: white; background-color: black;">
        <p>courtesy: CSAU</p>
    </footer>
</body>
</html>
