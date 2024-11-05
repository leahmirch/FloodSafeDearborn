<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}

$userId = $_SESSION['user_id'];
$message = '';

$sql = "SELECT * FROM users WHERE id = :id";
$stmt = $conn->prepare($sql);
$stmt->execute([':id' => $userId]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (!empty($_POST['new_password'])) {
        $new_password = $_POST['new_password'];
        
        if (preg_match('/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{10,}$/', $new_password)) {
            $hashed_password = password_hash($new_password, PASSWORD_BCRYPT);

            $updatePassword = $conn->prepare("UPDATE users SET password = :password WHERE id = :id");
            $updatePassword->execute([':password' => $hashed_password, ':id' => $userId]);
            $message = "Password updated successfully! ";
        } else {
            $message = "Password must be at least 10 characters long, containing at least one lowercase letter, one uppercase letter, and one number.";
        }
    }

    if (isset($_FILES['new_image']) && $_FILES['new_image']['error'] == 0) {
        $targetDir = "uploads/";
        $imageName = basename($_FILES["new_image"]["name"]);
        $targetFilePath = $targetDir . $imageName;
        $fileType = strtolower(pathinfo($targetFilePath, PATHINFO_EXTENSION));

        $allowTypes = ['jpg', 'jpeg', 'png', 'gif'];
        if (in_array($fileType, $allowTypes)) {
            if (move_uploaded_file($_FILES["new_image"]["tmp_name"], $targetFilePath)) {
                $updateImage = $conn->prepare("UPDATE users SET image = :image WHERE id = :id");
                $updateImage->execute([':image' => $imageName, ':id' => $userId]);
                $message .= "Image updated successfully!";
            } else {
                $message = "Sorry, there was an error uploading your file.";
            }
        } else {
            $message = "Only JPG, JPEG, PNG, and GIF files are allowed.";
        }
    }

    if (!empty($_POST['self_introduction'])) {
        $selfIntroduction = $_POST['self_introduction'];
        $updateIntro = $conn->prepare("UPDATE users SET self_introduction = :self_introduction WHERE id = :id");
        $updateIntro->execute([':self_introduction' => $selfIntroduction, ':id' => $userId]);
        $message .= " Self-introduction updated successfully!";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Update Profile</title>
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
        input[type="text"], input[type="password"], input[type="file"] {
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
                placeholder: 'Edit your self-introduction here...',
                modules: {
                    toolbar: [['bold', 'italic', 'underline'], ['link']]
                }
            });

            // Load the existing self-introduction
            quill.root.innerHTML = <?php echo json_encode($user['self_introduction']); ?>;

            document.querySelector('form').addEventListener('submit', function () {
                var selfIntroduction = document.querySelector('input[name=self_introduction]');
                selfIntroduction.value = quill.root.innerHTML;
            });
        });
    </script>
</head>
<body>
    <div class="form-container">
        <h1>Update Profile</h1>
        <p class="message"><?php echo $message; ?></p>

        <?php if ($user['image']): ?>
            <img src="uploads/<?php echo htmlspecialchars($user['image']); ?>" alt="Profile Image" style="width: 150px; height: auto; margin-bottom: 15px;">
        <?php else: ?>
            <p>No profile image uploaded.</p>
        <?php endif; ?>

        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="new_password">New Password:</label>
                <input type="password" name="new_password" placeholder="Enter new password">
            </div>

            <div class="form-group">
                <label for="new_image">New Profile Image:</label>
                <input type="file" name="new_image" accept="image/jpeg, image/png, image/gif">
            </div>

            <div class="form-group">
                <label for="self_introduction">Self Introduction:</label>
                <div id="editor-container"></div>
                <input type="hidden" name="self_introduction">
            </div>

            <button type="submit">Update Profile</button>
        </form>
        <br>
        <a href="home.php">Return to Home</a>
    </div>
</body>
</html>