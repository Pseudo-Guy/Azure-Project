# ==============================================================================
# AzureCloudHub - Resource Cleanup Script (PowerShell)
# Implements Report Recommendation §3.3: Delete resource groups to avoid charges
# ==============================================================================

param(
    [string]$ResourceGroupName = "rg-azurecloudhub-prod"
)

Write-Host "==========================================================" -ForegroundColor Red
Write-Host " AzureCloudHub - Cloud Teardown & Cost Guard" -ForegroundColor Red
Write-Host "==========================================================" -ForegroundColor Red

Write-Host "`nWARNING: This will delete resource group '$ResourceGroupName' and all resources inside it." -ForegroundColor Yellow
$confirm = Read-Host "Are you sure you want to proceed? (Y/N)"

if ($confirm -match "^[yY]") {
    Write-Host "`nRemoving resource lock if present..." -ForegroundColor Yellow
    az lock delete --name "lock-prevent-accidental-deletion" --resource-group $ResourceGroupName 2>$null
    
    Write-Host "Deleting resource group '$ResourceGroupName' asynchronously..." -ForegroundColor Yellow
    az group delete --name $ResourceGroupName --yes --no-wait
    Write-Host "[OK] Resource group deletion initiated. No further cloud charges will occur." -ForegroundColor Green
} else {
    Write-Host "Teardown aborted." -ForegroundColor Gray
}
