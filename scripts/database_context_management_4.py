class Database:
    def get_order(self,order_id):
        return {
            'order_id':order_id,
            'pizza':'pepperoni',
            'status':'out for delivery'
        }
