from flask import request, session


def get_next_url(default):
    return request.args.get('next') or session.pop('next', None) or default
