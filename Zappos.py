from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

restaurants = []
restaurant_menus = []
menu_items = []


class Restaurant(Resource):
    @classmethod
    def get(cls, name):
        restaurant = next(filter(lambda rest: rest['name'] == name, restaurants), None)
        if restaurant:
            return {'restaurant': restaurant}, 200
        else:
            return 404  # 404 error code if restaurant cannot be found

    @classmethod
    def post(cls, name):
        # filters to only return a matching restaurant with that name, returns nothing if there is none
        if next(filter(lambda rest: rest['name'] == name, restaurants), None):
            return {'Error': "A restaurant with name '{}' already exists.".format(name)}, 400

        restaurant = {'name': name}
        restaurants.append(restaurant)
        return restaurant, 201

    @classmethod
    def delete(cls, name):
        global restaurants
        # re-creates the list without the deleted restaurant
        restaurants = list(filter(lambda rest: rest['name'] != name, restaurants))
        return {'Result': "Restaurant was successfully deleted."}


class Menu(Resource):
    @classmethod
    def get(cls, name):
        restaurant_menu = next(filter(lambda menu: menu['name'] == name, restaurant_menus), None)
        if restaurant_menu:
            return {'restaurant_menu': restaurant_menu}, 200
        else:
            return {'Error': "Menu '{}' could not be found.".format(name)}, 404

    @classmethod
    def post(cls, name):
        if next(filter(lambda menu: menu['name'] == name, restaurant_menus), None):
            return {'Error': "A menu with name '{}' already exists. ".format(name)}, 400
        else:
            restaurant_menu = {'name': name}
            restaurant_menus.append(restaurant_menu)
            return restaurant_menu, 201

    @classmethod
    def delete(cls, name):
        global restaurant_menus
        restaurant_menus = list(filter(lambda menu: menu['name'] != name, restaurant_menus))
        return {'Result': "Item was successfully deleted."}


class MenuItem(Resource):
    @classmethod
    def get(cls, name):
        menu_item = next(filter(lambda item: item['name'] == name, menu_items), None)
        if menu_item:
            return {'menu_item': menu_item}, 200
        else:
            return 404  # 404 error code if item cannot be found

    menu_parser = reqparse.RequestParser()
    menu_parser.add_argument('price', type=float, required=True, help="The price is required.")

    @classmethod
    def post(cls, name):
        # filters to only return a matching menu item with that name, returns nothing if there is none
        if next(filter(lambda item: item['name'] == name, menu_items), None):
            return {'Error': "An item with name '{}' already exists on the menu.".format(name)}, 400
        data = MenuItem.menu_parser.parse_args()

        menu_item = {'name': name, 'price': data['price']}
        menu_items.append(menu_item)
        return menu_item, 201

    @classmethod
    def delete(cls, name):
        global menu_items
        menu_items = list(filter(lambda item: item['name'] != name, menu_items))
        return {'Result': "Item was successfully deleted."}

    @classmethod
    def put(cls, name):
        data = MenuItem.menu_parser.parse_args()
        menu_item = next(filter(lambda item: item['name'] == name, menu_items), None)

        # if the menu item does not exist, it will create a new menu item
        if menu_item is None:
            menu_item = {'name': name, 'price': data['price']}
            # add the new item to the existing items list
            menu_items.append(menu_item)
        # if the item already exists, the existing item will be updated with the data
        else:
            menu_item.update(data)
        return menu_item


class AllItems(Resource):
    @classmethod
    def get(cls):
        # returns all the menu items
        return {'All Menu Items': menu_items}


class AllMenus(Resource):
    @classmethod
    def get(cls):
        return {'All Menus': restaurant_menus}


class AllRestaurants(Resource):
    @classmethod
    def get(cls):
        return {'Restaurants': restaurants}


# adds path to all menus
api.add_resource(AllMenus, '/menus')
# adds path to a specific item on a menu in a restaurant
api.add_resource(MenuItem, '/item/<string:name>')
# adds path to all menu items
api.add_resource(AllItems, '/items')
# adds path to the list of all restaurants
api.add_resource(AllRestaurants, '/restaurants')
# adds path to a specific menu
api.add_resource(Menu, '/menu/<string:name>')
# adds path to a specific restaurant
api.add_resource(Restaurant, '/restaurant/<string:name>')

app.run(port=5000, debug=True)
