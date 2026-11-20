// ==============================================================================
// AzureCloudHub - Infrastructure as Code (Bicep)
// Provisions Enterprise AI Model Serving Architecture on Microsoft Azure
// Author: Arighna Sadhu (UID: 24BAI70500) | AZ-900 Project Portfolio
// ==============================================================================

@description('Primary deployment location compliant with Azure Governance Allowed Locations')
param location string = 'centralindia'

@description('Deployment environment tier')
@allowed([
  'dev'
  'test'
  'prod'
])
param environment string = 'prod'

@description('Workload project prefix')
param projectName string = 'cloudhub'

@description('Candidate & Owner tag value')
param ownerName string = 'Arighna Sadhu'

@description('Cost center code for cost allocation and billing')
param costCenter string = 'CC-70500'

@description('Monthly spending budget limit in USD')
param monthlyBudgetAmount int = 150

@description('Email address for Cost Management budget alert notifications')
param alertEmail string = 'arighna.sadhu@chandigarhuniversity.ac.in'

// Common enterprise tags enforced by Azure Policy
var standardTags = {
  Environment: environment
  Owner: ownerName
  Project: 'AzureCloudHub-AIML'
  CostCenter: costCenter
  ManagedBy: 'Bicep-IaC'
  Certification: 'AZ-900'
}

var uniqueSuffix = uniqueString(resourceGroup().id)
var storageAccountName = 'st${projectName}${uniqueSuffix}'
var appServicePlanName = 'asp-${projectName}-${environment}'
var appServiceName = 'app-${projectName}-${environment}-${uniqueSuffix}'
var logAnalyticsName = 'log-${projectName}-${environment}'
var appInsightsName = 'appi-${projectName}-${environment}'
var vnetName = 'vnet-${projectName}-${environment}'
var nsgName = 'nsg-${projectName}-${environment}'

// ------------------------------------------------------------------------------
// 1. Virtual Network & Network Security Group (Networking Domain)
// ------------------------------------------------------------------------------
resource nsg 'Microsoft.Network/networkSecurityGroups@2023-09-01' = {
  name: nsgName
  location: location
  tags: standardTags
  properties: {
    securityRules: [
      {
        name: 'Allow-HTTPS-Inbound'
        properties: {
          priority: 100
          access: 'Allow'
          direction: 'Inbound'
          protocol: 'Tcp'
          sourcePortRange: '*'
          destinationPortRange: '443'
          sourceAddressPrefix: 'Internet'
          destinationAddressPrefix: '*'
        }
      }
      {
        name: 'Deny-All-Other-Inbound'
        properties: {
          priority: 4096
          access: 'Deny'
          direction: 'Inbound'
          protocol: '*'
          sourcePortRange: '*'
          destinationPortRange: '*'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
        }
      }
    ]
  }
}

resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: vnetName
  location: location
  tags: standardTags
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'snet-appservice'
        properties: {
          addressPrefix: '10.0.1.0/24'
          networkSecurityGroup: {
            id: nsg.id
          }
          delegations: [
            {
              name: 'appServiceDelegation'
              properties: {
                serviceName: 'Microsoft.Web/serverFarms'
              }
            }
          ]
        }
      }
    ]
  }
}

// ------------------------------------------------------------------------------
// 2. Storage Account with Lifecycle Management (Storage Domain)
// ------------------------------------------------------------------------------
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  tags: standardTags
  sku: {
    name: 'Standard_ZRS' // Zone-Redundant Storage across 3 Availability Zones
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

resource modelContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'model-artifacts'
  properties: {
    publicAccess: 'None'
  }
}

// Automated Lifecycle Rule: Hot -> Cool (30d) -> Archive (90d)
resource storageLifecycle 'Microsoft.Storage/storageAccounts/managementPolicies@2023-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    policy: {
      rules: [
        {
          name: 'MoveArtifactsToCoolAndArchive'
          enabled: true
          type: 'Lifecycle'
          definition: {
            filters: {
              blobTypes: [
                'blockBlob'
              ]
              prefixMatch: [
                'model-artifacts/'
              ]
            }
            actions: {
              baseBlob: {
                tierToCool: {
                  daysAfterModificationGreaterThan: 30
                }
                tierToArchive: {
                  daysAfterModificationGreaterThan: 90
                }
              }
            }
          }
        }
      ]
    }
  }
}

// ------------------------------------------------------------------------------
// 3. Observability: Log Analytics & Application Insights (Monitoring Domain)
// ------------------------------------------------------------------------------
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  tags: standardTags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  tags: standardTags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
  }
}

// ------------------------------------------------------------------------------
// 4. Compute: App Service Linux Web App for Containers (Compute PaaS Domain)
// ------------------------------------------------------------------------------
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: appServicePlanName
  location: location
  tags: standardTags
  kind: 'linux'
  sku: {
    name: 'B1' // Basic Tier for cost efficiency, scalable to P1v3
    tier: 'Basic'
  }
  properties: {
    reserved: true // Required for Linux
  }
}

resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: appServiceName
  location: location
  tags: standardTags
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOCKER|ghcr.io/arighnasadhu/azurecloudhub:latest'
      appSettings: [
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'AZURE_REGION'
          value: location
        }
        {
          name: 'AZURE_ENVIRONMENT'
          value: environment
        }
        {
          name: 'STORAGE_ACCOUNT_NAME'
          value: storageAccount.name
        }
        {
          name: 'PORT'
          value: '8000'
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
      ]
    }
  }
}

// ------------------------------------------------------------------------------
// 5. Governance: Resource Lock (CanNotDelete safeguard)
// ------------------------------------------------------------------------------
resource deleteLock 'Microsoft.Authorization/locks@2020-05-01' = {
  name: 'lock-prevent-accidental-deletion'
  scope: appService
  properties: {
    level: 'CanNotDelete'
    notes: 'Resource lock to guard against accidental removal of production AI API'
  }
}

// ------------------------------------------------------------------------------
// Outputs
// ------------------------------------------------------------------------------
output appServiceEndpoint string = 'https://${appService.properties.defaultHostName}'
output storageAccountName string = storageAccount.name
output appInsightsConnectionString string = appInsights.properties.ConnectionString
output vnetId string = vnet.id
