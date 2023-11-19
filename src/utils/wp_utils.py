import os

import requests
from requests.auth import HTTPBasicAuth

from src.utils.mongo_utils import MongoUtils


class WPUtils:
    def __init__(self) -> None:
        self.BASE_URL = os.getenv("WP_BASE_URL")
        self.auth = HTTPBasicAuth(os.environ["WP_WC_KEY"], os.environ["WP_WC_SECRET"])

        mongo = MongoUtils()

    def get_role_names_from_product(self, product_id: int) -> list[str]:
        resp = requests.get(f"{self.BASE_URL}/products/{product_id}", auth=self.auth)
        resp.raise_for_status()

        data = resp.json()
        return next((attribute["options"] for attribute in data["attributes"] if attribute["name"] == "role"), [])

    def get_customer_data(self, customer_id: int) -> dict:
        # TODO: Waiting on Wordpress confgiration
        return {"discord": "", "email": ""}

    def get_all_customers(self) -> list[dict]:
        page = 1
        all_customers = []

        while True:
            resp = requests.get(f"{self.BASE_URL}/wp-json/wc/v3/customers", params={"page": page}, auth=self.auth)

            if resp.ok:
                customers = resp.json()
                if not customers:
                    break
                all_customers.extend(customers)

                page += 1
            else:
                raise Exception("Error fetching customers")

        return all_customers


wp_utils = WPUtils()
