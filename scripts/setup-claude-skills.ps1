$ErrorActionPreference = "Stop"

# This script lives in <project-root>\scripts\
$projectRoot = Split-Path -Parent $PSScriptRoot
$sharedSkills = Join-Path $projectRoot ".ai\skills"
$claudeDirectory = Join-Path $projectRoot ".claude"
$claudeSkills = Join-Path $claudeDirectory "skills"

New-Item -ItemType Directory -Force -Path $sharedSkills | Out-Null
New-Item -ItemType Directory -Force -Path $claudeDirectory | Out-Null

# Leave existing folders or links untouched.
$existing = Get-Item -LiteralPath $claudeSkills -Force -ErrorAction SilentlyContinue

if ($null -ne $existing) {
    if (
        $existing.LinkType -eq "Junction" -and
        $existing.Target -eq $sharedSkills
    ) {
        Write-Host "Skills junction is already configured."
        exit 0
    }

    throw "$claudeSkills already exists. Move any skills into $sharedSkills, then rename or remove the existing entry before running again."
}

New-Item -ItemType Junction `
    -Path $claudeSkills `
    -Target $sharedSkills | Out-Null

Write-Host "Linked $claudeSkills -> $sharedSkills"