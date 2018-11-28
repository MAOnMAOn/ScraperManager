from pure_pagination import Paginator, PageNotAnInteger


def paginator_processing(request, query_set):
    # 进行分页处理
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    page_size = request.GET.get('pageSize', 10)
    p = Paginator(query_set, int(page_size), request=request)
    paginator = int(page)
    p.start_item = (paginator - 1) * p.per_page + 1
    p.end_item = p.per_page * paginator if p.count > p.per_page * paginator else p.count
    query_set = p.page(str(page))
    return query_set


