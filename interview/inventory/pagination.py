from rest_framework.pagination import LimitOffsetPagination


class ListViewPagination(LimitOffsetPagination):
    default_limit = 3
