# from enum import Enum
# from fastapi import FastAPI

# class ModelName(str, Enum):
#     alexnet = 'alexnet'
#     resnet = 'resnet'
#     lenet = 'lenet'

# app = FastAPI()

# #* ------- Path Parameter --------------- 
# @app.get('/models/{model_name}/')
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {'model_name':model_name, "message": 'Deep Learning FTW'}
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# @app.get('/greet/{name}')
# def greeting(name: str):
#     return f'Hello {name}'



# #* -------- Query Parameter -------

# @app.get("/items")
# def get_data(category: str, brand: str):
#     return f"Category: {category}, Brand: {brand}"


# #* --------- Request body and Response body -------------- 
# from pydantic import BaseModel

# class Items(BaseModel):
#     name: str
#     description: str
#     price: float


# @app.post("/items/")
# def create_items(item:Items):
#     item = {"name":item.name, "description":item.description, "price": item.price}
#     return item



# class Demo(BaseModel):
#     name: str
#     description: str | None = None
#     prince: float
#     tax: float | None = None

# @app.post("/newitems")
# async def create_new_item(item: Demo):
#     item_dict = item.model_dump()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax 
#         item_dict.update({"price_with_tax":price_with_tax})
#     return item_dict


#* ---------- Request body + path parameters =-----------

# from fastapi import FastAPI
# from pydantic import BaseModel


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# app = FastAPI()

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()} 


# #* ------------- Request body + path + query parameters ------------------

# from fastapi import FastAPI
# from pydantic import BaseModel


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# app = FastAPI()

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result

#* ------------------ Additional Validations ----------------------- 

from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results 