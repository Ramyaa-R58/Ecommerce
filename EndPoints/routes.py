from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from Dependencies.authValidation import create_user_token, get_current_login, check_admin
from Helpers.constants import *
from Models.responseModels import *
from DB_ops.database_ops import DatabaseOps
import bcrypt

from Modules.Category import CategoryClass

router_handle = APIRouter()

@router_handle.post("/login")
async def Login(user: LoginDetails):
    try:
        cursor,conn = DatabaseOps.get_connection()

        # Fetch user record
        cursor.execute("""
            SELECT u.user_id, u.full_name, u.password, r.role_name
            FROM dbo.UserTable u
            JOIN dbo.UserRoleTable ur ON u.user_id = ur.user_id
            JOIN dbo.RoleTable r ON ur.role_id = r.role_id
            WHERE u.email = ?
        """, (user.email,))
        row = cursor.fetchone()

        success = True
        message = "Login Successful"
        token = ''

        if not row:
            success = False
            message = "User not found"
        else:
            user_id, full_name, hashed_password, role_name = row
            check_password = bcrypt.checkpw(user.password.encode('utf-8'),
                                            hashed_password.encode('utf-8'))
            if not check_password:
                success = False
                message = "Incorrect Password"
            else:
                encoded_data = {'id': user_id, 'full_name': full_name, 'user_role': role_name}
                token = create_user_token(encoded_data)

        return JSONResponse({'success': success, 'message': message, 'token': token})
    except Exception as e:
        return JSONResponse({'success': False, 'message': str(e)})
    finally:
        DatabaseOps.disconnect_connection(cursor, conn)

# ---------------- REGISTER ----------------
@router_handle.post("/register")
async def Register(user: UserDetails):
    try:
        cursor,conn = DatabaseOps.get_connection()

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'),
                                        bcrypt.gensalt()).decode('utf-8')

        # Insert user
        cursor.execute("""
            INSERT INTO dbo.UserTable (full_name, email, password, phone_number)
            VALUES (?, ?, ?, ?)
        """, (user.full_name, user.email, hashed_password, user.phone_number))

        # Get generated user_id
        cursor.execute("SELECT user_id FROM dbo.UserTable WHERE email = ?", (user.email,))
        user_id = cursor.fetchone()[0]

        # Assign default role (customer = 2)
        cursor.execute("""
            INSERT INTO dbo.UserRoleTable (user_id, role_id)
            VALUES (?, ?)
        """, (user_id, 2))

        conn.commit()
        return JSONResponse({'success': True, 'message': "User Registered Successfully"})
    except Exception as e:
        return JSONResponse({'success': False, 'message': str(e)})
    finally:
        DatabaseOps.disconnect_connection(cursor, conn)

# ---------------- GET USER ROLE ----------------
@router_handle.get("/get_user_role")
async def get_all_user_role(current_login=Depends(get_current_login)):
    try:
        if current_login['user_role'] == 'admin':
            cursor,conn = DatabaseOps.get_connection()

            cursor.execute("""
                SELECT u.user_id, u.full_name, r.role_name
                FROM dbo.UserTable u
                JOIN dbo.UserRoleTable ur ON u.user_id = ur.user_id
                JOIN dbo.RoleTable r ON ur.role_id = r.role_id
            """)
            rows = cursor.fetchall()

            roles = []
            for row in rows:
                roles.append({
                    'User_Id': row.user_id,
                    'User_Name': row.full_name,
                    'Role_Name': row.role_name
                })

            return JSONResponse({'success': True, 'message': "Roles fetched successfully", 'data': roles})
    except Exception as e:
        return JSONResponse({'success': False, 'message': str(e)})
    finally:
        DatabaseOps.disconnect_connection(cursor, conn)

# ---------------- ASSIGN ROLE ----------------
@router_handle.post("/assign_role_to_user")
async def assign_role(user_role: UserRoleData, current_login=Depends(get_current_login)):
    try:
        if check_admin(current_login):
            cursor,conn = DatabaseOps.get_connection()

            role_id = ADMIN if user_role.role_name == 'admin' else CUSTOMER

            cursor.execute("""
                UPDATE dbo.UserRoleTable
                SET role_id = ?
                WHERE user_id = ?
            """, (role_id, user_role.user_id))

            conn.commit()
            return JSONResponse({'success': True, 'message': 'Role assigned successfully'})
    except Exception as e:
        return JSONResponse({'success': False, 'message': str(e)})
    finally:
        DatabaseOps.disconnect_connection(cursor, conn)






























