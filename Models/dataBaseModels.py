from playhouse.sqlite_ext import JSONField
from peewee import *
db = SqliteDatabase('Eshop.db')
class BaseModel(Model):
    class Meta:
        database = db

class UserTable(BaseModel):
    user_id = CharField(unique=True,null=False)
    full_name = CharField(null=False)
    email = CharField(unique=True,null=False)
    password = CharField(null=False)
    phone_number = CharField(null=False)
    def save(self, *args,**kwargs):
        if not self.user_id:
            last_user = UserTable.select().order_by(UserTable.user_id.desc()).first()
            id_int_value = int(last_user.user_id.replace("ESUID","")) + 1 if last_user else 1
            self.user_id = f"ESUID{id_int_value}"
        super().save(*args,**kwargs)
class RoleTable(BaseModel):
    role_id = AutoField()
    role_name = CharField(unique=True,null=False)
class UserRoleTable(BaseModel):
    user_role_id = AutoField()
    user_id = ForeignKeyField(UserTable,to_field=UserTable.user_id,backref='user_roles',field='user_id')
    role_id = ForeignKeyField(RoleTable,to_field=RoleTable.role_id,backref='role_users',field='role_id')
class AddressTable(BaseModel):
    address_id = AutoField()
    user_id = ForeignKeyField(UserTable,to_field=UserTable.user_id,backref='user_addresses',field='user_id')
    address_line1 = TextField(null=False)
    address_line2 = TextField(null=True)
class CategoryTable(BaseModel):
    category_id = CharField(unique=True,null=False)
    category_name = CharField(unique=True,null=False)
    category_description = TextField(null=True)
    def save(self,*args,**kwargs):
        if not self.category_id:
            last_category = CategoryTable.select().order_by(CategoryTable.category_id.desc()).first()
            id_int_value = int(last_category.replace("ESCID","")) + 1 if last_category else 1
            self.category_id = f"ESCID{id_int_value}"
        super().save(*args,**kwargs)
class ProductTable(BaseModel):
    product_id = CharField(unique=True,null=False)
    product_name = CharField(unique=True,null=False)
    product_description = TextField(null=True)
    price = FloatField(null=False)
    stock_quantity = IntegerField(null=False)
    specifications = JSONField(null=True)
    category_id = ForeignKeyField(CategoryTable,to_field=CategoryTable.category_id,backref='category_products',field='category_id')
    def save(self, *args,**kwargs):
        if not self.product_id:
            last_product = ProductTable.select().order_by(ProductTable.product_id.desc()).first()
            id_int_value = int(last_product.replace("ESPID","")) + 1 if last_product else 1
            self.product_id = f"ESPID{id_int_value}"
        super().save(*args,**kwargs)

class OrderStatusTable(BaseModel):
    order_status_id = AutoField()
    order_status_name = CharField(unique=True,null=False)
class CartStatusTable(BaseModel):
    cart_status_id = AutoField()
    cart_status_name = CharField(unique=True,null=False)
class PaymentStatusTable(BaseModel):
    payment_status_id = AutoField()
    payment_status_name = CharField(unique=True,null=False)
class OrderTable(BaseModel):
    order_id = CharField(unique=True,null=False)
    user_id = ForeignKeyField(UserTable,to_field=UserTable.user_id,backref='user_orders',field='user_id')
    order_date = DateTimeField(null=False)
    order_status_id = ForeignKeyField(OrderStatusTable,to_field=OrderStatusTable.order_status_id,backref='status_orders',field='order_status_id')
    total_amount = FloatField(null=False)

class OrderProductTable(BaseModel):
    order_product_id = AutoField()
    order_id = ForeignKeyField(OrderTable,to_field=OrderTable.order_id,backref='order_products',field='order_id')
    product_id = ForeignKeyField(ProductTable,to_field=ProductTable.product_id,backref='product_orders',field='product_id')
    quantity = IntegerField(null=False)
class CartTable(BaseModel):
    cart_id = AutoField()
    user_id = ForeignKeyField(UserTable,to_field=UserTable.user_id,backref='user_carts',field='user_id')
    cart_status_id = ForeignKeyField(CartStatusTable,to_field=CartStatusTable.cart_status_id,backref='status_carts',field='cart_status_id')
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    product_id = ForeignKeyField(ProductTable,to_field=ProductTable.product_id,backref='product_carts',field='product_id')
    quantity = IntegerField(null=False)
class PaymentTable(BaseModel):
    payment_id = AutoField()
    user_id = ForeignKeyField(UserTable,to_field=UserTable.user_id,backref='user_payments',field='user_id')
    order_id = ForeignKeyField(OrderTable,to_field=OrderTable.order_id,backref='order_payments',field='order_id')
    payment_status_id = ForeignKeyField(PaymentStatusTable,to_field=PaymentStatusTable.payment_status_id,backref='status_payments',field='payment_status_id')
