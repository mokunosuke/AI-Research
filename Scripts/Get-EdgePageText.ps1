param(
    [Parameter(Mandatory = $false)]
    [string]$Url,

    [Parameter(Mandatory = $false)]
    [ValidateRange(1000, 200000)]
    [int]$MaxCharacters = 60000,

    [Parameter(Mandatory = $false)]
    [ValidateRange(5, 120)]
    [int]$TimeoutSeconds = 40
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient

if ($Url) {
    $parsedUrl = $null
    if (-not [Uri]::TryCreate($Url, [UriKind]::Absolute, [ref]$parsedUrl) -or
        $parsedUrl.Scheme -notin @('http', 'https')) {
        throw 'Url must be an absolute http or https URL.'
    }

    $edge = Get-Process msedge -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne 0 } |
        Select-Object -First 1

    if (-not $edge) {
        throw 'Microsoft Edge is not running. Open Edge and sign in to the site, then retry.'
    }

    Start-Process -FilePath $edge.Path -ArgumentList "--new-tab `"$Url`""
}

$deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
$pageText = $null
$pageUrl = $null
$pageTitle = $null
$targetReached = -not $Url
$contentReady = $false

do {
    Start-Sleep -Milliseconds 700

    $edge = Get-Process msedge -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -ne 0 } |
        Select-Object -First 1

    if ($edge) {
        try {
            $root = [System.Windows.Automation.AutomationElement]::FromHandle(
                [IntPtr]$edge.MainWindowHandle
            )
            $pageTitle = $root.Current.Name

            $addressBar = $root.FindFirst(
                [System.Windows.Automation.TreeScope]::Descendants,
                [System.Windows.Automation.PropertyCondition]::new(
                    [System.Windows.Automation.AutomationElement]::AutomationIdProperty,
                    'view_1017'
                )
            )
            if ($addressBar) {
                $valuePattern = $null
                if ($addressBar.TryGetCurrentPattern(
                    [System.Windows.Automation.ValuePattern]::Pattern,
                    [ref]$valuePattern
                )) {
                    $pageUrl = $valuePattern.Current.Value
                }
            }

            if ($Url -and $pageUrl) {
                try {
                    $targetReached = ([Uri]$pageUrl).Host -eq $parsedUrl.Host -and
                        ([Uri]$pageUrl).AbsolutePath.TrimEnd('/') -eq $parsedUrl.AbsolutePath.TrimEnd('/')
                }
                catch {
                    $targetReached = $false
                }
            }

            $document = $root.FindFirst(
                [System.Windows.Automation.TreeScope]::Descendants,
                [System.Windows.Automation.PropertyCondition]::new(
                    [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
                    [System.Windows.Automation.ControlType]::Document
                )
            )

            if ($document) {
                $textPattern = $null
                if ($document.TryGetCurrentPattern(
                    [System.Windows.Automation.TextPattern]::Pattern,
                    [ref]$textPattern
                )) {
                    $pageText = $textPattern.DocumentRange.GetText($MaxCharacters)
                    $minimumLength = if ($pageUrl -match '^https?://(www\.)?x\.com/') { 900 } else { 250 }
                    $contentReady = $pageText.Length -ge $minimumLength -and
                        $pageText -notmatch '(?i)タイムラインを読み込み中|loading timeline|ページを読み込んでいます|loading\.\.\.'
                }
            }
        }
        catch {
            $pageText = $null
        }
    }
} while ((-not $contentReady -or -not $targetReached) -and
         [DateTime]::UtcNow -lt $deadline)

if (-not $contentReady) {
    throw 'Could not read page text from the active Edge tab before the timeout.'
}

if (-not $targetReached) {
    throw "Edge did not reach the requested host. Current address: $pageUrl"
}

"PAGE TITLE: $pageTitle"
"PAGE URL: $pageUrl"
'--- PAGE TEXT ---'
$pageText
