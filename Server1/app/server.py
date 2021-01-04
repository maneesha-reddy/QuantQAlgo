from aiohttp import web
from . import views


app = web.Application()
app.router.add_get('/', views.)