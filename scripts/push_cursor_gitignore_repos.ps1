# Commit and push .cursor/ gitignore changes across git repos.
#
# Only touches repos with pending changes to .gitignore and/or .cursor/ (untrack).
# Skips repos with other uncommitted changes unless -AllowOtherChanges.
#
# Usage:
#   powershell -File scripts/push_cursor_gitignore_repos.ps1 -WhatIf
#   powershell -File scripts/push_cursor_gitignore_repos.ps1
#   powershell -File scripts/push_cursor_gitignore_repos.ps1 -Repos "D:\auto-ai\repositories\diary"
#
# Typical flow:
#   1. ensure_cursor_gitignored.ps1   (local gitignore + git rm --cached)
#   2. push_cursor_gitignore_repos.ps1 -WhatIf
#   3. push_cursor_gitignore_repos.ps1

param(
    [string[]] $Roots = @(
        "D:\auto-ai\repositories",
        "D:\s4\repositories",
        "D:\docs\repositories",
        "D:\aicu\repositories",
        "D:\interfaces\repositories"
    ),
    [string[]] $Repos = @(),
    [string] $CommitMessage = "Stop tracking local Cursor IDE config",
    [switch] $WhatIf,
    [switch] $SkipPull,
    [switch] $AllowOtherChanges
)

$SkipPathPattern = '(\\|/)(bugs|dataset\\bugs)(\\|/)'

function Get-RepoList {
    if ($Repos.Count -gt 0) {
        return $Repos | Where-Object { Test-Path (Join-Path $_ ".git") }
    }
    $found = @()
    foreach ($root in $Roots) {
        if (-not (Test-Path $root)) { continue }
        Get-ChildItem -Path $root -Recurse -Directory -Filter ".git" -ErrorAction SilentlyContinue | ForEach-Object {
            $found += $_.Parent.FullName
        }
    }
    return $found | Where-Object { $_ -notmatch $SkipPathPattern } | Sort-Object -Unique
}

function Test-CursorOnlyChanges {
    param([string[]] $PorcelainLines)
    if ($PorcelainLines.Count -eq 0) { return $false }
    $cursorRelated = $false
    foreach ($line in $PorcelainLines) {
        if ($line.Length -lt 4) { continue }
        $path = $line.Substring(3).Trim('"')
        if ($path -eq ".gitignore" -or $path -like ".cursor/*" -or $path -eq ".cursor") {
            $cursorRelated = $true
            continue
        }
        if (-not $AllowOtherChanges) {
            return $false
        }
    }
    return $cursorRelated
}

$results = @()
foreach ($repo in (Get-RepoList)) {
    Push-Location $repo
    $status = @(git status --porcelain 2>$null)
    if (-not (Test-CursorOnlyChanges -PorcelainLines $status)) {
        Pop-Location
        continue
    }

    $remote = git remote 2>$null | Select-Object -First 1
    $branch = git branch --show-current 2>$null
    $action = "pending"

    if ($WhatIf) {
        $action = "would_commit_push"
    } else {
        if (-not $SkipPull -and $remote) {
            git pull --rebase 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                $action = "pull_failed"
                $results += [PSCustomObject]@{ Repo = $repo; Branch = $branch; Action = $action }
                Pop-Location
                continue
            }
        }

        git add -- .gitignore .cursor 2>$null
        git commit -m $CommitMessage 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            $action = "commit_failed"
        } elseif ($remote) {
            git push 2>&1 | Out-Null
            $action = if ($LASTEXITCODE -eq 0) { "pushed" } else { "push_failed" }
        } else {
            $action = "committed_no_remote"
        }
    }

    $results += [PSCustomObject]@{
        Repo = $repo
        Branch = $branch
        Action = $action
        Files = ($status -join "; ")
    }
    Pop-Location
}

if ($results.Count -eq 0) {
    Write-Host "No repos with pending .cursor/.gitignore-only changes."
} else {
    $results | Format-Table -AutoSize -Wrap
    if ($WhatIf) {
        Write-Host "Dry run: $($results.Count) repo(s) would be committed and pushed."
    } else {
        $ok = ($results | Where-Object { $_.Action -eq "pushed" }).Count
        Write-Host "Pushed: $ok / $($results.Count)"
    }
}
