import os

from fastapi import Request
from fastapi.templating import Jinja2Templates


current_directory = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_directory, "templates"))


from jinja2 import pass_context


@pass_context
def urlx_for(context: dict, name: str, **path_params: any) -> str:
    request: Request = context['request']
    http_url = request.url_for(name, **path_params)
    if scheme := request.headers.get('x-forwarded-proto'):
        return http_url.replace(scheme=scheme)
    return http_url


templates.env.globals['url_for'] = urlx_for