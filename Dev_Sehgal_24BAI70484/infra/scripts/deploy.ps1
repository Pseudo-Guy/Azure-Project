# ==============================================================================
# AzureCloudHub - Automated Deployment Script (PowerShell)
# Author: Dev Sehgal (UID: 24BAI70484)
# ==============================================================================

param(
    [string]$ResourceGroupName = "rg-azurecloudhub-prod",
    [string]$Location = "centralindia",
    [string]$Environment = "prod",
    [string]$Owner = "Dev Sehgal",
    [string]$CostCenter = "CC-70484"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " AzureCloudHub - Automated Cloud Deployment (AZ-900)" -ForegroundColor Cyan
Write-Host " Candidate: $Owner (UID: 24BAI70484)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Azure CLI authentication
Write-Host "`n[1/5] Checking Azure CLI session..." -ForegroundColor Yellow
$account = az account show --output json 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Error "Please authenticate by running: az login"
    exit 1
}
Write-Host "Connected to Subscription: $($account.name) ($($account.id))" -ForegroundColor Green

# 2. Create Resource Group with mandatory tags
Write-Host "`n[2/5] Creating Resource Group: $ResourceGroupName in $Location..." -ForegroundColor Yellow
az group create `
    --name $ResourceGroupName `
    --location $Location `
    --tags Environment=$Environment Owner="$Owner" Project="AzureCloudHub-AIML" CostCenter=$CostCenter `
    --output table

# 3. Assign Azure Policy definition for allowed locations
Write-Host "`n[3/5] Assigning Governance Policy: Allowed Locations..." -ForegroundColor Yellow
$policyPath = Join-Path $PSScriptRoot "..\policies\allowed-locations-policy.json"
if (Test-Path $policyPath) {
    az policy definition create `
        --name "allowed-locations-cloudhub" `
        --rules $policyPath `
        --output none 2>$null
    Write-Host "Governance policy registered." -ForegroundColor Green
}

# 4. Deploy Infrastructure via Bicep Template
Write-Host "`n[4/5] Deploying Infrastructure as Code (Bicep)..." -ForegroundColor Yellow
$bicepPath = Join-Path $PSScriptRoot "..\bicep\main.bicep"
$deployment = az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file $bicepPath `
    --parameters location=$Location environment=$Environment ownerName="$Owner" costCenter=$CostCenter `
    --output json | ConvertFrom-Json

$appUrl = $deployment.properties.outputs.appServiceEndpoint.value
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "Live Web Service: $appUrl" -ForegroundColor Cyan

# 5. Summary & Cost Warning
Write-Host "`n[5/5] Deployment Summary:" -ForegroundColor Yellow
Write-Host "  - Resource Group: $ResourceGroupName"
Write-Host "  - Region:         $Location"
Write-Host "  - Service URL:    $appUrl"
Write-Host "`n[NOTE] As recommended in Section 3.3 of your report, remember to run" -ForegroundColor Yellow
Write-Host "       ./cleanup.ps1 after testing to delete resources and prevent charges.`n" -ForegroundColor Yellow
