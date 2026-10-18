$ErrorActionPreference = "Stop"

# Always build from the project directory, even when this script is launched
# using an absolute path.
Set-Location -LiteralPath $PSScriptRoot

$pyinstallerArgs = @(
    "-m", "PyInstaller",
    "--clean",
    "--noconfirm",
    "--windowed",
    "--onedir",
    "--name", "SavePassword",
    "--collect-all", "customtkinter",
    "main.py"
)

# An icon is optional. Add assets\save_password.ico when the project has a
# branded icon; the build remains usable before that asset exists.
$iconPath = Join-Path $PSScriptRoot "assets\save_password.ico"
if (Test-Path -LiteralPath $iconPath) {
    $pyinstallerArgs = @(
        "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "--windowed",
        "--onedir",
        "--name", "SavePassword",
        "--icon", $iconPath,
        "--collect-all", "customtkinter",
        "main.py"
    )
}

& python @pyinstallerArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Build complete: $PSScriptRoot\dist\SavePassword\SavePassword.exe"
Write-Host "Share the complete dist\SavePassword folder, not only the .exe file."
