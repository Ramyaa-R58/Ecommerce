from fastapi import HTTPException

from Models.dataBaseModels import CategoryTable, ProductTable


class Category:
    @staticmethod
    async def get_all_categories():
        try:
            if CategoryTable.select().count() == 0:
                return {'success': False, 'message': "No categories found", 'data': []}
            query = CategoryTable.select()
            result = []
            for row in query:
                result.append({
                    'Category_Id': row.category_id,
                    'Category_Name': row.category_name,
                    'Category_Description': row.category_description
                })
            return {'success': True, 'message': "Categories fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def add_category(category_name: str, category_description: str | None = None):
        try:
            category = CategoryTable(category_name=category_name, category_description=category_description)
            category.save()
            return {'success': True, 'message': "Category added successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_category_by_id(category_id:str):
        try:
            category = CategoryTable.get(CategoryTable.category_id == category_id)
            result = {'Category_Id':category.category_id,'Category_Name':category.category_name,'Category_Description':category.category_description}
            return {
                'success': True,
                'message': "Category fetched successfully",
                'data':result
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    @staticmethod
    async def delete_category(category_id:str):
        try:
            CategoryTable.delete().where(CategoryTable.category_id == category_id).execute()
            if ProductTable.select().where(ProductTable.category_id == category_id).count() > 0:
                ProductTable.delete().where(ProductTable.category_id == category_id).execute()
            return {'success': True, 'message': "Category deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    @staticmethod
    async def update_category(category_id:str,category_name:str,category_description:str|None=None):
        try:
            category = CategoryTable.get(CategoryTable.category_id == category_id)
            category.category_name = category_name
            category.category_description = category_description
            category.save()
            return {'success': True, 'message': "Category updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


