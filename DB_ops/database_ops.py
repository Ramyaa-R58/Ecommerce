from azure.identity import AzureCliCredential, DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
import pyodbc
from settings import *




class DataBaseOps:
    cursor = None
    conn = None
    conn_str = None
    def assign_connection(self,cursor,conn,conn_str):
        self.cursor,self.conn,self.conn_str = cursor,conn,conn_str

    @staticmethod
    def get_connection():
        with pyodbc.connect(DataBaseOps.conn_str) as conn:
            DataBaseOps.conn = conn
            DataBaseOps.cursor = conn.cursor()
        return DataBaseOps.cursor,DataBaseOps.conn

    @staticmethod
    def connect_database():
        SERVER = 'eshop-server'
        DATABASE = 'eshop-db'
        USERNAME = 'ramyaa'
        PASSWORD = 'Tommy@123'
        DRIVER = '{ODBC Driver 18 for SQL Server}'


        # server_client = SqlManagementClient(credential=DefaultAzureCredential(),subscription_id=AZURE_SUBSCRIPTION_ID)
        # servers = server_client.servers.list_by_resource_group(RESOURCE_GRP)
        # if not SERVER in [server.name for server in servers]:
        #
        #     server_client.servers.begin_create_or_update(RESOURCE_GRP,SERVER,{
        #         "location":LOCATION,
        #         "administrator_login": USERNAME,
        #         "administrator_login_password": PASSWORD,
        #         "public_network_access":"Enabled"
        #
        #
        #     }).result()
        #     server_client.firewall_rules.create_or_update(RESOURCE_GRP,SERVER,'AllowAllWindowsAzureIps',{
        #                                                   'start_ip_address':'0.0.0.0',
        #                                                   'end_ip_address':'255.255.255.255'})
        #     server_client.databases.begin_create_or_update(RESOURCE_GRP,SERVER,DATABASE,{
        #         'location':LOCATION
        #     })

        # Has to be installed
        SERVER = 'eshop-server.database.windows.net'
        conn_str = (
            f"Driver={DRIVER};"
            f"Server=tcp:{SERVER},1433;"
            f"Database={DATABASE};"
            f"Uid={USERNAME};"
            f"Pwd={PASSWORD};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            )

# Connect and create table
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
        DataBaseOps.assign_connection(DataBaseOps,cursor=cursor,conn=conn,conn_str=conn_str)
        return cursor,conn
        
    @staticmethod
    def disconnect_connection(cursor,conn):
        DataBaseOps.cursor.close()
        DataBaseOps.conn.close()
    @staticmethod
    def insert_table_data(cursor, conn, table_name_data: dict):
        for table_name, data_list in table_name_data.items():
            # Map table to its column(s)
            if table_name == "RoleTable":
                columns = ["role_name"]
            elif table_name == "OrderStatusTable":
                columns = ["order_status_name"]
            elif table_name == "CartStatusTable":
                columns = ["cart_status_name"]
            elif table_name == "PaymentStatusTable":
                columns = ["payment_status_name"]
            else:
                continue

            # Check if table is empty
            cursor.execute(f"SELECT COUNT(*) FROM dbo.{table_name}")
            count = cursor.fetchone()[0]

            if count == 0:
                for row in data_list:
                    col_names = ", ".join(columns)
                    placeholders = ", ".join(["?" for _ in columns])
                    values = tuple(row[col] for col in columns)

                    cursor.execute(
                        f"INSERT INTO dbo.{table_name} ({col_names}) VALUES ({placeholders})",
                        values
                    )

        # Commit after all inserts
        conn.commit()
    @staticmethod
    def create_tables(cursor, conn):
        # Create UserTable with computed user_id (ESUID prefix)
        # UserTable
        cursor.execute("""
        IF OBJECT_ID('dbo.UserTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.UserTable (
                user_int_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id AS ('ESUID' + CAST(user_int_id AS NVARCHAR(50))) NVARCHAR(50) PERSISTED UNIQUE NOT NULL,
                full_name NVARCHAR(100) NOT NULL,
                email NVARCHAR(100) UNIQUE NOT NULL,
                password NVARCHAR(255) NOT NULL,
                phone_number NVARCHAR(20) NOT NULL
            )
        END
        """)

        # RoleTable
        cursor.execute("""
        IF OBJECT_ID('dbo.RoleTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.RoleTable (
                role_id INT IDENTITY(1,1) PRIMARY KEY,
                role_name NVARCHAR(50) UNIQUE NOT NULL
            )
        END
        """)

        # UserRoleTable
        cursor.execute("""
        IF OBJECT_ID('dbo.UserRoleTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.UserRoleTable (
                user_role_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id NVARCHAR(50) NOT NULL,
                role_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES dbo.UserTable(user_id),
                FOREIGN KEY (role_id) REFERENCES dbo.RoleTable(role_id)
            )
        END
        """)

        # AddressTable
        cursor.execute("""
        IF OBJECT_ID('dbo.AddressTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.AddressTable (
                address_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id NVARCHAR(50) NOT NULL,
                address_line1 NVARCHAR(255) NOT NULL,
                address_line2 NVARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES dbo.UserTable(user_id)
            )
        END
        """)

        # CategoryTable
        cursor.execute("""
        IF OBJECT_ID('dbo.CategoryTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.CategoryTable (
                category_int_id INT IDENTITY(1,1) PRIMARY KEY,
                category_id AS ('ESCID' + CAST(category_int_id AS NVARCHAR(50))) PERSISTED UNIQUE NOT NULL,
                category_name NVARCHAR(100) UNIQUE NOT NULL,
                category_description NVARCHAR(255)
            )
        END
        """)

        # ProductTable
        cursor.execute("""
        IF OBJECT_ID('dbo.ProductTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.ProductTable (
                product_int_id INT IDENTITY(1,1) PRIMARY KEY,
                product_id AS ('ESPID' + CAST(product_int_id AS NVARCHAR(50))) PERSISTED UNIQUE NOT NULL,
                product_name NVARCHAR(100) UNIQUE NOT NULL,
                product_description NVARCHAR(255),
                price FLOAT NOT NULL,
                stock_quantity INT NOT NULL,
                specifications NVARCHAR(MAX),
                category_id NVARCHAR(50) NOT NULL,
                FOREIGN KEY (category_id) REFERENCES dbo.CategoryTable(category_id)
            )
        END
        """)

        # OrderStatusTable
        cursor.execute("""
        IF OBJECT_ID('dbo.OrderStatusTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.OrderStatusTable (
                order_status_id INT IDENTITY(1,1) PRIMARY KEY,
                order_status_name NVARCHAR(50) UNIQUE NOT NULL
            )
        END
        """)

        # CartStatusTable
        cursor.execute("""
        IF OBJECT_ID('dbo.CartStatusTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.CartStatusTable (
                cart_status_id INT IDENTITY(1,1) PRIMARY KEY,
                cart_status_name NVARCHAR(50) UNIQUE NOT NULL
            )
        END
        """)

        # PaymentStatusTable
        cursor.execute("""
        IF OBJECT_ID('dbo.PaymentStatusTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.PaymentStatusTable (
                payment_status_id INT IDENTITY(1,1) PRIMARY KEY,
                payment_status_name NVARCHAR(50) UNIQUE NOT NULL
            )
        END
        """)

        # OrderTable
        cursor.execute("""
        IF OBJECT_ID('dbo.OrderTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.OrderTable (
                order_id NVARCHAR(50) PRIMARY KEY,
                user_id NVARCHAR(50) NOT NULL,
                order_date DATETIME NOT NULL,
                order_status_id INT NOT NULL,
                total_amount FLOAT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES dbo.UserTable(user_id),
                FOREIGN KEY (order_status_id) REFERENCES dbo.OrderStatusTable(order_status_id)
            )
        END
        """)

        # OrderProductTable
        cursor.execute("""
        IF OBJECT_ID('dbo.OrderProductTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.OrderProductTable (
                order_product_id INT IDENTITY(1,1) PRIMARY KEY,
                order_id NVARCHAR(50) NOT NULL,
                product_id NVARCHAR(50) NOT NULL,
                quantity INT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES dbo.OrderTable(order_id),
                FOREIGN KEY (product_id) REFERENCES dbo.ProductTable(product_id)
            )
        END
        """)

        # CartTable
        cursor.execute("""
        IF OBJECT_ID('dbo.CartTable', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.CartTable (
                cart_id INT IDENTITY(1,1) PRIMARY KEY,
                user_id NVARCHAR(50) NOT NULL,
                cart_status_id INT NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                product_id NVARCHAR(50) NOT NULL,
                quantity INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES dbo.UserTable(user_id),
                FOREIGN KEY (cart_status_id) REFERENCES dbo.CartStatusTable(cart_status_id),
                FOREIGN KEY (product_id) REFERENCES dbo.ProductTable(product_id)
            )
        END
        """)
        conn.commit()
        # Define table data with plain strings instead of ORM classes
        table_data = {
            "RoleTable": [
                {"role_name": "admin"},
                {"role_name": "customer"}
            ],
            "OrderStatusTable": [
                {"order_status_name": "initiated"},
                {"order_status_name": "paymentdone"},
            ],
            "CartStatusTable": [
                {"cart_status_name": "pending"},
                {"cart_status_name": "checkout"},
            ],
            "PaymentStatusTable": [
                {"payment_status_name": "completed"},
                {"payment_status_name": "failed"}
            ]
        }


        DataBaseOps.insert_table_data(cursor, conn, table_data)