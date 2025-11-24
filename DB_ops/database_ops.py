from Models.dataBaseModels import *

class DataBaseOps:
    @staticmethod
    def insert_table_data(table_name_data:dict):
        for table_name,data in table_name_data.items():
            if table_name.select().count() == 0:
                table_name.insert_many(data).execute()
    @staticmethod
    def create_tables():

        tables = [UserTable,RoleTable,UserRoleTable,AddressTable,
                  CategoryTable,ProductTable,OrderStatusTable,
                  CartStatusTable,PaymentStatusTable,OrderTable,
                  OrderProductTable,CartTable]
        db.create_tables(tables,safe=True)
        table_data = {
            RoleTable:[
                {'role_name':'admin'},
                {'role_name':'customer'}
            ],
            OrderStatusTable:[
                {'order_status_name':'initiated'},
                {'order_status_name':'paymentdone'},
            ],
            CartStatusTable:[
                {'cart_status_name':'pending'},
                {'cart_status_name':'checkout'},
            ],
            PaymentStatusTable:[
                {'payment_status_name':'completed'},
                {'payment_status_name':'failed'}
            ]
        }
        DataBaseOps.insert_table_data(table_data)
