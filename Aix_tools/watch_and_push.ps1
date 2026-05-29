param([int]$IntervalSeconds=60,[string]$Branch="main",[string]$RepoPath=(Resolve-Path (Join-Path $PSScriptRoot "..")).Path,[string]$LogPath=(Join-Path $PSScriptRoot "git_watch_push.log"))
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
function Log($Message){Add-Content -LiteralPath $LogPath -Value ("{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"),$Message) -Encoding UTF8}
Set-Location -LiteralPath $RepoPath
[IO.File]::WriteAllText((Join-Path $PSScriptRoot "git_watch_push.pid"),"$PID",[Text.Encoding]::UTF8)
Log "watcher started repo=$RepoPath branch=$Branch interval=${IntervalSeconds}s"
while($true){
  try{
    Set-Location -LiteralPath $RepoPath
    $RepairScript=Join-Path $PSScriptRoot "repair_pdf_stats.py"
    if(Test-Path -LiteralPath $RepairScript){$RepairOutput=& python $RepairScript 2>&1;if($LASTEXITCODE -ne 0){throw ("repair_pdf_stats failed: "+($RepairOutput -join " | "))};foreach($Line in $RepairOutput){if($Line){Log $Line}}}
    if(git status --porcelain=v1 --untracked-files=all){git add -A -- .;if(git diff --cached --name-only){$t=Get-Date -Format "yyyy-MM-dd HH:mm:ss";git commit -m "chore: auto sync $t";Log "committed $t"}}
    git fetch origin $Branch
    $behind=[int](git rev-list --count "HEAD..origin/$Branch")
    if($behind -gt 0){git pull --rebase --autostash origin $Branch;Log "rebased from origin/$Branch"}
    $ahead=[int](git rev-list --count "origin/$Branch..HEAD")
    if($ahead -gt 0){git push origin $Branch;Log "pushed $ahead commit(s)"}
  }catch{Log ("error: "+$_.Exception.Message)}
  Start-Sleep -Seconds $IntervalSeconds
}
