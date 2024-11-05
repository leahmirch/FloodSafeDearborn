<?php
$db_file = __DIR__ . '/user_db.sqlite';

try {
    $conn = new PDO("sqlite:" . $db_file);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $conn->exec("CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        image TEXT,
        self_introduction TEXT
    )");
} catch (PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}
?>