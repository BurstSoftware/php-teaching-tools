session_start();

$_SESSION["user_id"] = 42;

echo $_SESSION["user_id"] ?? "Not logged in";
