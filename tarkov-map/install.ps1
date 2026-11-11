# Tarkov Map - installer. Run in PowerShell:
#   irm https://raw.githubusercontent.com/DevidBb/AndmeBaasidlogITPV24/claude/optimistic-dijkstra-b4tprc/tarkov-map/install.ps1 | iex
$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$Branch = 'claude/optimistic-dijkstra-b4tprc'
$Zip = "https://codeload.github.com/DevidBb/AndmeBaasidlogITPV24/zip/refs/heads/$Branch"
$Dir = Join-Path $env:LOCALAPPDATA 'TarkovMap'

function Find-Python {
    foreach ($c in @(@('py', '-3'), @('python'))) {
        $cmd = Get-Command $c[0] -ErrorAction SilentlyContinue
        if ($cmd -and $cmd.Source -notlike '*WindowsApps*') {
            try {
                $args2 = @($c | Select-Object -Skip 1) + @('-c', 'import sys; print(sys.executable)')
                $exe = & $c[0] @args2 2>$null
                if ($LASTEXITCODE -eq 0 -and $exe) { return ($exe | Select-Object -Last 1).Trim() }
            } catch {}
        }
    }
    $found = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe" -ErrorAction SilentlyContinue |
             Sort-Object FullName -Descending | Select-Object -First 1
    if ($found) { return $found.FullName }
    return $null
}

Write-Host "`n=== Tarkov Map: установка ===`n" -ForegroundColor Yellow

$py = Find-Python
if (-not $py) {
    Write-Host "Python не найден - ставлю (1-2 минуты)..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install -e --id Python.Python.3.12 --scope user --silent --accept-package-agreements --accept-source-agreements | Out-Null
        $py = Find-Python
    }
    if (-not $py) {
        $inst = Join-Path $env:TEMP 'python-setup.exe'
        Invoke-WebRequest 'https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe' -OutFile $inst -UseBasicParsing
        Start-Process $inst -ArgumentList '/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1' -Wait
        $py = Find-Python
    }
    if (-not $py) { throw "Не получилось поставить Python. Поставь его с python.org и запусти установку ещё раз." }
}
Write-Host "Python: $py"

Write-Host "Скачиваю приложение..."
$tmp = Join-Path $env:TEMP "tarkovmap_$([guid]::NewGuid().ToString('N'))"
New-Item -ItemType Directory -Path $tmp | Out-Null
try { Invoke-WebRequest $Zip -OutFile "$tmp\app.zip" -UseBasicParsing -ErrorAction Stop }
catch { throw "Не удалось скачать приложение: $_" }
Expand-Archive "$tmp\app.zip" -DestinationPath $tmp
$src = Get-ChildItem $tmp -Directory | Select-Object -First 1
New-Item -ItemType Directory -Path $Dir -Force | Out-Null
Copy-Item "$($src.FullName)\tarkov-map\*" $Dir -Recurse -Force
Remove-Item $tmp -Recurse -Force

Write-Host "Ставлю библиотеки (numpy, opencv)..."
& $py -m pip install -q --disable-pip-version-check -r "$Dir\requirements.txt" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "Библиотеки не поставились - карта будет работать, цены предметов нет." -ForegroundColor Red }

# Desktop button
$lnk = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Tarkov Map.lnk'
$sh = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk)
$sh.TargetPath = $py
$sh.Arguments = "`"$Dir\server.py`" --open"
$sh.WorkingDirectory = $Dir
$sh.Save()
Write-Host "`nГотово! На рабочем столе появилась кнопка 'Tarkov Map'." -ForegroundColor Green
Write-Host "Запускаю... Если Windows спросит про брандмауэр - нажми 'Разрешить'.`n"

& $py "$Dir\server.py" --open
