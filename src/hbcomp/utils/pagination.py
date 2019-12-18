from flask import request, url_for, current_app


def get_page(request, arg_name='p'):
    try:
        return int(request.args.get(arg_name, '1'))
    except ValueError:
        return 1


def get_page_size(request, arg_name='s', default_size=None):
    if default_size is None:
        default_size = current_app.config.get('DEFAULT_LIST_PAGE_SIZE', 10)
    try:
        r = int(request.args.get(arg_name, default_size))
    except ValueError:
        r = default_size
    max_size = current_app.config.get('MAX_LIST_PAGE_SIZE', 50)
    if r > max_size:
        r = max_size
    return r


def url_for_other_page(page):  # pragma: no cover
    args = request.view_args.copy()
    args['p'] = page
    return url_for(request.endpoint, **args)
