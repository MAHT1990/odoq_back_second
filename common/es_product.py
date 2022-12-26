from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q, Range

from django.conf import settings

# 상품명 검색시, 운영환경에서만 elasticsearch를 활용하여 검색

if settings.SEARCH_ENGINE == 'ELASTIC':
  elasticsearch = Elasticsearch(settings.ELASTICSEARCH_HOST)
  #index = 'product'
  index = 'mongo_product'
  search = Search(using=elasticsearch, index=index)

# name만 query, 다른 필드 조건은 filter로
class SearchSample:
  def __init__(self, q, filters: dict = None, sort: dict = None, page: int = 1, page_size: int = 50):
    self.q = q
    self.filters = filters,
    self.sort = sort
    self.page = page
    self.page_size = page_size

  def __call__(self, *args, **kwargs):

    skip = self.page - 1
    s = Search(using=elasticsearch, index=index).extra(from_=(skip * self.page_size), size=self.page_size)
    q = (
      Q('match_phrase', name=self.q)
    )
    f = (
        Q('match', is_deleted=False)
        & Q('terms', store_id=[17, 16])
        &
        (
          Q('range', **{'price': {'gte': 10000, 'lt': 40000}})
          | Q('range', **{'discount_price': {'gte': 10000, 'lt': 40000}})
        )
        # & Q('match', store_id=13)
        # & Q('range', created_at={'gte': '2021-10-11', 'lte': '2021-10-19'})
    )

    s = s.query(q)
    s = s.filter(f)
    response = s.sort('created_at').execute()

    print(response)
    for hit in response:
      print(hit.name)



