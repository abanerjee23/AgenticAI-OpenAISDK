import re

AUTO_REFUND_LIMIT = 1000

class DataBase:
    def __init__(self):
        self.orders = {
            'order_101': {'order_value': 200, 'order_status': 'received', 'customer_email': 'luke@gmail.com'},
            'order_102': {'order_value': 2000, 'order_status': 'under_review', 'customer_email': 'mark@gmail.com'},
            'order_103': {'order_value': 20, 'order_status': 'processed', 'customer_email': 'alice@hotmail.com'},
            'order_104': {'order_value': 20000, 'order_status': 'under_review', 'customer_email': 'liz@gmail.com'},
            'order_105': {'order_value': 150, 'order_status': 'received', 'customer_email': 'sam@yahoo.com'},
        }

    def _normalize_order_id(self, order_id):
        match = re.search(r'\d+', str(order_id))
        return f"order_{match.group()}" if match else str(order_id)

    def _get_order(self, order_id):
        if not order_id:
            raise ValueError("Valid order_id must be provided!")
        order = self.orders.get(order_id) or self.orders.get(self._normalize_order_id(order_id))
        if order is None:
            raise KeyError(f"No order found with id: {order_id}")
        return order

    def get_order_status(self, order_id):
        return self._get_order(order_id)['order_status']

    def get_order_value(self, order_id):
        return f"${self._get_order(order_id)['order_value']}"

    def process_refund(self, order_id, customer_email):
        order = self._get_order(order_id)
        if order['customer_email'] != customer_email:
            raise PermissionError(f"Order {order_id} does not belong to this customer.")
        if order['order_status'] == 'processed':
            raise ValueError(f"Refund for {order_id} has already been processed.")
        if order['order_status'] == 'under_review':
            raise ValueError(f"Order {order_id} is under FinOps review and cannot be auto-refunded.")
        if order['order_value'] > AUTO_REFUND_LIMIT:
            order['order_status'] = 'under_review'
            raise ValueError(
                f"Order {order_id} exceeds the ${AUTO_REFUND_LIMIT} auto-refund limit "
                "and has been escalated to FinOps for human review."
            )
        order['order_status'] = 'processed'
        return order['order_status']
