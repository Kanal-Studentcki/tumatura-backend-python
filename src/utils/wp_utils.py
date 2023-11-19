import os

import requests
from requests.auth import HTTPBasicAuth

from src.utils.mongo_utils import MongoUtils


class WPUtils:
    def __init__(self):
        self.BASE_URL = os.getenv("WP_BASE_URL")
        self.auth = HTTPBasicAuth(os.getenv("WP_WC_KEY"), os.getenv("WP_WC_SECRET"))

        mongo = MongoUtils()

    def get_role_names_from_product(self, product_id: int):
        resp = requests.get(f"{self.BASE_URL}/products/{product_id}", auth=self.auth)
        if resp.ok:
            data = resp.json()
            return next((attribute["options"] for attribute in data["attributes"] if attribute["name"] == "role"), None)

    def get_customer_data(self, customer_id: int):
        # TODO: Waiting on Wordpress confgiration
        return {"discord": "", "email": ""}

    def get_all_customers(self):
        page = 1
        all_customers = []

        while True:
            resp = requests.get(f"{self.BASE_URL}/wp-json/wc/v3/customers", params={'page': page}, auth=self.auth)

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
