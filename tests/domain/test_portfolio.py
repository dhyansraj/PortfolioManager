from domain.simple import Asset, User, Order, Position

from domain.portfolio import Portfolio

from mongoengine import connect, disconnect

from bson.json_util import dumps


def test_portfolio():

    disconnect()

    connect(
        "portfolio_manager",
        host="localhost",
        port=27017,
        username="admin",
        password="admin",
        authentication_source="admin",
    )

    Order.drop_collection()
    Asset.drop_collection()
    Position.drop_collection()
    User.drop_collection()
    Portfolio.drop_collection()

    goog = Asset(
        type="equity", symbol="GOOG", open=1786.07, close=1766.72, last=1766.72
    )

    goog.save()

    jpm = Asset(type="equity", symbol="JPM", open=134.58, close=138.05, last=138.05)

    jpm.save()

    dhyan = User(user_id="dhyanraj", first_name="Dhyan", last_name="Raj")

    dhyan.save()

    dhyan_port = Portfolio(user=dhyan)
    dhyan_port.save()

    dhyan_port.buy_asset(goog, 1600, 10, 0, None)

    dhyan_port.buy_asset(jpm, 160, 16, 0, None)

    dhyan_port.buy_asset(goog, 1610, 30, 0, None)

    dhyan_port.buy_asset(goog, 1620, 20, 0, None)

    dhyan_port.buy_asset(jpm, 165, 18, 0, None)


def test_portfolio_by_userid():

    disconnect()

    connect(
        "portfolio_manager",
        host="localhost",
        port=27017,
        username="admin",
        password="admin",
        authentication_source="admin",
    )

    dhyan = User.objects().first()

    dhyan_p = Portfolio.get_by_userid(dhyan)

    # print(dumps(dhyan_p.no_dereference().first().to_mongo()))

    y = dhyan_p.first()

    for x in y.positions:
        pos = x.to_mongo()

        # ass = pos.asset.to_mongo()

        print(dict(pos))

    assert dhyan_p


test_portfolio_by_userid()
