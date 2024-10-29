<?php
require 'db.php';
$message = '';
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $username = $_POST['username'];
        $email = $_POST['email'];
        $password = $_POST['password'];
        $image = NULL;
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $message = "Invalid email format.";
        }

        elseif ($conn->query("SELECT COUNT(*) FROM users WHERE username =
            '$username'")->fetchColumn() > 0) {
            $message = "Username already taken. Please choose another.";
        }

        elseif ($conn->query("SELECT COUNT(*) FROM users WHERE email =
            '$email'")->fetchColumn() > 0) {
            $message = "Email already registered. Please use another.";
        }

        elseif (!preg_match('/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{10,}$/',
            $password)) {
            $message = "Password must be at least 10 characters long, containing
            at least one lowercase letter, one uppercase letter, and one number. No
            special characters.";
        } else {
            $password = password_hash($password, PASSWORD_BCRYPT);
        
        if (isset($_FILES['image']) && $_FILES['image']['error'] == 0) {
            $targetDir = "uploads/";
            $imageName = basename($_FILES["image"]["name"]);
            $targetFilePath = $targetDir . $imageName;
            $fileType = strtolower(pathinfo($targetFilePath,
            PATHINFO_EXTENSION));
            $allowTypes = ['jpg', 'jpeg', 'png', 'gif'];
            
            if (in_array($fileType, $allowTypes)) {
            if (move_uploaded_file($_FILES["image"]["tmp_name"],
                $targetFilePath)) {
                $image = $imageName;
                $message = "Image uploaded successfully! ";
            } else {
                $message = "Sorry, there was an error uploading your
                file.";
            }
            } else {
                $message = "Only JPG, JPEG, PNG, and GIF files are allowed.";
            }
            } else {
                $message .= " No image was uploaded.";
            }
            if ($message === '' || strpos($message, 'uploaded successfully') !==
                false) {
                $sql = "INSERT INTO users (username, email, password, image)
                VALUES (:username, :email, :password, :image)";
                $stmt = $conn->prepare($sql);
            if ($stmt->execute([':username' => $username, ':email' => $email,
                ':password' => $password, ':image' => $image])) {
                $message .= " Successfully registered!";
            } else {
                $message .= " Registration failed. Please try again.";
            }
        }
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <title>Register</title>
    </head>
    <body>
        <h1>Register</h1>
        <p><?php echo $message; ?></p>
        <form method="POST" enctype="multipart/form-data">
        <label for="username">Username:</label>
        <input type="text" name="username" required>
        <label for="email">Email:</label>
        <input type="email" name="email" required>
        <label for="password">Password:</label>
        <input type="password" name="password" required>

        <label for="image">Profile Image:</label>
        <input type="file" name="image" accept="image/jpeg, image/png,
        image/gif">
        <p></p>
        <button type="submit">Register</button>
        </form>
        <p>Already registered? <a href="login.php">Login here</a>.</p>
    </body>
</html>