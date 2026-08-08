class User
{
    public function __construct(
        private string $name,
        private string $role
    ) {
    }

    public function getName(): string
    {
        return $this->name;
    }
}

$user = new User("Nathan", "admin");

echo $user->getName();
