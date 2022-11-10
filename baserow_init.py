from baserow_requests import BaserowClient
from env import EMAIL, PASSWORD, GROUP_NAME, DATABASE_NAME
import xmi_parsing

client = BaserowClient(EMAIL, PASSWORD)

br_tables = xmi_parsing.get_classes()
print(f"Baserow Tables: {br_tables}")


def find(table: object, keys: list, values: list):
    """
        Returns list of items where some of their keys match some values
        If only one item was found, return the item, otherwise return the whole list
    """
    l = [item for item in table if all(item[key] == value for key, value in zip(keys, values))]
    return l[0] if len(l) == 1 else l


""" GET A GROUP ID """
list_groups_response = client.list_groups()
groups = list_groups_response.json()
group = find(groups, ["name"], [GROUP_NAME])
print(f"Group ID: {group['id']}")


""" CREATE A NEW DATABASE AND GET THE ID """
nastava_response = client.create_application(group['id'], DATABASE_NAME, "database")
database = nastava_response.json()
print(f"Database ID: {database['id']}")


""" CREATE TABLES WITH ONLY PRIMARY KEY """
for table in br_tables:
    table_response = client.create_database_table(database['id'], table)
    new_table = table_response.json()
    print(f"Table ID: {new_table['id']}")
    print(f"Created table {new_table['name']} with a primary key")
