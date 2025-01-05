import azure.functions as func
import azure.durable_functions as df
import logging
from time import sleep 
from models import *

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@myApp.route(route="orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):    
    # Request an order
    order_payload = OrderPayload(
        order_name="milk", 
        total_cost=5, 
        quantity=1
    )  
    orchestrator_name = req.route_params['functionName']
    instance_id = await client.start_new(orchestrator_name, client_input=order_payload)
    
    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    response = client.create_check_status_response(req, instance_id)
    return response

@myApp.orchestration_trigger(context_name="context")
def process_orchestrator(context: df.DurableOrchestrationContext):   
    # Retry options for activity functions
    retry_interval_in_milliseconds = 2000
    max_number_of_attempts = 3
    retry_options = df.RetryOptions(retry_interval_in_milliseconds, max_number_of_attempts)
     
    # Reserve requested inventory 
    order_id = context.instance_id
    order_payload: OrderPayload = context.get_input()
    inventory_request = InventoryRequest(
        request_id=order_id, 
        item_name=order_payload.order_name,
        quantity=order_payload.quantity
    )
    
    inventory_result: InventoryResult = yield context.call_activity_with_retry("reserve_inventory", retry_options, inventory_request)   
    
    # There's not enough inventory, so fail and notify the customer
    if not inventory_result.success:
        notification = Notification(f"Insufficient inventory for {order_payload.order_name}.")
        yield context.call_activity("notify_customer", notification)
        context.set_custom_status("Insufficient inventory.")
        return OrderResult(processed=False).to_json() # Need to call to_json(), otherwise will error "object is not JSON serializable"
        
    # There is enough inventory, so process the payment 
    payment_request = PaymentRequest(
        request_id=order_id, 
        item_purchased=order_payload.order_name, 
        payment_amount=order_payload.total_cost, 
    )
    
    yield context.call_activity_with_retry("process_payment", retry_options, payment_request)
    
    try:
        # Update inventory
        yield context.call_activity_with_retry("update_inventory", retry_options, inventory_request)
    except Exception as e:
        logging.error(f"Error updating inventory: {e}")
        notification = Notification(f"Failed to process order for {order_payload.order_name}. You're now getting a refund.")
        yield context.call_activity("notify_customer", notification)
        context.set_custom_status("Failed to update inventory.")
        return OrderResult(processed=False).to_json()
    
    # Order placed successfully. Notify customer.
    notification = Notification(f"Order for {order_payload.order_name} placed successfully!")
    yield context.call_activity("notify_customer", notification)
    context.set_custom_status("Order placed successfully.")

    return OrderResult(processed=True).to_json()

@myApp.activity_trigger(input_name="req")
def reserve_inventory(req: InventoryRequest):
    logging.info(f"Reserving inventory for order {req.request_id} of quantity {req.quantity} {req.item_name}.")
    
    # In a real app, this would be a call to a database or external service to check inventory
    # For simplicity, we'll just return a successful result with a dummy OrderPayload
    sleep(5) # Dummy delay to simulate database call
            
    order_response = OrderPayload(
        order_name=req.item_name, 
        total_cost=5, 
        quantity=req.quantity
    )
    
    return InventoryResult(True, order_response)

@myApp.activity_trigger(input_name="req")
def update_inventory(req: InventoryRequest):
    logging.info(f"Update inventory for {req.item_name}.")
    
    # In a real app, this would be a call to a database or external service to update inventory
    # For simplicity, we pretend the inventory has been updated and log the new quantity
    sleep(5) # Dummy delay to simulate database call
        
    logging.info(f"Inventory updated for {req.item_name}. Current quantity: 100.")
    
    # Activity functions must return a value today
    return "Inventory updated."

@myApp.activity_trigger(input_name="notification")
def notify_customer(notification: Notification):
    logging.info(notification.message)
    
    # Simulate notification
    sleep(2) 
    
    # Activity functions must return a value today
    return "Notified customer."

@myApp.activity_trigger(input_name="req")
def process_payment(req: PaymentRequest):
    logging.info(f"Processing payment for order {req.request_id} purchasing {req.item_purchased} with {req.payment_amount} {req.currency}.")
    
    # Simulate slow payment processing
    sleep(7) 

    logging.info(f"Payment request {req.request_id} processed successfully.")
    
    # Activity functions must return a value today
    return "Payment processed."

