from domain.simple import User, Order, Position

from mongoengine import Document, ReferenceField, ListField

from mongoengine import queryset_manager


class Portfolio(Document):
    positions = ListField(ReferenceField(Position))
    user = ReferenceField(User)

    def buy_asset(self, asset, price, quantity, charges, time):
        order = Order(
            asset=asset,
            user=self.user,
            price=price,
            quantity=quantity,
            charges=charges,
            time=time,
        )

        order.save()

        self.__add_to_position(order)

    def sell_asset(self, asset, price, quantity, charges, time):
        order = Order(
            type=False,
            asset=asset,
            user=self.user,
            price=price,
            quantity=quantity,
            charges=charges,
            time=time,
        )

        order.save()

        self.__add_to_position(order)

    def __add_to_position(self, order):

        pos = [
            x
            for x in self.positions
            if x.asset.type == order.asset.type and x.asset.symbol == order.asset.symbol
        ]

        if not pos:
            p = Position(orders=[order], asset=order.asset)

            if not self.positions:
                self.positions = [p]
            else:
                self.positions.append(p)
        else:
            p = pos[0]

            p.orders.append(order)

        p.save()

        self.save()

    @queryset_manager
    def get_by_userid(doc_cls, queryset, user):
        return queryset.filter(user=user)
