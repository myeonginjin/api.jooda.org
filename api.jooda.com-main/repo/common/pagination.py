from rest_framework.pagination import LimitOffsetPagination


class JoodaPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return {
            "total_count": self.count,
            "results": data,
        }
