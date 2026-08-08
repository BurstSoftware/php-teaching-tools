$name = $_POST["name"] ?? "";
$page = $_GET["page"] ?? "home";

$name = trim($_POST["name"] ?? "");

if ($name === "") {
    echo "A name is required.";
}
