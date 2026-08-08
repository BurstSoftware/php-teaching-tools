try {
    throw new RuntimeException("Something failed.");
} catch (RuntimeException $error) {
    echo $error->getMessage();
}
