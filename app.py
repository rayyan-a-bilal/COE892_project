from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import (warehouse_pydantic, warehouse_pydanticIn, Warehouse)
from models import (vehicle_pydantic, vehicle_pydanticIn, DeliveryVehicle)

from fastapi.middleware.cors import CORSMiddleware

#from dotenv import dotenv_values


# adding cors urls
origins = [
    "http://localhost:3000" # 3000 is default for react app
]




app = FastAPI()

# adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get('/')

def index():
    return {"Msg": "Go to /docs for the documentation of the API endpoints"}





################# Warehouse CRUD

@app.post('/warehouse')
async def add_warehouse(warehouse_info: warehouse_pydanticIn):
    warehouse_obj = await Warehouse.create(**warehouse_info.dict())
    response = await warehouse_pydantic.from_tortoise_orm(warehouse_obj)
    return {"status": "ok", "data": response}


@app.get('/warehouse/{')
async def get_warehouses():
    response = await warehouse_pydanticIn.from_queryset(Warehouse.all())
    return {"status": "ok", "data": response}


@app.get('/warehouse/{warehouse_id}')
async def get_specific_warehouse(warehouse_id: int):
    response = await warehouse_pydantic.from_queryset_single(Warehouse.get(id=warehouse_id)) #serialize single warehouse
    return {"status": "ok", "data": response}


@app.put('/warehouse/{warehouse_id}')
async def update_warehouse(warehouse_id: int, update_info: warehouse_pydanticIn):
    warehouse = await Warehouse.get(id=warehouse_id)
    update_info = update_info.dict(exclude_unset=True)
    for attribute, value in update_info.items():
        setattr(warehouse, attribute, value)
    await warehouse.save()
    response = await warehouse_pydantic.from_tortoise_orm(warehouse)
    return {"status": "ok", "data": response}

@app.delete('/warehouse/{warehouse_id}')
async def delete_warehouse(warehouse_id: int):
    warehouse = await Warehouse.filter(id=warehouse_id).delete()
    if warehouse:
        return {"status": "ok"}
    return {"status": "error", "message": "Warehouse not found"}








############### Vehicle CRUD

@app.post('/vehicle')
async def add_vehicle(vehicle_info: vehicle_pydanticIn):
    vehicle_obj = await DeliveryVehicle.create(**vehicle_info.dict())
    response = await vehicle_pydantic.from_tortoise_orm(vehicle_obj)
    return {"status": "ok", "data": response}


@app.get('/vehicle/{')
async def get_vehicle():
    response = await vehicle_pydanticIn.from_queryset(DeliveryVehicle.all())
    return {"status": "ok", "data": response}


@app.get('/vehicle/{vehicle_id}')
async def get_specific_vehicle(vehicle_id: int):
    response = await vehicle_pydantic.from_queryset_single(DeliveryVehicle.get(id=vehicle_id)) #serialize single car
    return {"status": "ok", "data": response}


@app.put('/vehicle/{vehicle_id}')
async def update_vehicle(vehicle_id: int, update_info: vehicle_pydanticIn):
    vehicle = await DeliveryVehicle.get(id=vehicle_id)
    update_info = update_info.dict(exclude_unset=True)
    for attribute, value in update_info.items():
        setattr(vehicle, attribute, value)
    await vehicle.save()
    response = await vehicle_pydantic.from_tortoise_orm(vehicle)
    return {"status": "ok", "data": response}

@app.delete('/vehicle/{vehicle_id}')
async def delete_vehicle(vehicle_id: int):
   vehicle = await DeliveryVehicle.filter(id=vehicle_id).delete()
   if vehicle:
       return {"status": "ok"}
   return {"status": "error", "message": "Vehicle not found"}


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']}, generate_schemas=True,
    add_exception_handlers=True

)