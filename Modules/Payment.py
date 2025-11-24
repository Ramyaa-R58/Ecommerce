from fastapi import HTTPException
from Helpers.constants import *
from Models.dataBaseModels import *
from Models.responseModels import PaymentDetails


class PaymemtTable:
    @staticmethod
    async def payment_action(payment_details:PaymentDetails,user_id:str):
        try:
            if payment_details.payment_status == "completed":
                message = "Payment completed successfully"
                payment = PaymentTable(
                    user_id=user_id,
                    order_id=payment_details.order_id,
                    payment_status_id=COMPLETED,
                )
                payment.save()
                order = OrderTable.get(OrderTable.order_id == payment_details.order_id)
                #clear cart
                order_product_info = OrderProductTable.get((OrderProductTable.order_id == payment_details.order_id) & (OrderProductTable.user_id == user_id))
                for product in order_product_info:
                    CartTable.delete().where((CartTable.user_id == user_id) & (CartTable.product_id == product.product_id)).execute()
                order.order_status_id = PAYMENTDONE
                order.save()
            else:
                payment = PaymentTable(
                    user_id=user_id,
                    order_id=payment_details.order_id,
                    payment_status_id=FAILED,
                )
                payment.save()

            return {'success': True, 'message': message}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))