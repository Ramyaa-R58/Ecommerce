from fastapi import FastAPI
from EndPoints.routes import router_handle
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from DB_ops.database_ops import DataBaseOps
app = FastAPI()

app.include_router(router_handle)
cursor,conn = DataBaseOps.connect_database()
DataBaseOps.create_tables(cursor,conn)
app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_credentials=["*"],
    allow_origins=["*"],
    allow_methods=["*"]

)

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",port=8000,reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
