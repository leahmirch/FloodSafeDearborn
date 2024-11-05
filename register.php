<?php
require 'db.php';

$message = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $email = $_POST['email'];
    $password = $_POST['password'];
    $selfIntroduction = $_POST['self_introduction'];
    $image = NULL;

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $message = "Invalid email format.";
    }
    elseif ($conn->query("SELECT COUNT(*) FROM users WHERE username = '$username'")->fetchColumn() > 0) {
        $message = "Username already taken. Please choose another.";
    }
    elseif ($conn->query("SELECT COUNT(*) FROM users WHERE email = '$email'")->fetchColumn() > 0) {
        $message = "Email already registered. Please use another.";
    }
    elseif (!preg_match('/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{10,}$/', $password)) {
        $message = "Password must be at least 10 characters long, containing at least one lowercase letter, one uppercase letter, and one number.";
    } else {
        $password = password_hash($password, PASSWORD_BCRYPT);

        if (isset($_FILES['image']) && $_FILES['image']['error'] == 0) {
            $targetDir = "uploads/";
            $imageName = basename($_FILES["image"]["name"]);
            $targetFilePath = $targetDir . $imageName;
            $fileType = strtolower(pathinfo($targetFilePath, PATHINFO_EXTENSION));

            $allowTypes = ['jpg', 'jpeg', 'png', 'gif'];

            if (in_array($fileType, $allowTypes)) {
                if (move_uploaded_file($_FILES["image"]["tmp_name"], $targetFilePath)) {
                    $image = $imageName;
                    $message = "Image uploaded successfully! ";
                } else {
                    $message = "Sorry, there was an error uploading your file.";
                }
            } else {
                $message = "Only JPG, JPEG, PNG, and GIF files are allowed.";
            }
        } else {
            $message .= " No image was uploaded.";
        }

        if ($message === '' || strpos($message, 'uploaded successfully') !== false) {
            $sql = "INSERT INTO users (username, email, password, image, self_introduction) VALUES (:username, :email, :password, :image, :self_introduction)";
            $stmt = $conn->prepare($sql);

            if ($stmt->execute([':username' => $username, ':email' => $email, ':password' => $password, ':image' => $image, ':self_introduction' => $selfIntroduction])) {
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
    <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
    <style>
        .form-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="email"], input[type="password"], input[type="file"] {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        #editor-container {
            height: 150px;
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .message {
            font-weight: bold;
            color: red;
        }
        button {
            padding: 10px 15px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
    <script src="https://cdn.quilljs.com/1.3.6/quill.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            var quill = new Quill('#editor-container', {
                theme: 'snow',
                placeholder: 'Write your self-introduction here...',
                modules: {
                    toolbar: [['bold', 'italic', 'underline'], ['link']]
                }
            });

            document.querySelector('form').addEventListener('submit', function () {
                var selfIntroduction = document.querySelector('input[name=self_introduction]');
                selfIntroduction.value = quill.root.innerHTML;
            });
        });
    </script>
</head>
<body>
    <div class="form-container">
        <h1>Register</h1>
        <p class="message"><?php echo $message; ?></p>
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" name="username" required>
            </div>

            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" name="email" required>
            </div>

            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" name="password" required>
            </div>

            <div class="form-group">
                <label for="image">Profile Image:</label>
                <input type="file" name="image" accept="image/jpeg, image/png, image/gif">
            </div>

            <div class="form-group">
                <label for="self_introduction">Self Introduction:</label>
                <div id="editor-container"></div>
                <input type="hidden" name="self_introduction">
            </div>

            <button type="submit">Register</button>
        </form>
        <p>Already registered? <a href="login.php">Login here</a>.</p>
    </div>
</body>
</html>