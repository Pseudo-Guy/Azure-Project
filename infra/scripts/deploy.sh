#!/usr/bin/env bash
# ==============================================================================
# AzureCloudHub - Automated Deployment Script (Bash)
# Author: Arighna Sadhu (UID: 24BAI70500)
# ==============================================================================

set -e

RESOURCE_GROUP="rg-azurecloudhub-prod"
LOCATION="centralindia"
ENVIRONMENT="prod"
OWNER="Arighna Sadhu"
COST_CENTER="CC-70500"

echo "=========================================================="
echo " AzureCloudHub - Automated Cloud Deployment (AZ-900)"
echo " Candidate: $OWNER (UID: 24BAI70500)"
echo "=========================================================="

echo "[1/4] Checking Azure CLI login..."
az account show --output table

echo "[2/4] Creating Resource Group: $RESOURCE_GROUP in $LOCATION..."
az group create \
  --name "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --tags Environment="$ENVIRONMENT" Owner="$OWNER" Project="AzureCloudHub-AIML" CostCenter="$COST_CENTER" \
  --output table

echo "[3/4] Deploying Infrastructure as Code (Bicep)..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file "$SCRIPT_DIR/../bicep/main.bicep" \
  --parameters location="$LOCATION" environment="$ENVIRONMENT" ownerName="$OWNER" costCenter="$COST_CENTER" \
  --output table

echo "[4/4] Deployment completed successfully!"
echo "Run ./cleanup.sh when finished to delete the resource group and avoid charges."
