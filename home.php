<?php
session_start();
require 'db.php';
    if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
    }

    $userId = $_SESSION['user_id'];
    $sql = "SELECT username, image FROM users WHERE id = :id";
    $stmt = $conn->prepare($sql);
    $stmt->execute([':id' => $userId]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html>
    <head>
    <title>Home</title>
        <style>
            .profile-image {
            max-width: 50%;
            height: auto;
            display: block;
            margin: 0;
            }
        </style>
    </head>
    <body>
        <h1>Welcome, <?php echo htmlspecialchars($user['username']); ?>!</h1>

        <?php if ($user['image']): ?>
        <img src="uploads/<?php echo htmlspecialchars($user['image']); ?>"
        alt="Profile Image" class="profile-image">
        <?php else: ?>
        <p>No profile image uploaded.</p>
        <?php endif; ?>
        <br>
        <a href="profile.php">Edit Profile</a><br><br>
        <a href="logout.php">Logout</a>
    </body>
</html>