$statement = $pdo->prepare(
    "SELECT * FROM users WHERE email = :email"
);

$statement->execute([
    "email" => $email,
]);

$user = $statement->fetch();
