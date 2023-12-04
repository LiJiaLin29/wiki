'''
电子书接口实现
'''
from typing import List,Union
from fastapi import APIRouter, Query
from api.services.ebook_service import EbookService
from model.com_response import ComResponse
from schema.schemas import EbookAddRequest,EbookUpdateRequest,EbookSearchRequest
from config.logger import myLogger

logger = myLogger(__name__)

svc = EbookService()

router = APIRouter(
    prefix='/api/v1/ebooks'
)

@router.get('/')
async def get_list(categoryIds:Union[List[int],None]=Query(default=None),page:int = 1, pageSize:int = 5,name:str = ''):
    logger.debug(f'get_list,查询条件：categoryIds={categoryIds}')
    req = EbookSearchRequest(page=page, pageSize=pageSize, name=name,categoryIds=categoryIds)
    data, error = svc.fetch_all(req)
    resp = ComResponse()
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content(data)
    return resp

@router.post('/save')
async def save_ebook(ebook: EbookUpdateRequest):
    resp = ComResponse()
    error = svc.update_ebook(ebook)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    return resp

@router.post('/add')
async def add_ebook(ebook: EbookAddRequest):
    resp = ComResponse()
    error = svc.add_ebook(ebook)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    return resp

@router.delete('/{bookId}')
async def delete_by_id(bookId: int):
    resp = ComResponse()
    error = svc.delete_ebook([bookId])
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    return resp

@router.get('/{bookId}')
async def fetch_by_id(bookId: int):
    resp = ComResponse()
    data, error = svc.get_by_id(bookId)
    if error is not None:
        resp.set_success(False)
        resp.set_message(error)
    else:
        resp.set_content(data)
    return resp