class PaginateMixin:
    def modify_request(self, request):
        request.query_params._mutable = True
        page = request.query_params.get('page', 0)
        request.query_params['page'] = str(page)
        request.query_params._mutable = False
