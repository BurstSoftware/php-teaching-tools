A clean PHP + Node.js project uses:

PHP for routing, forms, sessions, database access, and server-rendered HTML.
Composer for PHP dependencies.
Node.js/npm for JavaScript, CSS, and frontend build tools.
A public/ directory as the only web-accessible folder.
1. Install the required software

Install:

PHP
Composer
A currently supported Node.js LTS release
Git
A database such as MySQL, MariaDB, PostgreSQL, or SQLite

Verify the installations:

php --version
composer --version
node --version
npm --version
git --version

Use a supported LTS Node.js version rather than an end-of-life release. Node.js downloads

2. Create the project
mkdir php-node-project
cd php-node-project

git init
composer init
npm init -y

When composer init asks questions, you can accept the defaults for now.

3. Create the directory structure
php-node-project/
├── public/
│   ├── assets/
│   └── index.php
├── src/
│   └── functions.php
├── resources/
│   ├── css/
│   │   └── app.css
│   └── js/
│       └── app.js
├── storage/
│   └── logs/
├── tests/
├── vendor/
├── node_modules/
├── .env
├── .env.example
├── .gitignore
├── composer.json
└── package.json

The important security rule is that public/ should eventually become the web server’s document root. Application code, credentials, logs, and Composer files stay outside it.

4. Configure Composer autoloading

Modify composer.json:

{
    "name": "nathan/php-node-project",
    "description": "PHP application with Node.js frontend tooling",
    "type": "project",
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "require": {}
}

Regenerate the autoloader:

composer dump-autoload

Composer’s autoloader lets PHP load classes from src/ without manually requiring every class. See the official Composer introduction.

5. Create the PHP entry point

Create public/index.php:

<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/vendor/autoload.php';

$pageTitle = 'PHP + Node.js Project';
$message = 'Your development environment is working.';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title><?= htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8') ?></title>

    <link rel="stylesheet" href="/assets/app.css">
    <script type="module" src="/assets/app.js" defer></script>
</head>
<body>
    <main>
        <h1><?= htmlspecialchars($pageTitle, ENT_QUOTES, 'UTF-8') ?></h1>
        <p><?= htmlspecialchars($message, ENT_QUOTES, 'UTF-8') ?></p>

        <button id="test-button" type="button">
            Test JavaScript
        </button>
    </main>
</body>
</html>
6. Add frontend source files

Create resources/js/app.js:

const button = document.querySelector("#test-button");

button?.addEventListener("click", () => {
    alert("PHP and Node.js are working together!");
});

Create resources/css/app.css:

:root {
    font-family: system-ui, sans-serif;
    color: #1f2937;
    background: #f8fafc;
}

body {
    margin: 0;
}

main {
    width: min(90%, 60rem);
    margin: 4rem auto;
}

button {
    padding: 0.75rem 1rem;
    color: white;
    background: #2563eb;
    border: 0;
    border-radius: 0.375rem;
    cursor: pointer;
}
7. Install the frontend build tool

A simple choice is esbuild:

npm install --save-dev esbuild

Update the scripts section of package.json:

{
    "scripts": {
        "build:js": "esbuild resources/js/app.js --bundle --minify --outfile=public/assets/app.js",
        "build:css": "esbuild resources/css/app.css --bundle --minify --outfile=public/assets/app.css",
        "build": "npm run build:js && npm run build:css",
        "watch:js": "esbuild resources/js/app.js --bundle --sourcemap --outfile=public/assets/app.js --watch",
        "watch:css": "esbuild resources/css/app.css --bundle --sourcemap --outfile=public/assets/app.css --watch"
    }
}

Build the assets:

npm run build

Alternatively, Vite provides a more complete frontend development server and production build system. Its current setup requirements are documented in the official Vite guide.

8. Start PHP

Run:

php -S localhost:8000 -t public

Open:

http://localhost:8000

PHP’s built-in server is intended only for development and should not be exposed as a production server. PHP built-in server documentation

While developing, use separate terminals:

# Terminal 1
php -S localhost:8000 -t public
# Terminal 2
npm run watch:js
# Terminal 3
npm run watch:css
9. Configure environment variables

Create .env.example:

APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000

DB_DRIVER=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=php_node_app
DB_USER=app_user
DB_PASSWORD=

Copy it locally:

cp .env.example .env

Install a PHP environment-variable package:

composer require vlucas/phpdotenv

Load it near the beginning of public/index.php:

$dotenv = Dotenv\Dotenv::createImmutable(dirname(__DIR__));
$dotenv->safeLoad();

Never place passwords, API keys, or production credentials in JavaScript. Frontend code is visible to visitors.

10. Add .gitignore
/vendor/
/node_modules/
/public/assets/
.env
*.log
.DS_Store

Keep .env.example committed, but exclude the real .env.

11. Add a database when needed

For a small application, SQLite is the easiest starting point:

$database = new PDO(
    'sqlite:' . dirname(__DIR__) . '/storage/database.sqlite',
    null,
    null,
    [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]
);

For MySQL or PostgreSQL, use a restricted application database account and prepared statements.

12. Production setup

For deployment:

Run composer install --no-dev --optimize-autoloader.
Run npm ci.
Run npm run build.
Configure Nginx or Apache with public/ as the document root.
Use PHP-FPM to execute PHP.
Disable PHP error display and write errors to logs.
configure HTTPS.
Store production secrets in server environment variables.
Give the web server write access only to directories that require it.

Node.js generally does not need to run in production when it is only compiling frontend assets. The compiled files inside public/assets/ are served by Nginx or Apache.
