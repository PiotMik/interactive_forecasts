from fastapi import FastAPI, Query
from typing import Annotated
import uvicorn
from backend import data_management, methodology_gateway

app = FastAPI()


@app.get("/data")
async def get_data(dataset: str, variables: Annotated[list[str], Query()]):
    data = data_management.load_data(dataset)[variables]
    return data.to_json(orient='columns')


@app.put("/data")
async def insert_datapoint(dataset: str, variable: str, date: str, value: float):
    data = data_management.load_data(dataset)
    data.loc[date, variable] = value
    data_management.dump_data(data=data, name=dataset)


@app.get("/forecast/{methodology_name}")
async def get_forecast(methodology_name: str, payload: dict):
    dataset, inputs = payload['dataset'], payload['inputs']
    wrapper = methodology_gateway.MethodologyWrapper.get_wrapper(methodology_name=methodology_name)
    inputs_parsed = wrapper.prepare_inputs(dataset=dataset, **inputs)
    return wrapper.call(**inputs_parsed).to_json(orient='columns')

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8080)
