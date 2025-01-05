class OrderPayload:
    def __init__(self, order_name, total_cost, quantity=1):
        self.order_name = order_name
        self.total_cost = total_cost
        self.quantity = quantity
    
    def to_json(self):
        return {
            "order_name": self.order_name,
            "total_cost": self.total_cost,
            "quantity": self.quantity
        }
    
    @classmethod
    def from_json(cls, json_dict):
        return cls(
            order_name = json_dict.get("order_name"),
            total_cost = json_dict.get("total_cost"),
            quantity = json_dict.get("quantity")
        )

class InventoryRequest:
    def __init__(self, request_id, item_name, quantity):
        self.request_id = request_id
        self.item_name = item_name
        self.quantity = quantity
        
    def to_json(self):
        return {
            "request_id": self.request_id,
            "item_name": self.item_name,
            "quantity": self.quantity
        }
    
    @classmethod
    def from_json(cls, json_dict):
        return cls(
            request_id = json_dict.get("request_id"),
            item_name = json_dict.get("item_name"),
            quantity = json_dict.get("quantity")
        )
        
class InventoryResult:
    def __init__(self, success, order_payload):
        self.success = success
        self.order_payload = order_payload
        
    def to_json(self):
        return {
            "success": self.success,
            "order_payload": self.order_payload
        }
    
    @classmethod
    def from_json(cls, json_dict):
        return cls(
            success = json_dict.get("success"),
            order_payload = json_dict.get("order_payload")
        )
        
class PaymentRequest:
    def __init__(self, request_id, item_purchased, payment_amount, currency="USD"):
        self.request_id = request_id
        self.item_purchased = item_purchased
        self.payment_amount = payment_amount
        self.currency = currency
        
    def to_json(self):
        return {
            "request_id": self.request_id,
            "item_purchased": self.item_purchased,
            "payment_amount": self.payment_amount,
            "currency": self.currency
        }
    
    @classmethod
    def from_json(cls, json_dict):
        return cls(
            request_id = json_dict.get("request_id"),
            item_purchased = json_dict.get("item_purchased"),
            payment_amount = json_dict.get("payment_amount"),
            currency = json_dict.get("currency")
        )

class OrderResult: 
    def __init__(self, processed):
        self.processed = processed
    
    def to_json(self):
        return {
            "processed": self.processed
        }
    
    @classmethod
    def from_json(cls, json_dict):
        return cls(
            processed = json_dict.get("processed")
        )
        
class InventoryItem:
    def __init__(self, name, total_cost, quantity):
        self.name = name
        self.total_cost = total_cost
        self.quantity = quantity 

class Notification:
    def __init__(self, message):
        self.message = message
    
    def to_json(self):
        return { 
            "message": self.message
        }
    
    @classmethod
    def from_json(cls, json_dict):
        return cls(
            message = json_dict.get("message")
        )
        


