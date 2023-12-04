'''
文档节管理接口实现
'''
from fastapi import APIRouter
from typing import Union
from api.services.ebookdoc_service import EbookDocService
from model.com_response import ComResponse
from schema.schemas import EbookDocAddRequest,EbookDocUpdateRequest

svc = EbookDocService()

router = APIRouter(
    prefix='/api/v1/docs'
)

@router.get('/')
async def get_list(name:str = '', ebookId:Union[int,None]=None):
    data, error = svc.get_all(name, ebookId)
    resp = ComResponse()
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content(data)
    return resp

@router.post('/save')
async def save_ebookdoc(ebookdoc: EbookDocUpdateRequest):
    resp = ComResponse()
    error = svc.update_ebookdoc(ebookdoc)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    return resp

@router.post('/add')
async def add_ebookdoc(ebookdoc: EbookDocAddRequest):
    resp = ComResponse()
    newId,error = svc.add_ebookdoc(ebookdoc)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content({'id': newId})
    return resp

@router.delete('/{ebookdocId}')
async def delete_by_id(ebookdocId: int):
    resp = ComResponse()
    error = svc.delete_ebookdoc([ebookdocId])
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    return resp

@router.get('/{ebookdocId}')
async def fetch_by_id(ebookdocId: int):
    resp = ComResponse()
    data, error = svc.get_by_id(ebookdocId)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content(data)
    return resp