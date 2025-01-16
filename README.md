<!--
---
description: This end-to-end sample shows how implement an order processing workflow using Durable Functions in Python. 
page_type: sample
products:
- azure-functions
- azure
urlFragment: durable-func-order-processing-py
languages:
- python
- bicep
- azdeveloper
---
-->

# Order processing workflow with Durable Functions (Python)

[Durable Functions](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview) is part of [Azure Functions](https://learn.microsoft.com/azure/azure-functions/functions-overview) offering. Durable Functions helps you easily orchestrate stateful logic, making it an excellent solution for workflow scenarios, as well as stateful patterns like fan-out/fan-in and workloads that require long-running operations or need to wait arbitrarily long for external events. 

This sample shows how to implement an order processing workflow with Durable Functions in Python 3.11. The sample leverages the [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows) and [Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/overview?tabs=bicep) to simplify the provisioning and deployment of all resources required by the app. 

Durable Functions needs a [storage backend provider](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-storage-providers) to persist application states. This sample uses the default backend, which is Azure Storage.  

> [!IMPORTANT]
> This sample creates several resources. Make sure to delete the resource group after testing to minimize charges!

## Run in your local environment

The project is designed to run on your local computer, provided you have met the [required prerequisites](#prerequisites). You can run the project locally in these environments:

+ [Using Azure Functions Core Tools (CLI)](#using-azure-functions-core-tools-cli)
+ [Using Visual Studio Code](#using-visual-studio-code)

### Prerequisites

+ [Python 3.11](https://www.python.org/downloads/) 
+ [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools)
+ Start Azurite storage emulator. See [this page](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) for how to configure and start the Azurite emulator for Local Storage.
+ Clone the repo, then create a file named `local.settings.json` with the following content in the **order_processor** directory:

  ```json
  {
    "IsEncrypted": false,
    "Values": {
      "AzureWebJobsStorage": "UseDevelopmentStorage=true",
      "FUNCTIONS_WORKER_RUNTIME": "python"
    }
  }
  ```

### Using Azure Functions Core Tools (CLI)
Make sure Azurite is started before proceeding.

1. Open the cloned repo in a new terminal and navigate to the `order_processor` directory: 
```bash
cd order_processor
```

2. Create and activate the virtual environment:
```bash
python3 -m venv venv_name
```
```bash
source .venv/bin/activate
```

3. Install required packages:
```bash
python3 -m pip install -r requirements.txt
```

4. Start function app 
```bash
func start
```

5. This sample uses an HTTP trigger to start an orchestration, so open a browser and go to http://localhost:7071/api/orchestrators/process_orchestrator. You should see something similar to the following: 

```json
{
    "id": "e838bdb52db24560a6b30c261ac2985d",
    "purgeHistoryDeleteUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/e838bdb52db24560a6b30c261ac2985d?code=<code>",
    "sendEventPostUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/e838bdb52db24560a6b30c261ac2985d/raiseEvent/{eventName}?code=<code>",
    "statusQueryGetUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/e838bdb52db24560a6b30c261ac2985d?code=<code>",
    "terminatePostUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/e838bdb52db24560a6b30c261ac2985d/terminate?reason={{text}}}&code=<code>"
}
```

6. To check the status of the orchestration instance started, go to the `statusQueryGetUri`. Your orchestration instance should show status "Running". After a few seconds, refresh to see that the orchestration instance is "Completed" and what the output is.

```json
{
    "name": "process_orchestrator",
    "instanceId": "5ddc571338594942a5051903e4a50656",
    "runtimeStatus": "Completed",
    "input": "{\"__class__\": \"OrderPayload\", \"__module__\": \"models\", \"__data__\": \"{\\\"order_name\\\": \\\"milk\\\", \\\"total_cost\\\": 5, \\\"quantity\\\": 1}\"}",
    "customStatus": "Order placed successfully.",
    "output": {
        "success": true
    },
    "createdTime": "2025-01-15T01:41:18Z",
    "lastUpdatedTime": "2025-01-15T01:41:39Z"
}
```

### Using Visual Studio Code

1) Open the *order_processor* folder in a new terminal
2) Open VS Code by entering `code .` in the terminal
3) Start Azurite by opening the command template and searching for `Azurite: Start`
4) Press Run/Debug (F5) to run in the debugger
5) Use same approach above to start an orchestration instance and check its status. 


## Provision the solution on Azure

In the root folder (**durable-functions-order-processing-python**) use the [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows) to provision a new resource group with the environment name you provide and all the resources for the sample by running:

```bash
azd up
``` 

## Inspect the solution (optional)

Once the deployment is done, inspect the new resource group. The Durable Functions app, Flex Consumption hosting plan, Azure Storage account, App Insights, managed identity, and various networking related resources have been created and configured.

Because Durable Functions requires access to Azure Storage Blob, Table, and Queue, the associated networking resources such as private endpoints, link, etc. are created for each of those. The managed identity assigned to the app is also given the [required role-based access control (RBAC) permissions](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-configure-managed-identity#assign-access-roles-to-the-managed-identity).

Following guidance for [hosting Durable Functions apps in the Flex Consumption plan](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-azure-storage-provider#flex-consumption-plan), this sample sets the plan's *always ready* instance to 1 and the property `maxQueuePollingInterval` to 1 second. 

## Test the solution

1. Use this Function CLI command to quickly find the function app url:

    ```bash
    func azure functionapp list-functions <APP_NAME> --show-keys
    ````
    
    The url should look something like this: https://func-processor-abcdefgxzy.azurewebsites.net/api/orchestrators/process_orchestrator. 

Or you can find the app url on Azure portal. 

2. Open up a browser and go that url to trigger the start of an orchestration instance. 

3. Go to the `statusQueryGetUri` to see the status of your orchestration instance. It should show "Running" (or "Pending" then "Running") and change to "Completed" after a few seconds if you refresh the page. The result should be similar to [above](#using-azure-functions-core-tools-cli). 

## Clean up resources

When you no longer need the resources created in this sample, run the following command to delete the Azure resources:

```bash
azd down
```

## Resources

For more information on Durable Functions or the new Flex Consumption plan, see the following resources:

* [Durable Functions](https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview)
* [Azure Functions Flex Consumption documentation](https://learn.microsoft.com/azure/azure-functions/flex-consumption-plan)
