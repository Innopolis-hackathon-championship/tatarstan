async def get_user(user_id):
    return {'role': 1}


def add_user(user_id):
    pass


async def add_product(item, number_of_product, price):
    print(item, number_of_product, price)
    pass

async def get_all_couriers():
    return [4445555,555555, 5591094060, 605058748]#DataBase.get_userids_by_role(2)
async def get_order(id):
    return {'id': 444,
            'composition': 'булочка с маком 3 шт'}

async def set_order_state(id, state):
    pass