@router_handle.post("/login")
async def Login(user:LoginDetails):
    try:
        success = True
        message = "Login Successful"
        token = ''
        user_record = UserTable.get_or_none(UserTable.email == user.email)
        check_password  = bcrypt.checkpw(user.password.encode('utf-8'),user_record.password.encode('utf-8'))
        if not user_record:
            success = True
            message = "User not found"
        elif check_password:
            success = False
            message = "Incorrect Password"
        else:
            user_role_data = user_record.user_roles[0].role_id.role_name
            encoded_data = {'id':user_record.user_id,'full_name':user_record.full_name,'user_role':user_role_data}
            token = create_user_token(encoded_data)
        return JSONResponse({'success':success,'message':message,'token':token})
    except Exception as e:
        return JSONResponse({'success':False,'message':str(e)})
@router_handle.post("/register")
async def Register(user:UserDetails):
    try:
        success=True
        message="User Registered Successfully"
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        user = UserTable(full_name=user.full_name,email=user.email,password=hashed_password,phone_number=user.phone_number)
        user.save()
        UserRoleTable.create(user_id=user.user_id,role_id=2)
        return JSONResponse({'success':success,'message':message})
    except Exception as e:
        return JSONResponse({'success':False,'message':str(e)})



@router_handle.get('/get_user_role')
async def get_all_user_role(current_login=Depends(get_current_login)):
   try:
       if current_login['user_role'] == 'admin':
             roles = []
             query = UserTable.select()
             for user_entry in query:
                 user_record = UserTable.get_or_none(UserTable.user_id == user_entry.user_id)
                 role_name = user_record.user_roles[0].role_id.role_name
                 roles.append({
                    'User_Id':user_entry.user_id,
                     'User_Name':user_entry.full_name,
                    'Role_Name':role_name
                  })
             return JSONResponse({'success':True,'message':"Roles fetched successfully",'data':roles})
   except Exception as e:
        return JSONResponse({'success':False,'message':str(e)})

@router_handle.post('/assign_role_to_user')
async def assign_role(user_role:UserRoleData,current_login=Depends(get_current_login)):
   try:
       if check_admin(current_login):
           if user_role.role_name == 'admin':
               role_id = ADMIN
           else:
               role_id = CUSTOMER
           UserRoleTable.update(role_id = role_id).where(UserRoleTable.user_id == user_role.user_id).execute()
           return JSONResponse({'success':True,'message':'Role assigned successfully'})
   except Exception as e:
       return JSONResponse({'success':False,'message':str(e)})

@router_handle.get('/get_categories')
async def get_categories(current_login=Depends(get_current_login)):
    try:
        if check_admin(current_login):
            result = await CategoryClass.get_all_categories()
            return JSONResponse(result)
    except Exception as e:
        return JSONResponse({'success':False,'message':str(e)})

# need to have route for order details - payment status etc.

@router_handle.post('/add_category')
async def add_category(category:CategoryDetails,current_login=Depends(get_current_login)):
    try:
        if check_admin(current_login):
            result = await CategoryClass.add_category(category.category_name,category.category_description)
            return JSONResponse(result)
    except Exception as e:
        return JSONResponse({'success':False,'message':str(e)})
@router_handle.delete('/delete_category/{category_id}')
async def delete_category(category_id:str,current_login=Depends(get_current_login)):
    try:
        if check_admin(current_login):
            result = await CategoryClass.delete_category(category_id)
            return JSONResponse(result)
    except Exception as e:
        return JSONResponse({'success':False,'message':str(e)})
@router_handle.put('/update_category')
async def update_category(category:CategoryDetails,current_login=Depends(get_current_login)):
    try:
        if check_admin(current_login):
            result = await CategoryClass.update_category(category.category_id,category.category_name,category.category_description)
            return JSONResponse(result)
    except Exception as e:
        return JSONResponse({'success':False,'message':str(e)})



