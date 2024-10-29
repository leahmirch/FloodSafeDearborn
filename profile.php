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

        if (preg_match('/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{10,}$/',
            $new_password)) {
            $hashed_password = password_hash($new_password, PASSWORD_BCRYPT);
            $updatePassword = $conn->prepare("UPDATE users SET password =
            :password WHERE id = :id");
            $updatePassword->execute([':password' => $hashed_password, ':id'
            => $userId]);
            $message = "Password updated successfully! ";
        } else {
            $message = "Password must be at least 10 characters long,
            containing at least one lowercase letter, one uppercase letter, and one
            number.";
        }
    }
 
    if (isset($_FILES['new_image']) && $_FILES['new_image']['error'] == 0) {
        $targetDir = "uploads/";
        $imageName = basename($_FILES["new_image"]["name"]);
        $targetFilePath = $targetDir . $imageName;
        $fileType = strtolower(pathinfo($targetFilePath,
        PATHINFO_EXTENSION));
        $allowTypes = ['jpg', 'jpeg', 'png', 'gif'];
        
        if (in_array($fileType, $allowTypes)) {
            if (move_uploaded_file($_FILES["new_image"]["tmp_name"],
                $targetFilePath)) {
                $updateImage = $conn->prepare("UPDATE users SET image =
                :image WHERE id = :id");
                $updateImage->execute([':image' => $imageName, ':id' =>
                $userId]);
                $message .= "Image updated successfully!";

            } else {
                $message = "Sorry, there was an error uploading your file.";
            }
        } else {
            $message = "Only JPG, JPEG, PNG, and GIF files are allowed.";
        }
    }
}

?>
<!DOCTYPE html>
<html>
    <head>
        <title>Update Profile</title>
    </head>
    <body>
        <h1>Update Profile</h1>
        <p><?php echo $message; ?></p>
        <?php if ($user['image']): ?>
        <img src="uploads/<?php echo htmlspecialchars($user['image']); ?>"
        alt="Profile Image" style="width: 150px; height: auto;">
        <?php else: ?>
        <p>No profile image uploaded.</p>
        <?php endif; ?>
        <form method="POST" enctype="multipart/form-data">
        <label for="new_password">New Password:</label>
        <input type="password" name="new_password" placeholder="Enter new
        password">

        <label for="new_image">New Profile Image:</label>
        <input type="file" name="new_image" accept="image/jpeg, image/png,
        image/gif">
        <p></p>
        <button type="submit">Update Profile</button>
        </form>
        <br>
        <a href="home.php">Return</a>
    </body>
</html>
