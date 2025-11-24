from fastapi import HTTPException


class ProductTable:
    @staticmethod
    async def get_all_products():
        try:
            if ProductTable.select().count() == 0:
                return {'success': False, 'message': "No products found", 'data': []}
            query = ProductTable.select()
            result = []
            for row in query:
                result.append({
                    'Product_Id': row.product_id,
                    'Product_Name': row.product_name,
                    'Product_Description': row.product_description,
                    'Price': row.price,
                    'Stock_Quantity': row.stock_quantity,
                    'Specifications': row.specifications,
                    'Category_Id': row.category_id.category_id
                })
            return {'success': True, 'message': "Products fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    @staticmethod
    async def add_product(product_name:str,product_description:str|None,price:float,stock_quantity:int,specifications:dict|None,category_id:str):
        try:
            product = ProductTable(product_name=product_name,product_description=product_description,price=price,stock_quantity=stock_quantity,specifications=specifications,category_id=category_id)
            product.save()
            return {'success': True, 'message': "Product added successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_product_by_category(category_id:str):
        try:
            query = ProductTable.select().where(ProductTable.category_id == category_id)
            result = []
            for row in query:
                result.append({
                    'Product_Id': row.product_id,
                    'Product_Name': row.product_name,
                    'Product_Description': row.product_description,
                    'Price': row.price,
                    'Stock_Quantity': row.stock_quantity,
                    'Specifications': row.specifications,
                    'Category_Id': row.category_id.category_id
                })
            return {'success': True, 'message': "Products fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    @staticmethod
    async def get_product_by_id(product_id:str):
        try:
            product = ProductTable.get(ProductTable.product_id == product_id)
            result = {
                'Product_Id': product.product_id,
                'Product_Name': product.product_name,
                'Product_Description': product.product_description,
                'Price': product.price,
                'Stock_Quantity': product.stock_quantity,
                'Specifications': product.specifications,
                'Category_Id': product.category_id
            }
            return {
                'success': True,
                'message': "Product fetched successfully",
                'data': result
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    @staticmethod
    async def delete_product(product_id:str):
        try:
            ProductTable.delete().where(ProductTable.product_id == product_id).execute()
            return {'success': True, 'message': "Product deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_product(product_id:str,product_name:str,product_description:str|None,price:float,stock_quantity:int,specifications:dict|None):
        try:
            product = ProductTable.get(ProductTable.product_id == product_id)
            product.product_name = product_name
            product.product_description = product_description
            product.price = price
            product.stock_quantity = stock_quantity
            product.specifications = specifications
            product.save()
            return {'success': True, 'message': "Product updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))