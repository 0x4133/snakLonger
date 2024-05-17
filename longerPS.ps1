# Define the abbreviations and their expansions
$expansions = @{
    "brb" = "be right back"
    "omw" = "on my way"
    "idk" = "I don't know"
    "smh" = "shaking my head"
    "btw" = "by the way"
}

# Function to simulate key presses
function Simulate-KeyPress {
    param (
        [string]$text
    )

    foreach ($char in $text.ToCharArray()) {
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait($char)
        Start-Sleep -Milliseconds 20  # Delay to simulate typing speed
    }
}

# Monitor clipboard for changes and replace abbreviations
while ($true) {
    Add-Type -AssemblyName System.Windows.Forms
    $clipboardText = [System.Windows.Forms.Clipboard]::GetText()

    foreach ($abbreviation in $expansions.Keys) {
        if ($clipboardText -match "\b$abbreviation\b") {
            $expandedText = $expansions[$abbreviation]
            $clipboardText = $clipboardText -replace "\b$abbreviation\b", $expandedText
            [System.Windows.Forms.Clipboard]::SetText($clipboardText)
            Simulate-KeyPress $expandedText
        }
    }

    Start-Sleep -Milliseconds 100  # Polling interval
}