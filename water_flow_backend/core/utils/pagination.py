# Django imports
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):

    # Page size
    page_size = 10

    # Page size query parameter
    page_size_query_param = 'page_size'

    # Maximum page size
    max_page_size = 100