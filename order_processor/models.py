import json

class OrderPayload:
    def __init__(self, order_name, total_cost, quantity=1):
        self.order_name = order_name
        self.total_cost = total_cost
        self.quantity = quantity
    
    @staticmethod
    def to_json(self):
        return json.dumps({
            "order_name": self.order_name,
            "total_cost": self.total_cost,
            "quantity": self.quantity
        })
    
    @staticmethod
    def from_json(json_string):
        json_dict = json.loads(json_string)
        return OrderPayload(
            order_name = json_dict.get("order_name"),
            total_cost = json_dict.get("total_cost"),
            quantity = json_dict.get("quantity")
        )

class InventoryRequest:
    def __init__(self, request_id, item_name, quantity):
        self.request_id = request_id
        self.item_name = item_name
        self.quantity = quantity
        
    @staticmethod
    def to_json(self):
        return json.dumps({
            "request_id": self.request_id,
            "item_name": self.item_name,
            "quantity": self.quantity
        })
    
    @staticmethod
    def from_json(json_string):
        json_dict = json.loads(json_string)
        return InventoryRequest(
            request_id = json_dict.get("request_id"),
            item_name = json_dict.get("item_name"),
            quantity = json_dict.get("quantity")
        )
        
class PaymentRequest:
    def __init__(self, request_id, item_purchased, payment_amount, currency="USD"):
        self.request_id = request_id
        self.item_purchased = item_purchased
        self.payment_amount = payment_amount
        self.currency = currency
        
    @staticmethod
    def to_json(self):
        return json.dumps({
            "request_id": self.request_id,
            "item_purchased": self.item_purchased,
            "payment_amount": self.payment_amount,
            "currency": self.currency
        })
    
    @staticmethod
    def from_json(json_string):
        json_dict = json.loads(json_string)
        return PaymentRequest(
            request_id = json_dict.get("request_id"),
            item_purchased = json_dict.get("item_purchased"),
            payment_amount = json_dict.get("payment_amount"),
            currency = json_dict.get("currency")
        )
        
class Notification:
    def __init__(self, message):
        self.message = message
        
    @staticmethod
    def to_json(self):
        return json.dumps({ 
            "message": self.message
        })
    
    @staticmethod
    def from_json(json_string):
        json_dict = json.loads(json_string)
        return Notification(
            message = json_dict.get("message")
        )
        


