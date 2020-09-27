"""
To paginate the query
"""
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator


def paginate_data(request, query, per_page=25):
    paginator = Paginator(query, per_page) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query = paginator.page(paginator.num_pages)
    return query
