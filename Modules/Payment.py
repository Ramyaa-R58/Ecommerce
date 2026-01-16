from fastapi import HTTPException
from Helpers.constants import *
from DB_ops.database_ops import DataBaseOps
from Models.responseModels import PaymentDetails


class PaymemtTable:
    @staticmethod
    async def payment_action(payment_details:PaymentDetails,user_id:str):
        try:
            if payment_details.payment_status == "completed":
                message = "Payment completed successfully"
                cursor,conn = DataBaseOps.get_connection()
                cursor.execute("""
                               INSERT INTO dbo.PaymentTable(user_id, order_id, payment_status_id)
                                 VALUES (?, ?, ?) """,(user_id, payment_details.order_id, COMPLETED))
                
                
                #clear cart
                order_product_info = OrderProductTable.get((OrderProductTable.order_id == payment_details.order_id) & (OrderProductTable.user_id == user_id))
                cursor.execute("""SELECT * FROM dbo.OrderProductTable WHERE order_id = ? AND user_id = ? """, (payment_details.order_id, user_id))
                order_product_info = cursor.fetchall()
                for product in order_product_info:
                    cursor.execute(""" DELETE FROM dbo.CartTable WHERE user_id = ? AND product_id = ? """, (user_id, product.product_id))
                cursor.execute("""
                               UPDATE dbo.OrderTable
                               SET order_status_id = ?
                               WHERE order_id = ?""", (PAYMENTDONE, payment_details.order_id))
                conn.commit()
                
            else:
                message = "Payment failed"
                cursor.execute("""
                               UPDATE dbo.OrderTable
                               SET order_status_id = ?
                               WHERE order_id = ?""", (PAYMENTFAILED, payment_details.order_id))
                conn.commit()

            return {'success': True, 'message': message}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)