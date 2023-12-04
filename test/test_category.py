import pytest
from model.models import Category, session
from api.services.category_service import CategoryService
from objtyping import to_primitive
svc = CategoryService()

def  test_search():
    tree = svc.get_category_tree()
    print(f'tree:{tree}')