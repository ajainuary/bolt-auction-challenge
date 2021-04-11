# routes.py
import pathlib

from views import index, leaderboard, register, new_auction, submit_bid, end_auction


PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/leaderboard', leaderboard)
    app.router.add_post('/register', register)
    app.router.add_post('/new_auction', new_auction)
    app.router.add_post('/end_auction', end_auction)
    app.router.add_post('/submit_bid', submit_bid)
    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')
