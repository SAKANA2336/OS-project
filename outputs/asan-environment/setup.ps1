#Requires -Version 5.1
[CmdletBinding()]
param(
    [string]$WorkRoot = "",
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$utf8 = [System.Text.UTF8Encoding]::new($false)
if (-not $WorkRoot) {
    $WorkRoot = Join-Path $PSScriptRoot "../../work/asan-environment"
}
$WorkRoot = [System.IO.Path]::GetFullPath($WorkRoot)
if ($WorkRoot.Contains(",")) {
    throw "WorkRoot must not contain a comma (Docker --mount separator)."
}
$runId = "env-" + [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ").ToLowerInvariant() +
    "-" + [Guid]::NewGuid().ToString("N").Substring(0, 8)
$runRoot = Join-Path $WorkRoot $runId
$null = New-Item -ItemType Directory -Path $runRoot
$docker = (Get-Command docker.exe -ErrorAction Stop).Source
$containerName = "os-project-asan-" + $runId
$manifest = [ordered]@{
    run_id = $runId
    kind = "environment-functional-validation"
    status = "started"
    started_at = [DateTime]::UtcNow.ToString("o")
    context = "desktop-linux"
    paper_claims_tested = @()
    base_digest = $null
    image_id = $null
    image_tag = $null
    checks_passed = 0
    kit_sha256 = @{}
    smoke_limits = @{ cpus = 2; memory_bytes = 2147483648; pids = 128; timeout_seconds = 300 }
}
$containerAttempted = $false

function ConvertTo-NativeArgument([string]$Value) {
    # Windows CommandLineToArgvW-compatible quoting for PowerShell 5.1.
    $escaped = [regex]::Replace($Value, '(\\*)"', '$1$1\"')
    $escaped = [regex]::Replace($escaped, '(\\+)$', '$1$1')
    return '"' + $escaped + '"'
}

function Invoke-Docker([string]$Label, [string[]]$DockerArgs, [int]$TimeoutSeconds = 30) {
    $allArgs = @("--context", "desktop-linux") + $DockerArgs
    $commandRecord = @{ argv = $allArgs; timeout_seconds = $TimeoutSeconds }
    [IO.File]::WriteAllText(
        (Join-Path $runRoot "$Label.command.json"),
        ($commandRecord | ConvertTo-Json -Depth 6), $utf8
    )
    Write-Host "[$Label] Running Docker..."
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $docker
    $start.Arguments = (($allArgs | ForEach-Object { ConvertTo-NativeArgument $_ }) -join " ")
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        $null = $process.Start()
        $outTask = $process.StandardOutput.ReadToEndAsync()
        $errTask = $process.StandardError.ReadToEndAsync()
        $ended = $process.WaitForExit($TimeoutSeconds * 1000)
        if (-not $ended) {
            $process.Kill()
            $null = $process.WaitForExit(5000)
        }
        $null = $outTask.Wait(5000)
        $null = $errTask.Wait(5000)
        $stdout = if ($outTask.IsCompleted) { $outTask.Result } else { "[stdout incomplete]" }
        $stderr = if ($errTask.IsCompleted) { $errTask.Result } else { "[stderr incomplete]" }
        [IO.File]::WriteAllText((Join-Path $runRoot "$Label.stdout.log"), $stdout, $utf8)
        [IO.File]::WriteAllText((Join-Path $runRoot "$Label.stderr.log"), $stderr, $utf8)
        if (-not $ended) {
            throw "$Label exceeded $TimeoutSeconds seconds. Logs are in $runRoot."
        }
        if ($process.ExitCode -ne 0) {
            throw "$Label failed (exit $($process.ExitCode)): $stderr"
        }
        return $stdout.Trim()
    } finally {
        $process.Dispose()
    }
}

try {
    foreach ($name in @("Dockerfile", ".dockerignore", "cases.c", "normal.cpp", "verify.py", "setup.ps1")) {
        $manifest.kit_sha256[$name] = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $name) -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    $endpoint = Invoke-Docker "endpoint" @(
        "context", "inspect", "desktop-linux", "--format", "{{.Endpoints.docker.Host}}"
    )
    if ($endpoint -ne "npipe:////./pipe/dockerDesktopLinuxEngine") {
        throw "Expected the local Docker Desktop named pipe; refusing any alternative endpoint."
    }
    $infoFormat = '{"version":{{json .ServerVersion}},"os":{{json .OSType}},"arch":{{json .Architecture}},"kernel":{{json .KernelVersion}},"cpus":{{.NCPU}},"memory":{{.MemTotal}},"memory_limit":{{.MemoryLimit}},"pids_limit":{{.PidsLimit}}}'
    $info = (Invoke-Docker "engine" @("info", "--format", $infoFormat)) | ConvertFrom-Json
    if ($info.os -ne "linux" -or $info.arch -notin @("x86_64", "amd64")) {
        throw "A native Linux x86_64 Docker engine is required."
    }
    if (-not $info.memory_limit -or -not $info.pids_limit) {
        throw "The engine must support memory and PID limits."
    }
    if ($info.cpus -lt 2 -or $info.memory -lt 3GB) {
        throw "Docker needs at least 2 CPUs and 3 GiB RAM for this setup."
    }
    if ($CheckOnly) {
        $manifest.status = "preflight_passed"
        Write-Host "Preflight passed. No image was downloaded or built."
    } else {
        $drive = [IO.DriveInfo]::new([IO.Path]::GetPathRoot($WorkRoot))
        if ($drive.AvailableFreeSpace -lt 4GB) {
            throw "At least 4 GiB of free space is required on the evidence drive."
        }
        $null = Invoke-Docker "pull" @("pull", "--platform", "linux/amd64", "ubuntu:24.04") 300
        $digest = Invoke-Docker "base-digest" @(
            "image", "inspect", "ubuntu:24.04", "--format", "{{index .RepoDigests 0}}"
        )
        if ($digest -notmatch '^([a-z0-9./:-]+/)?ubuntu@sha256:[0-9a-f]{64}$') {
            throw "Cannot establish an immutable Ubuntu base digest."
        }
        $manifest.base_digest = $digest
        $tag = "os-project-asan:" + $runId
        $manifest.image_tag = $tag
        $null = Invoke-Docker "build" @(
            "build", "--platform", "linux/amd64", "--pull=false",
            "--build-arg", "BASE_IMAGE=$digest", "--tag", $tag,
            "--file", (Join-Path $PSScriptRoot "Dockerfile"), $PSScriptRoot
        ) 900
        $imageId = Invoke-Docker "image-id" @("image", "inspect", $tag, "--format", "{{.Id}}")
        if ($imageId -notmatch '^sha256:[0-9a-f]{64}$') {
            throw "Cannot establish the immutable built image ID."
        }
        $manifest.image_id = $imageId
        $containerAttempted = $true
        $null = Invoke-Docker "validation" @(
            "run", "--rm", "--name", $containerName, "--platform", "linux/amd64",
            "--network", "none", "--read-only", "--user", "65534:65534",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--cpus", "2", "--memory", "2g", "--memory-swap", "2g", "--pids-limit", "128",
            "--ulimit", "core=0", "--tmpfs", "/tmp:rw,exec,nosuid,nodev,size=256m,mode=1777",
            "--mount", "type=bind,source=$runRoot,target=/evidence",
            $imageId
        ) 300
        $containerAttempted = $false
        $summary = Get-Content -LiteralPath (Join-Path $runRoot "validation/summary.json") -Raw | ConvertFrom-Json
        $checks = @($summary.checks)
        if ($summary.status -ne "passed" -or $checks.Count -ne 7 -or
            @($checks | Where-Object { $_.passed -ne $true }).Count -ne 0) {
            throw "Validation did not pass all seven checks."
        }
        $manifest.checks_passed = 7
        $manifest.status = "passed"
        Write-Host "PASS: 7/7 functional checks. This is not a 2012 benchmark reproduction."
        Write-Host "Image: $imageId"
    }
} catch {
    $manifest.status = "failed"
    $manifest.error = $_.Exception.Message
    Write-Warning $_.Exception.Message
    if ($_.Exception.Message -match '^pull (failed|exceeded)') {
        Write-Host "Image download failed; the target environment has not been built."
        Write-Host "Check Docker Desktop's proxy/network connection, then rerun for a new evidence ID."
    }
} finally {
    if ($containerAttempted) {
        # Only this run's uniquely named container may be removed.
        try {
            $null = Invoke-Docker "cleanup" @("container", "rm", "--force", $containerName) 20
        } catch {
            # A successful --rm run has already removed its container.
            $manifest.cleanup_note = $_.Exception.Message
        }
    }
    $manifest.finished_at = [DateTime]::UtcNow.ToString("o")
    [IO.File]::WriteAllText(
        (Join-Path $runRoot "run.json"), ($manifest | ConvertTo-Json -Depth 8), $utf8
    )
    Write-Host "Evidence: $runRoot"
}
if ($manifest.status -eq "failed") {
    exit 1
}
