param (
    [string]$FilePath
)

# Load required .NET ZIP libraries
Add-Type -AssemblyName System.IO.Compression.FileSystem

# Temporary extraction path
$TempPath = "C:\Users\JGI\Desktop\ci-scripts\temp_extract"
$CorePropsPath = "$TempPath\docProps\core.xml"

# Ensure the temp directory is clean
if (Test-Path $TempPath) { Remove-Item -Recurse -Force $TempPath }
New-Item -ItemType Directory -Path $TempPath | Out-Null

# Extract the Excel file (ZIP Archive)
[System.IO.Compression.ZipFile]::ExtractToDirectory($FilePath, $TempPath)

# Load CoreProperties.xml
[xml]$CoreProperties = Get-Content $CorePropsPath

# Define XML namespace manager
$xmlNS = New-Object System.Xml.XmlNamespaceManager($CoreProperties.NameTable)
$xmlNS.AddNamespace("cp", "http://schemas.openxmlformats.org/package/2006/metadata/core-properties")

# Find "cp:version" node
$VersionNode = $CoreProperties.SelectSingleNode("//cp:version", $xmlNS)

# Set version as today's date
$Version = Get-Date -Format "yyyy-MM-dd"

# If found, update it; otherwise, create it
if ($VersionNode) {
    Write-Host "✅ Found 'cp:version' -> Current Value: $($VersionNode.InnerText)"
    $VersionNode.InnerText = $Version
} else {
    Write-Host "⚠️ 'cp:version' not found! Creating it now..."
    $VersionNode = $CoreProperties.CreateElement("cp", "version", "http://schemas.openxmlformats.org/package/2006/metadata/core-properties")
    $VersionNode.InnerText = $Version
    $CoreProperties.DocumentElement.AppendChild($VersionNode) | Out-Null
}

# Save updated CoreProperties.xml
$CoreProperties.Save($CorePropsPath)

# Delete the original file before overwriting (Windows ZIP APIs require this)
Remove-Item $FilePath -Force

# Recreate the modified Excel file as a ZIP archive
[System.IO.Compression.ZipFile]::CreateFromDirectory($TempPath, $FilePath)

# Cleanup
Remove-Item -Recurse -Force $TempPath

Write-Host "✅ Successfully updated 'Version number' to '$Version' in $FilePath"
