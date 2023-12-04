'''
分类管理接口实现
'''
from fastapi import APIRouter
from api.services.category_service import CategoryService
from model.com_response import ComResponse
from schema.schemas import CategoryAddRequest,CategoryUpdateRequest

svc = CategoryService()

router = APIRouter(
    prefix='/api/v1/categorys'
)

@router.get('/')
async def get_list(name:str = ''):
    data, error = svc.get_all(name)
    resp = ComResponse()
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content(data)
    return resp

@router.post('/save')
async def save_category(category: CategoryUpdateRequest):
    resp = ComResponse()
    error = svc.update_category(category)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    return resp

@router.post('/add')
async def add_category(category: CategoryAddRequest):
    resp = ComResponse()
    newId,error = svc.add_category(category)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content({'id': newId})
    return resp

@router.delete('/{categoryId}')
async def delete_by_id(categoryId: int):
    resp = ComResponse()
    error = svc.delete_category([categoryId])
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    return resp

@router.get('/{categoryId}')
async def fetch_by_id(categoryId: int):
    resp = ComResponse()
    data, error = svc.get_by_id(categoryId)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content(data)
    return resp