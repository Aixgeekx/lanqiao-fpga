param([string]$Version=(Get-Content -LiteralPath (Join-Path (Split-Path $PSScriptRoot -Parent) "VERSION")).Trim())
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
$repo=Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $repo
if($Version -notmatch '^v?\d+\.\d+\.\d+$'){throw "版本号必须形如 1.2.3 或 v1.2.3"}
$tag=if($Version.StartsWith("v")){$Version}else{"v$Version"}
if(git status --porcelain=v1 --untracked-files=all){throw "工作区不干净，请先提交或暂存当前改动"}
git fetch origin main
$behind=[int](git rev-list --count "HEAD..origin/main")
if($behind -gt 0){throw "本地落后 origin/main，请先拉取同步"}
if(git tag --list $tag){throw "标签 $tag 已存在"}
git tag -a $tag -m "Release $tag"
git push origin $tag
Write-Output "released $tag"
