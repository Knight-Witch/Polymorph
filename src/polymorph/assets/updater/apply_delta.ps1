param(
    [Parameter(Mandatory=$true)][string]$InstallDir,
    [Parameter(Mandatory=$true)][string]$StageDir,
    [Parameter(Mandatory=$true)][int]$ParentPid,
    [Parameter(Mandatory=$true)][string]$BaseVersion,
    [Parameter(Mandatory=$true)][string]$TargetVersion,
    [switch]$NoRestart,
    [int]$TestFailAfter = 0
)
$ErrorActionPreference = "Stop"
$manifest = Get-Content -LiteralPath (Join-Path $StageDir "manifest.json") -Raw | ConvertFrom-Json
if ($manifest.schema -ne 1 -or $manifest.from_version -ne $BaseVersion -or $manifest.to_version -ne $TargetVersion) {
    throw "Update manifest identity mismatch"
}
$backup = Join-Path $StageDir "rollback"
New-Item -ItemType Directory -Force -Path $backup | Out-Null
$applied = [System.Collections.Generic.List[string]]::new()
function Assert-Hash([string]$Path, [string]$Expected) {
    if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing file: $Path" }
    # Works in both Windows PowerShell and PowerShell Core even when hash cmdlets
    # are unavailable or implicit module loading is disabled.
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $stream = [System.IO.File]::OpenRead($Path)
    try { $actual = [System.BitConverter]::ToString($sha.ComputeHash($stream)).Replace("-", "").ToLowerInvariant() }
    finally { $stream.Dispose(); $sha.Dispose() }
    if ($actual -ne $Expected) { throw "Checksum mismatch: $Path" }
}
try {
    # Wait for Polymorph.exe to release its locked binaries, never kill its process.
    for ($attempt = 0; $attempt -lt 150; $attempt++) {
        if (!(Get-Process -Id $ParentPid -ErrorAction SilentlyContinue)) { break }
        Start-Sleep -Milliseconds 200
    }
    if (Get-Process -Id $ParentPid -ErrorAction SilentlyContinue) { throw "App did not close for update" }
    # Validate entire source state before modifying even one byte.
    foreach ($entry in $manifest.files) {
        $rel = [string]$entry.path
        if ($rel -notmatch '^[A-Za-z0-9_./+\-]+$' -or $rel.Contains("..") -or $rel.StartsWith("/")) {
            throw "Unsafe update path"
        }
        $target = Join-Path $InstallDir $rel
        $source = Join-Path (Join-Path $StageDir "payload") $rel
        Assert-Hash $source ([string]$entry.after)
        if ($null -ne $entry.before) { Assert-Hash $target ([string]$entry.before) }
        elseif (Test-Path -LiteralPath $target) { throw "Existing unexpected destination" }
    }
    foreach ($entry in $manifest.files) {
        $rel = [string]$entry.path
        $target = Join-Path $InstallDir $rel
        $source = Join-Path (Join-Path $StageDir "payload") $rel
        $saved = Join-Path $backup $rel
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        if ($null -ne $entry.before) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $saved) | Out-Null
            Copy-Item -LiteralPath $target -Destination $saved -Force
        }
        $applied.Add($rel)
        Copy-Item -LiteralPath $source -Destination $target -Force
        Assert-Hash $target ([string]$entry.after)
        if ($TestFailAfter -gt 0 -and $applied.Count -ge $TestFailAfter) {
            throw "Injected rollback QA failure"
        }
    }
    $key = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Polymorph"
    if (Test-Path $key) { Set-ItemProperty -Path $key -Name DisplayVersion -Value $TargetVersion }
    if (!$NoRestart) { Start-Process -FilePath (Join-Path $InstallDir "Polymorph.exe") }
    "Update installed: $BaseVersion -> $TargetVersion" | Set-Content -LiteralPath (Join-Path $StageDir "result.txt")
} catch {
    $message = $_.Exception.Message
    for ($i = $applied.Count - 1; $i -ge 0; $i--) {
        $rel = $applied[$i]
        $target = Join-Path $InstallDir $rel
        $saved = Join-Path $backup $rel
        if (Test-Path -LiteralPath $saved) { Copy-Item -LiteralPath $saved -Destination $target -Force }
        else { Remove-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue }
    }
    "Update failed and rolled back: $message" | Set-Content -LiteralPath (Join-Path $StageDir "result.txt")
    [Console]::Error.WriteLine("Delta helper rollback: $message")
    exit 1
}
