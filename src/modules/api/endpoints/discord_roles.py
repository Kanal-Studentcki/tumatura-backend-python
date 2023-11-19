from itertools import chain

from fastapi.responses import JSONResponse

from src.modules.api.routers import register_router
from src.modules.api.rules.discord_roles_data import WPOrderUpdateData
from src.utils.mongo_utils import mongo_utils
from src.utils.wp_utils import wp_utils

router = register_router("/discord_roles")


@router.post("/new_purchase")
async def new_purchase(data: WPOrderUpdateData):
    if data.status == "Completed":
        product_ids = [product.product_id for product in data.line_items]
        product_role_names = [wp_utils.get_role_names_from_product(product_id) for product_id in product_ids]
        roles_to_assign = set(chain(*product_role_names))

        role_ids = []
        for role_name in roles_to_assign:
            role_ids.append(mongo_utils.get_role_id_by_name(role_name))

        customer_data = wp_utils.get_customer_data(data.customer_id)
        mongo_utils.upsert_user_role(role_ids, customer_data["discord"], customer_id=data.customer_id,
                                     email=customer_data["email"])

        return JSONResponse(content={"success": True, "comment": ""}, status_code=201)

    return JSONResponse(content={"success": False, "comment": "Skipped, order status != 'Completed'"}, status_code=200)
