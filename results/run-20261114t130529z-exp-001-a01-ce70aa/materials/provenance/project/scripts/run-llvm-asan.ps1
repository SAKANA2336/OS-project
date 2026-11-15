#Requires -Version 5.1
[CmdletBinding()]
param(
    [string]$Python = "python",
    [string]$Image = "",
    [switch]$FetchOnly
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$configPath = Join-Path $root "config/llvm-asan.json"
$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
$source = Join-Path $root "workloads/downloads/llvm-test-suite"
$utf8 = [Text.UTF8Encoding]::new($false)

& $Python (Join-Path $PSScriptRoot "llvm-asan.py") fetch --source $source
if ($LASTEXITCODE -ne 0) { throw "Pinned workload acquisition/verification failed." }
if ($FetchOnly) { return }
if (-not $Image) { $Image = $config.image }

$runId = "run-" + [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ").ToLowerInvariant() +
    "-exp-001-a01-" + [Guid]::NewGuid().ToString("N").Substring(0, 6)
$runRoot = Join-Path $root "runs/$runId"
$null = New-Item -ItemType Directory -Path $runRoot
$container = "os-project-" + $runId
$hostRecord = [ordered]@{
    run_id = $runId
    kind = "exploratory-workload-transfer"
    status = "started"
    started_at = [DateTime]::UtcNow.ToString("o")
    image_id = $Image
}

function Quote-Native([string]$Value) {
    $escaped = [regex]::Replace($Value, '(\\*)"', '$1$1\"')
    $escaped = [regex]::Replace($escaped, '(\\+)$', '$1$1')
    return '"' + $escaped + '"'
}

function Invoke-DockerRecorded([string[]]$DockerArguments, [string]$Label, [int]$TimeoutSeconds) {
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $docker
    $start.Arguments = (($DockerArguments | ForEach-Object { Quote-Native $_ }) -join " ")
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    $timedOut = $false
    try {
        $null = $process.Start()
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
            $timedOut = $true
            $process.Kill()
            $process.WaitForExit(5000) | Out-Null
        }
        $null = $stdout.Wait(5000)
        $null = $stderr.Wait(5000)
        $prefix = Join-Path $runRoot $Label
        [IO.File]::WriteAllText(($prefix + ".stdout.log"), $stdout.Result, $utf8)
        [IO.File]::WriteAllText(($prefix + ".stderr.log"), $stderr.Result, $utf8)
        $record = @{
            arguments = $DockerArguments; exit_code = $process.ExitCode; timed_out = $timedOut
        }
        [IO.File]::WriteAllText(
            ($prefix + ".command.json"), ($record | ConvertTo-Json -Depth 4), $utf8
        )
        if ($timedOut -or $process.ExitCode -ne 0) {
            throw "Docker $Label failed. See $Label.stderr.log in the evidence directory."
        }
        return $stdout.Result.Trim()
    } finally {
        $process.Dispose()
    }
}

try {
    foreach ($path in @($root, $source, $runRoot)) {
        if ($path.Contains(",")) { throw "Docker mount paths must not contain commas." }
    }
    $commit = (& git -C $root rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Cannot record project commit." }
    $hostRecord.project_commit = $commit
    $changed = @(& git -C $root status --short)
    $hostRecord.project_dirty = $changed.Count -gt 0
    # Preserve the attempted implementation even if Docker preflight fails.
    $snapshot = Join-Path $runRoot "provenance/project"
    $hostRecord.project_sources_sha256 = @{}
    foreach ($relative in @(
        "scripts/llvm-asan.py", "scripts/run-llvm-asan.ps1", "config/llvm-asan.json",
        "workloads/llvm-suite-lock.json", "experiments/exp-001/PLAN.md"
    )) {
        $destination = Join-Path $snapshot $relative
        $null = New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force
        Copy-Item -LiteralPath (Join-Path $root $relative) -Destination $destination
        $hostRecord.project_sources_sha256[$relative] =
            (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    $docker = (Get-Command docker.exe -ErrorAction Stop).Source
    Write-Host "Evidence: $runRoot"
    Write-Host "[preflight] Checking local Docker engine and pinned image..."
    $endpoint = Invoke-DockerRecorded @(
        "context", "inspect", "desktop-linux", "--format", "{{.Endpoints.docker.Host}}"
    ) "preflight-context" 30
    if ($endpoint -ne "npipe:////./pipe/dockerDesktopLinuxEngine") {
        throw "Expected the local Docker Desktop Linux endpoint."
    }
    $engineRaw = Invoke-DockerRecorded @(
        "--context", "desktop-linux", "info", "--format", "{{json .}}"
    ) "preflight-engine" 30
    $engine = $engineRaw | ConvertFrom-Json
    if ($engine.OSType -ne "linux" -or $engine.Architecture -notin @("x86_64", "amd64")) {
        throw "Linux x86_64 is required."
    }
    if (-not $engine.MemoryLimit -or -not $engine.SwapLimit -or
        -not $engine.PidsLimit -or -not $engine.CpuCfsQuota -or $engine.MemTotal -lt 4GB) {
        throw "Docker needs CPU/memory/swap/PID limits and at least 4 GiB available to the engine."
    }
    $resolvedImage = Invoke-DockerRecorded @(
        "--context", "desktop-linux", "image", "inspect", $Image, "--format", "{{.Id}}"
    ) "preflight-image" 30
    if ($resolvedImage -notmatch '^sha256:[0-9a-f]{64}$') {
        throw "Pinned image is missing. Build the existing ASan environment first; no automatic pull."
    }
    $hostRecord.image_id = $resolvedImage
    $hostRecord.engine = @{
        version = $engine.ServerVersion; kernel = $engine.KernelVersion
        cpus = $engine.NCPU; memory_bytes = $engine.MemTotal
    }
    $arguments = @(
        "--context", "desktop-linux", "run", "--rm", "--name", $container,
        "--platform", "linux/amd64", "--network", "none", "--read-only",
        "--user", "65534:65534", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--cpus", [string]$config.limits.cpus,
        "--memory", $config.limits.memory, "--memory-swap", $config.limits.memory,
        "--pids-limit", [string]$config.limits.pids, "--ulimit", "core=0",
        "--tmpfs", ("`/tmp:rw,exec,nosuid,nodev,size=" + $config.limits.tmpfs + ",mode=1777"),
        "--mount", "type=bind,source=$root,target=/project,readonly",
        "--mount", "type=bind,source=$source,target=/suite,readonly",
        "--mount", "type=bind,source=$runRoot,target=/evidence",
        "--entrypoint", "python3", $resolvedImage, "/project/scripts/llvm-asan.py", "run",
        "--source", "/suite", "--output", "/evidence", "--run-id", $runId,
        "--project-commit", $commit, "--image", $resolvedImage
    )
    # This local evidence may contain host mount paths; review before publication.
    [IO.File]::WriteAllText(
        (Join-Path $runRoot "container-arguments.local.json"),
        ($arguments | ConvertTo-Json -Depth 4), $utf8
    )
    Write-Host "[pilot] Building both arms and validating six workloads (up to 25 minutes)..."
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $docker
    $start.Arguments = (($arguments | ForEach-Object { Quote-Native $_ }) -join " ")
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        $null = $process.Start()
        $stdout = $process.StandardOutput.ReadToEndAsync()
        $stderr = $process.StandardError.ReadToEndAsync()
        $timedOut = -not $process.WaitForExit([int]$config.overall_timeout_seconds * 1000)
        if ($timedOut) {
            try {
                Invoke-DockerRecorded @(
                    "--context", "desktop-linux", "container", "rm", "--force", $container
                ) "timeout-cleanup" 30 | Out-Null
            } catch {
                $hostRecord.container_cleanup_error = $_.Exception.Message
            } finally {
                if (-not $process.HasExited) { $process.Kill() }
            }
        }
        $null = $stdout.Wait(5000)
        $null = $stderr.Wait(5000)
        $safeStdout = [regex]::Replace(
            $stdout.Result, [regex]::Escape($runRoot), "<run-evidence>",
            [Text.RegularExpressions.RegexOptions]::IgnoreCase
        )
        $safeStderr = [regex]::Replace(
            $stderr.Result, [regex]::Escape($runRoot), "<run-evidence>",
            [Text.RegularExpressions.RegexOptions]::IgnoreCase
        )
        [IO.File]::WriteAllText((Join-Path $runRoot "host.stdout.log"), $safeStdout, $utf8)
        [IO.File]::WriteAllText((Join-Path $runRoot "host.stderr.log"), $safeStderr, $utf8)
        $hostRecord.exit_code = $process.ExitCode
        $hostRecord.timed_out = $timedOut
        if ($timedOut) { throw "Experiment exceeded its overall time budget; container stop requested." }
        $manifestPath = Join-Path $runRoot "run-manifest.json"
        if (Test-Path -LiteralPath $manifestPath) {
            $containerStatus = (Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json).status
            $hostRecord.container_status = $containerStatus
        }
        if ($process.ExitCode -ne 0) {
            if ($hostRecord.container_status -eq "invalid_pilot") {
                $hostRecord.status = "invalid_pilot"
                throw "Pilot completed but at least one sample is invalid; inspect metrics and validation."
            }
            throw "Experiment failed; see host.stderr.log and per-command logs."
        }
    } finally {
        $process.Dispose()
    }
    $hostRecord.status = "completed_pilot"
    Write-Host "Pilot completed. This is not a SPEC CPU2006 reproduction."
} catch {
    if ($hostRecord.status -ne "invalid_pilot") { $hostRecord.status = "failed" }
    $hostRecord.error = $_.Exception.Message
    Write-Warning $_.Exception.Message
} finally {
    $hostRecord.finished_at = [DateTime]::UtcNow.ToString("o")
    [IO.File]::WriteAllText(
        (Join-Path $runRoot "host.json"), ($hostRecord | ConvertTo-Json -Depth 8), $utf8
    )
    Write-Host "Evidence: $runRoot"
}
if ($hostRecord.status -eq "failed") { exit 1 }
