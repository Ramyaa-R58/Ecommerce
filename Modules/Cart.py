from datetime import datetime
from typing import List

from fastapi import HTTPException

from Helpers.constants import *
from Models.responseModels import CartProductDetails
from DB_ops.database_ops import DataBaseOps

class Cart:

    @staticmethod
    async def add_cart(cart_details:CartProductDetails, user_id: int):
        try:
            cursor, conn = DataBaseOps.get_connection()
            cursor.execute("""
                INSERT INTO dbo.CartTable (user_id, product_id, quantity, cart_status_id)
                VALUES (?, ?, ?, ?)
            """, (user_id, cart_details.product_id, cart_details.quantity, 'PENDING'))
            conn.commit()
            return {'success': True, 'message': "Product added to cart successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def remove_cart(product_id: str, user_id: int):
        try:
            cursor, conn = DataBaseOps.get_connection()
            cursor.execute("""
                DELETE FROM dbo.CartTable
                WHERE user_id = ? AND product_id = ?
            """, (user_id, product_id))
            conn.commit()
            return {'success': True, 'message': "Product removed from cart successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def checkout_items(user_id: int, product_details: list):
        try:
            cursor, conn = DataBaseOps.get_connection()
            total_amount = 0
            product_data = []

            for product in product_details:
                cursor.execute("SELECT product_name, price FROM dbo.ProductTable WHERE product_id = ?", (product.product_id,))
                row = cursor.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Product not found")

                product_name, price = row
                product_data.append({'Product Name': product_name, 'Quantity': product.quantity})
                total_amount += price * product.quantity

            # Insert order
            cursor.execute("""
                INSERT INTO dbo.OrderTable (user_id, order_status_id, order_date, total_amount)
                OUTPUT INSERTED.order_id
                VALUES (?, ?, ?, ?)
            """, (user_id, 'INITIATED', datetime.now(), total_amount))
            order_id = cursor.fetchone()[0]

            # Update cart + insert order products
            for item in product_details:
                cursor.execute("""
                    UPDATE dbo.CartTable
                    SET cart_status_id = ?
                    WHERE user_id = ? AND product_id = ?
                """, ('CHECKOUT', user_id, item.product_id))

                cursor.execute("""
                    INSERT INTO dbo.OrderProductTable (order_id, product_id, quantity, user_id)
                    VALUES (?, ?, ?, ?)
                """, (order_id, item.product_id, item.quantity, user_id))

            conn.commit()
            return {
                'success': True,
                'message': "Checkout completed successfully",
                'data': {
                    'Order_Id': order_id,
                    'Total_Amount': total_amount,
                    'product_details': product_data
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def get_cart_by_user(user_id: int):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("""
                SELECT c.cart_id, p.product_name, c.quantity
                FROM dbo.CartTable c
                JOIN dbo.ProductTable p ON c.product_id = p.product_id
                WHERE c.user_id = ?
            """, (user_id,))
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append({
                    'Cart_Id': row.cart_id,
                    'Product_Name': row.product_name,
                    'Quantity': row.quantity
                })

            return {'success': True, 'message': "Cart fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    # @staticmethod
    # async def add_cart(cart_details:CartProductDetails,user_id:str):
    #     try:
    #        CartTable.create(
    #            user_id=user_id,
    #            product_id=cart_details.product_id,
    #            quantity=cart_details.quantity,
    #            cart_status_id=PENDING
    #        )
    #        return {'success': True, 'message': "Product added to cart successfully"}
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
    # @staticmethod
    # async def remove_cart(product_id:str,user_id:str):
    #     try:
    #         CartTable.delete().where((CartTable.user_id == user_id) &(CartTable.product_id == product_id)).execute()
    #         return {'success': True, 'message': "Product removed from cart successfully"}
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))

    # @staticmethod
    # async def checkout_items(user_id:str,product_details:List[CartProductDetails]):
    #     try:
    #         total_amount = 0
    #         product_data = []
    #         for product in product_details:
    #            product_value = ProductTable.get(ProductTable.product_id == product.product_id)

    #            product_data.append({
    #                'Product Name':product_value.product_name,
    #                'Quantity':product.quantity,
    #            })
    #            amount = product_value.price * product.quantity
    #            total_amount = total_amount + amount
    #         order = OrderTable(user_id=user_id,order_status_id=INITAITED,order_date=datetime.now(),total_amount=total_amount)
    #         order.save()
    #         for item in product_details:
    #             cart_item = CartTable.get((CartTable.user_id == user_id) & (CartTable.product_id == item.product_id))
    #             cart_item.cart_status_id = CHECKOUT
    #             cart_item.save()
    #             order_product = OrderProductTable(order_id=order.order_id,product_id=item.product_id,quantity=item.quantity,user_id=user_id)
    #             order_product.save()
    #             # need to add product details also
    #         return {'success': True, 'message': "Checkout completed successfully",'data':{'Order_Id':order.order_id,'Total_Amount':total_amount,'product_details':product_data}}
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
    # @staticmethod
    # async def get_cart_by_user(user_id:str):
    #     try:
    #         query = CartTable.select().where(CartTable.user_id == user_id)
    #         user = UserTable.get(UserTable.user_id == user_id)
    #         result = []
    #         for row in query:
    #             product_name = user.user_id.user_carts[0].product_id.product_name
    #             result.append({
    #                 'Cart_Id': row.cart_id,
    #                 'Product_Name': product_name,
    #                 'Quantity': row.quantity,
    #             })
    #         return {'success': True, 'message': "Cart fetched successfully", 'data': result}
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))

