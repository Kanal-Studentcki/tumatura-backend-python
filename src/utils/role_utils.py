from src.utils.mongo_utils import mongo_utils

EXCLUDED_ROLE_ID = [1166822529701249117, 1166829905372266546,
                    1166828951138746420]  # [@everyone, @Admin, @Kanał Studentcki]


def roles_diff(discord_name: str, current_roles: list[int]) -> dict[str, list[int]]:
    current_roles = [i for i in current_roles if i not in EXCLUDED_ROLE_ID]

    diff = {"add": [], "delete": []}
    active_roles = [role.role_id for role in mongo_utils.get_user_data(discord_name=discord_name).roles]

    for role in current_roles:
        if role not in active_roles:
            diff["delete"].append(role)

    for role in active_roles:
        if role not in current_roles:
            diff["add"].append(role)

    return diff
