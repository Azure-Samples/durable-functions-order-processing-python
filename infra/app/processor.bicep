param name string
param location string = resourceGroup().location
param tags object = {}
param applicationInsightsName string = ''
param appServicePlanId string
param appSettings object = {}
param runtimeName string 
param runtimeVersion string 
param serviceName string = 'processor'
param storageAccountName string
param virtualNetworkSubnetId string = ''
param instanceMemoryMB int = 2048
param maximumInstanceCount int = 100
param identityId string = ''
param identityClientId string = ''
param dtsURL string = ''
param taskHubName string = ''

var applicationInsightsIdentity = 'ClientId=${identityClientId};Authorization=AAD'

// Durable Task Scheduler settings
var dtsSettings = !empty(dtsURL) ? {
  DURABLE_TASK_SCHEDULER_CONNECTION_STRING: 'Endpoint=${dtsURL};Authentication=ManagedIdentity;ClientID=${identityClientId}'
  TASKHUB_NAME: taskHubName
} : {}

module processor '../core/host/functions-flexconsumption.bicep' = {
  name: '${serviceName}-functions-module'
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    identityType: 'UserAssigned'
    identityId: identityId
    appSettings: union(appSettings,
      {
        AzureWebJobsStorage__clientId : identityClientId
        APPLICATIONINSIGHTS_AUTHENTICATION_STRING: applicationInsightsIdentity
      },
      dtsSettings)
    applicationInsightsName: applicationInsightsName
    appServicePlanId: appServicePlanId
    runtimeName: runtimeName
    runtimeVersion: runtimeVersion
    storageAccountName: storageAccountName
    virtualNetworkSubnetId: virtualNetworkSubnetId
    instanceMemoryMB: instanceMemoryMB 
    maximumInstanceCount: maximumInstanceCount
  }
}

output SERVICE_PROCESSOR_NAME string = processor.outputs.name
output SERVICE_API_IDENTITY_PRINCIPAL_ID string = processor.outputs.identityPrincipalId
