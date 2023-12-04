from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/api/v1/hello',
    # tags=['hello']
)

@router.get('/')
def sayHello():
    return 'hello man!!'

@router.get('/{id}')
def getUser(id: int):
    # JSONResponse，返回json响应数据
    item = {'name':'dada', 'national': '中国2'}
    return JSONResponse(content=item)

