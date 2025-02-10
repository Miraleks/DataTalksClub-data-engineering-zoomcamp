Get-Content .\credentials.env | ForEach-Object {
    if ($_ -match "^(.+?)=(.+)$") {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}