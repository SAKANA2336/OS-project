#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("work", "release")]
    [string]$Role
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Read-Git([string[]]$GitArgs) {
    $result = @(& git @GitArgs)
    if ($LASTEXITCODE -ne 0) {
        throw "Git check failed: $($GitArgs -join ' ')"
    }
    return ($result -join "`n").Trim()
}

function Resolve-GitDirectory([string]$Value, [string]$Root) {
    if (-not [IO.Path]::IsPathRooted($Value)) {
        $Value = Join-Path $Root $Value
    }
    return (Resolve-Path -LiteralPath $Value).ProviderPath.TrimEnd("\", "/")
}

$root = Resolve-GitDirectory (Read-Git @("rev-parse", "--show-toplevel")) (Get-Location).Path
$metadata = Join-Path $root ".git"
if (-not (Test-Path -LiteralPath $metadata -PathType Container)) {
    throw "An independent .git directory is required."
}
if ((Get-Item -LiteralPath $metadata -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
    throw "The .git directory must not be a link."
}
foreach ($option in @("--git-dir", "--git-common-dir")) {
    if ((Resolve-GitDirectory (Read-Git @("rev-parse", $option)) $root) -ne $metadata) {
        throw "Git metadata is shared or outside the repository."
    }
}
$null = Read-Git @(
    "merge-base", "--is-ancestor", "62b2d649e2c4ffdb91eeb7bf4c2932be5a9023ba", "HEAD"
)
$marker = (Get-Content -LiteralPath (Join-Path $root ".local/workspace-role") -Raw).Trim()
if ($marker -cne $Role) {
    throw "The workspace marker does not match the requested role."
}
$remotes = Read-Git @("remote")
$directoryName = Split-Path -Leaf $root
if ($Role -eq "work") {
    if ($directoryName -cne "OS-project-local" -or $remotes) {
        throw "Daily work requires OS-project-local with no remotes."
    }
} else {
    if ($directoryName -cne "OS-project" -or $remotes -cne "origin") {
        throw "Release work requires OS-project with only origin."
    }
    $expected = "https://github.com/SAKANA2336/OS-project.git"
    foreach ($arguments in @(
        @("remote", "get-url", "--all", "origin"),
        @("remote", "get-url", "--push", "--all", "origin")
    )) {
        if ((Read-Git $arguments) -cne $expected) {
            throw "Unexpected origin URL."
        }
    }
    if ((Read-Git @("branch", "--show-current")) -cne "main" -or
        (Read-Git @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")) -cne "origin/main") {
        throw "Release main must track origin/main."
    }
}
Write-Host "workspace-zone check passed"
Write-Host "role: $Role"
Write-Host "root: $root"
