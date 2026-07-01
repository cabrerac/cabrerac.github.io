# Ensure .cursor/ is gitignored and untracked in all git repos under given roots.
# Usage:
#   pwsh scripts/ensure_cursor_gitignored.ps1
#   pwsh scripts/ensure_cursor_gitignored.ps1 -Roots "D:\auto-ai\repositories","D:\s4\repositories"
#   pwsh scripts/ensure_cursor_gitignored.ps1 -WhatIf

param(
    [string[]] $Roots = @(
        "D:\auto-ai\repositories",
        "D:\s4\repositories",
        "D:\docs\repositories",
        "D:\aicu\repositories",
        "D:\interfaces\repositories"
    ),
    [switch] $WhatIf
)

$Marker = "# Cursor IDE (local machine; not for version control)"
$IgnoreLine = ".cursor/"

# Skip nested fixture / dataset clones (not top-level project repos)
$SkipPathPattern = '(\\|/)(bugs|dataset\\bugs)(\\|/)'

function Add-CursorGitignore {
    param([string] $RepoPath)
    $gitignore = Join-Path $RepoPath ".gitignore"
    if (Test-Path $gitignore) {
        $content = Get-Content $gitignore -Raw
        if ($content -match '(?m)^\.cursor(/|rules/)') {
            return "already_ignored"
        }
        $block = if ($content -match '\r?\n$') { "`n$Marker`n$IgnoreLine`n" } else { "`n`n$Marker`n$IgnoreLine`n" }
        if ($WhatIf) {
            return "would_append_gitignore"
        }
        Add-Content -Path $gitignore -Value "`n$Marker`n$IgnoreLine" -Encoding utf8
        return "appended_gitignore"
    }
    if ($WhatIf) {
        return "would_create_gitignore"
    }
    Set-Content -Path $gitignore -Value "$Marker`n$IgnoreLine`n" -Encoding utf8
    return "created_gitignore"
}

$repos = @()
foreach ($root in $Roots) {
    if (-not (Test-Path $root)) { continue }
    Get-ChildItem -Path $root -Recurse -Directory -Filter ".git" -ErrorAction SilentlyContinue | ForEach-Object {
        $repos += $_.Parent.FullName
    }
}
$repos = $repos | Where-Object { $_ -notmatch $SkipPathPattern } | Sort-Object -Unique

$summary = @()
foreach ($repo in $repos) {
    Push-Location $repo
    $rel = $repo
    $tracked = @(git ls-files ".cursor" 2>$null)
    $gitignoreAction = Add-CursorGitignore -RepoPath $repo
    $untrackAction = "none"
    if ($tracked.Count -gt 0) {
        if ($WhatIf) {
            $untrackAction = "would_untrack_$($tracked.Count)"
        } else {
            git rm -r --cached --quiet -- .cursor 2>$null
            if ($LASTEXITCODE -eq 0) {
                $untrackAction = "untracked_$($tracked.Count)"
            } else {
                $untrackAction = "untrack_failed"
            }
        }
    }
    if ($gitignoreAction -ne "already_ignored" -or $tracked.Count -gt 0) {
        $summary += [PSCustomObject]@{
            Repo = $rel
            Gitignore = $gitignoreAction
            Untrack = $untrackAction
        }
    }
    Pop-Location
}

if ($summary.Count -eq 0) {
    Write-Host "All repos already ignore .cursor/ and nothing was tracked."
} else {
    $summary | Format-Table -AutoSize -Wrap
    Write-Host "Repos touched: $($summary.Count). Review with 'git status' per repo; commit when ready."
}
