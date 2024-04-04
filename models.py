# where we create the database
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Products(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, null=False)
    quantity = fields.IntField(default=0)
    amount_sold = fields.IntField(default=0)
    unit_price = fields.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    revenue = fields.DecimalField(decimal_places=2, max_digits=20, default=0.00)

    # will be the warehouses
    supplied_by = fields.ForeignKeyField('models.Warehouse', related_name='goods_supplied')


# Supplier(Warehouse) inherits from model
class Warehouse(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    location = fields.CharField(max_length=50)
    inventory = fields.IntField(default=0)
    capacity = fields.IntField(default=0)



class DeliveryVehicle(Model):
    id = fields.IntField(pk=True)
    VehicleCapacity = fields.IntField(default=0)
    coverage = fields.CharField(max_length=4)  #How to code the location coverage for the vehicles


#Pydantic Models
#create model for accepting incoming data
product_pydantic = pydantic_model_creator(Products, name="Product")
product_pydanticIn = pydantic_model_creator(Products, name="ProductIn", exclude_readonly=True)
#excludes read only fields such as ID

warehouse_pydantic = pydantic_model_creator(Warehouse, name="Warehouse")
warehouse_pydanticIn = pydantic_model_creator(Warehouse, name="WarehouseIn", exclude_readonly=True)

vehicle_pydantic = pydantic_model_creator(DeliveryVehicle, name="Vehicle")
vehicle_pydanticIn = pydantic_model_creator(DeliveryVehicle, name="VehicleIn", exclude_readonly=True)