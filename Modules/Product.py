import json
from DB_ops.database_ops import DataBaseOps
from fastapi import HTTPException


class ProductTable:

    @staticmethod
    async def get_all_products():
        try:
            cursor,conn = DataBaseOps.get_connection()

            cursor.execute("SELECT COUNT(*) FROM dbo.ProductTable")
            count = cursor.fetchone()[0]
            if count == 0:
                return {'success': False, 'message': "No products found", 'data': []}

            cursor.execute("""
                SELECT product_id, product_name, product_description,
                       price, stock_quantity, specifications, category_id
                FROM dbo.ProductTable
            """)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append({
                    'Product_Id': row.product_id,
                    'Product_Name': row.product_name,
                    'Product_Description': row.product_description,
                    'Price': row.price,
                    'Stock_Quantity': row.stock_quantity,
                    'Specifications': row.specifications,
                    'Category_Id': row.category_id
                })

            return {'success': True, 'message': "Products fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def add_product(product_name:int,product_description:str|None,price:float,stock_quantity:int,specifications:dict|None,category_id:int):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("""
                INSERT INTO dbo.ProductTable
                (product_name, product_description, price, stock_quantity, specifications, category_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                product_name,
                product_description,
                price,
                stock_quantity,
                json.dumps(specifications) if specifications else None,
                category_id
            ))
            conn.commit()
            return {'success': True, 'message': "Product added successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def get_product_by_category(category_id: int):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT product_id, product_name, product_description,
                       price, stock_quantity, specifications, category_id
                FROM dbo.ProductTable
                WHERE category_id = ?
            """, (category_id,))
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append({
                    'Product_Id': row.product_id,
                    'Product_Name': row.product_name,
                    'Product_Description': row.product_description,
                    'Price': row.price,
                    'Stock_Quantity': row.stock_quantity,
                    'Specifications': row.specifications,
                    'Category_Id': row.category_id
                })

            return {'success': True, 'message': "Products fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def get_product_by_id(product_id: int):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("""
                SELECT product_id, product_name, product_description,
                       price, stock_quantity, specifications, category_id
                FROM dbo.ProductTable
                WHERE product_id = ?
            """, (product_id,))
            row = cursor.fetchone()
            if not row:
                return {'success': False, 'message': "Product not found", 'data': {}}

            result = {
                'Product_Id': row.product_id,
                'Product_Name': row.product_name,
                'Product_Description': row.product_description,
                'Price': row.price,
                'Stock_Quantity': row.stock_quantity,
                'Specifications': row.specifications,
                'Category_Id': row.category_id
            }
            return {'success': True, 'message': "Product fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def delete_product(product_id: int):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("DELETE FROM dbo.ProductTable WHERE product_id = ?", (product_id,))
            conn.commit()
            return {'success': True, 'message': "Product deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def update_product(product_id:int,product_name:str,product_description:str|None,price:float,stock_quantity:int,specifications:dict|None):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("""
                UPDATE dbo.ProductTable
                SET product_name = ?, product_description = ?, price = ?,
                    stock_quantity = ?, specifications = ?
                WHERE product_id = ?
            """, (
                product_name,
                product_description,
                price,
                stock_quantity,
                json.dumps(specifications) if specifications else None,
                product_id
            ))
            conn.commit()
            return {'success': True, 'message': "Product updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)


