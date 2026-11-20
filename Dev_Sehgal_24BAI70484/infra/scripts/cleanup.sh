#!/usr/bin/env bash
# ==============================================================================
# AzureCloudHub - Resource Cleanup Script (Bash)
# ==============================================================================

RESOURCE_GROUP="rg-azurecloudhub-prod"

echo "=========================================================="
echo " AzureCloudHub - Cloud Teardown & Cost Guard"
echo "=========================================================="

read -p "Are you sure you want to delete resource group '$RESOURCE_GROUP'? (y/n): " confirm
if [[ $confirm =~ ^[Yy]$ ]]; then
    echo "Removing resource lock if present..."
    az lock delete --name "lock-prevent-accidental-deletion" --resource-group "$RESOURCE_GROUP" 2>/dev/null || true

    echo "Deleting resource group '$RESOURCE_GROUP'..."
    az group delete --name "$RESOURCE_GROUP" --yes --no-wait
    echo "[OK] Resource group deletion initiated. No further charges will occur."
else
    echo "Teardown aborted."
fi
