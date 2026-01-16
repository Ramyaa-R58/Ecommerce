from fastapi import HTTPException

from DB_ops.database_ops import DataBaseOps


class CategoryClass:
    @staticmethod
    async def get_all_categories():
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("SELECT COUNT(*) FROM dbo.CategoryTable")
            count = cursor.fetchone()[0]
            if count == 0:
                return {'success': False, 'message': "No categories found", 'data': []}

            cursor.execute("SELECT category_id, category_name, category_description FROM dbo.CategoryTable")
            conn.commit()
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append({
                    'Category_Id': row.category_id,
                    'Category_Name': row.category_name,
                    'Category_Description': row.category_description
                })

            return {'success': True, 'message': "Categories fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor,conn)

    @staticmethod
    async def add_category(category_name: str, category_description: str | None = None):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("""
                    INSERT INTO dbo.CategoryTable (category_name, category_description)
                    VALUES (?, ?)
                """, (category_name, category_description))
            conn.commit()
            return {'success': True, 'message': "Category added successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def get_category_by_id(category_id: int):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("""
                    SELECT category_id, category_name, category_description
                    FROM dbo.CategoryTable
                    WHERE category_id = ?
                """, (category_id,))
            conn.commit()
            row = cursor.fetchone()
            if not row:
                return {'success': False, 'message': "Category not found", 'data': {}}

            result = {
                'Category_Id': row.category_id,
                'Category_Name': row.category_name,
                'Category_Description': row.category_description
            }
            return {'success': True, 'message': "Category fetched successfully", 'data': result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def delete_category(category_id: int):
        try:
            cursor,conn = DataBaseOps.get_connection()

            # Delete category
            cursor.execute("DELETE FROM dbo.CategoryTable WHERE category_id = ?", (category_id,))

            # Delete products under that category if any
            cursor.execute("SELECT COUNT(*) FROM dbo.ProductTable WHERE category_id = ?", (category_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.execute("DELETE FROM dbo.ProductTable WHERE category_id = ?", (category_id,))

            conn.commit()
            return {'success': True, 'message': "Category deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)

    @staticmethod
    async def update_category(category_id: int, category_name: str, category_description: str | None = None):
        try:
            cursor,conn = DataBaseOps.get_connection()
            cursor.execute("""
                    UPDATE dbo.CategoryTable
                    SET category_name = ?, category_description = ?
                    WHERE category_id = ?
                """, (category_name, category_description, category_id))
            conn.commit()
            return {'success': True, 'message': "Category updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            DataBaseOps.disconnect_connection(cursor, conn)