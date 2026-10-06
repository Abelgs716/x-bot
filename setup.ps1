# Instalador del bot de X. Ejecutar: powershell -ExecutionPolicy Bypass -File setup.ps1
$dir = $PSScriptRoot
$py = (Get-Command python).Source
$pyw = $py -replace 'python\.exe$', 'pythonw.exe'

Write-Host "== Claves de X (developer.x.com > tu App > Keys and tokens) ==" -ForegroundColor Cyan
Write-Host "IMPORTANTE: antes de generar el Access Token, pon la App en 'Read and write'."
$k  = Read-Host "API Key"
$ks = Read-Host "API Key Secret"
$t  = Read-Host "Access Token"
$ts = Read-Host "Access Token Secret"

Write-Host "`n== Telegram (opcional, Enter para saltar) ==" -ForegroundColor Cyan
$tg  = Read-Host "Token de @BotFather"
$tgu = ""
if ($tg) { $tgu = Read-Host "Tu ID numerico de Telegram (pidelo a @userinfobot)" }

@"
X_API_KEY=$k
X_API_SECRET=$ks
X_ACCESS_TOKEN=$t
X_ACCESS_SECRET=$ts
TELEGRAM_TOKEN=$tg
TELEGRAM_ALLOWED_USER_ID=$tgu
"@ | Out-File -Encoding ascii "$dir\.env"

& $py "$dir\check.py"
if ($LASTEXITCODE -ne 0) { Write-Host "Las claves no funcionan. Revisa y vuelve a ejecutar setup.ps1" -ForegroundColor Red; exit 1 }

$horas = Read-Host "`nHoras de publicacion separadas por coma (Enter = 10:00,18:30)"
if (-not $horas) { $horas = "10:00,18:30" }
Get-ScheduledTask -TaskName "XBot-*" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false
$i = 0
foreach ($h in $horas.Split(",")) {
    $i++
    $a = New-ScheduledTaskAction -Execute $pyw -Argument "`"$dir\post_next.py`"" -WorkingDirectory $dir
    $tr = New-ScheduledTaskTrigger -Daily -At $h.Trim()
    $s = New-ScheduledTaskSettingsSet -StartWhenAvailable
    Register-ScheduledTask -TaskName "XBot-$i" -Action $a -Trigger $tr -Settings $s | Out-Null
    Write-Host "Programado: un tweet diario a las $($h.Trim())" -ForegroundColor Green
}

if ($tg) {
    $a = New-ScheduledTaskAction -Execute $pyw -Argument "`"$dir\telegram_bot.py`"" -WorkingDirectory $dir
    $tr = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
    $s = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit 0 -RestartCount 99 -RestartInterval (New-TimeSpan -Minutes 1)
    Register-ScheduledTask -TaskName "XBot-Telegram" -Action $a -Trigger $tr -Settings $s | Out-Null
    Start-ScheduledTask -TaskName "XBot-Telegram"
    Write-Host "Bot de Telegram arrancado (se inicia solo al encender el PC)" -ForegroundColor Green
}

$n = (Get-Content "$dir\queue.json" -Raw -Encoding utf8 | ConvertFrom-Json).Count
Write-Host "`nListo. $n tweets en cola. Historial en log.txt" -ForegroundColor Green
