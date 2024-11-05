<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}

$userId = $_SESSION['user_id'];
$sql = "SELECT username, image, self_introduction FROM users WHERE id = :id";
$stmt = $conn->prepare($sql);
$stmt->execute([':id' => $userId]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
    <style>
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        .profile-image {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        .self-introduction-box {
            border: 1px solid #ddd;
            padding: 15px;
            margin-top: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
            text-align: left;
        }
        .self-introduction-header {
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome, <?php echo htmlspecialchars($user['username']); ?>!</h1>
        
        <?php if ($user['image']): ?>
            <img src="uploads/<?php echo htmlspecialchars($user['image']); ?>" alt="Profile Image" class="profile-image">
        <?php else: ?>
            <p>No profile image uploaded.</p>
        <?php endif; ?>
        
        <div class="self-introduction-box">
            <div class="self-introduction-header">Self Introduction:</div>
            <div>
                <?php echo $user['self_introduction'] ? $user['self_introduction'] : "<p>No self-introduction provided.</p>"; ?>
            </div>
        </div>

        <br>
        <a href="profile.php">Edit Profile</a><br><br>
        <a href="logout.php">Logout</a>
    </div>
</body>
</html>