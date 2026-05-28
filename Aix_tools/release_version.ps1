param([string]$Version=(Get-Content -LiteralPath (Join-Path (Split-Path $PSScriptRoot -Parent) "VERSION")).Trim())
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
$repo=Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $repo
if($Version -notmatch '^v?\d+\.\d+\.\d+$'){throw "Version must look like 1.2.3 or v1.2.3"}
$tag=if($Version.StartsWith("v")){$Version}else{"v$Version"}
if(git status --porcelain=v1 --untracked-files=all){throw "Working tree is not clean; commit or stash changes first"}
git fetch origin main
$behind=[int](git rev-list --count "HEAD..origin/main")
if($behind -gt 0){throw "Local branch is behind origin/main; pull first"}
if(git tag --list $tag){throw "Tag $tag already exists"}
git tag -a $tag -m "Release $tag"
git push origin $tag
Write-Output "released $tag"
