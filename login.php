<?php
require 'db.php';
session_start();
    if (isset($_SESSION['user_id'])) {
        header("Location: home.php");
        exit();
    }

    $message = '';

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $username = $_POST['username'];
        $password = $_POST['password'];
        $sql = "SELECT * FROM users WHERE username = :username";
        $stmt = $conn->prepare($sql);
        $stmt->execute([':username' => $username]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            header("Location: home.php");
            exit();
        } else {
            $message = "Invalid username or password.";
        }
    }
?>
<!DOCTYPE html>
<html>
    <head>
    <title>Login</title>
    </head>
    
    <body>
    <h1>Login</h1>
    <p><?php echo $message; ?></p>
    <form method="POST">
    <label for="username">Username:</label>
    <input type="text" name="username" required>

    <label for="password">Password:</label>
    <input type="password" name="password" required>
    <p></p>
    <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="register.php">Register here</a>.</p>
    </body>
</html>