import pytest
from model.models import Ebook, session
from api.services.ebook_service import EbookService
from objtyping import to_primitive
from schema.schemas import EbookSearchRequest
svc = EbookService()

def  test_search():
    req = EbookSearchRequest(page=2, pageSize=5)
    data, error = svc.fetch_all(req)
    for item in data.get_data():
        print('查询结果：',item.id)