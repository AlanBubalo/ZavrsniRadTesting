from baserow_client import BaserowClient
from env import GROUP_NAME, DATABASE_NAME
from xmi_parsing import get_classes, get_full_tables, get_associations


def find(table: list, query: object):
    """ Returns list of items where some of their keys match some values
        If only one item was found, return the item, otherwise return the whole list """
    l = [item for item in table if all(item[key] == value for key, value in query.items())]
    return l[0] if len(l) == 1 else False if len(l) == 0 else l


client = BaserowClient()

if not client.is_token_valid():
    print("Token authentication failed. You can still use some functions that do not require authentication.")
    exit()

print("Congratulations! You got yourself a token!")

tables = get_classes()
print(f"Baserow Tables: {tables}")

full_tables = get_full_tables()


""" GET A GROUP ID """
list_groups_response = client.list_groups()
groups = list_groups_response.json()
print(groups)

if list_groups_response.status_code != 200:
    exit()

group = find(groups, {"name": GROUP_NAME})
print(f"Group ID: {group['id']}")


""" GET ALL APPLICATIONS / DATABASES """
databases_response = client.list_all_applications()
databases = databases_response.json()

if databases_response.status_code != 200:
    print(databases)
    exit()

print("All databases:")
for db in databases:
    print(db)


""" GET DATABASES IN A GROUP"""
databases_in_group_response = client.list_applications(group['id'])
databases_in_group = databases_in_group_response.json()

if databases_in_group_response.status_code != 200:
    print(databases_in_group)
    exit()

print("Databases with group GROUP:")
for db in databases_in_group:
    print(db)


""" CHECK IF A DATABASE ALREADY EXISTS """
database = find(databases_in_group, {"name": DATABASE_NAME})

if database:
    """ GET A DATABASE """
    print(f"Database {DATABASE_NAME} already exists")
else:
    """ CREATE A NEW DATABASE AND GET THE ID """
    print(f"Creating new database {DATABASE_NAME}")
    database_response = client.create_application(group['id'], DATABASE_NAME, "database")
    database = database_response.json()
print(f"Database ID: {database['id']}")


""" CREATE TABLES WITH ONLY PRIMARY KEY """
table_id_name = {}

for table in tables:
    table_response = client.create_database_table(database['id'], table)
    new_table = table_response.json()
    table_id_name[new_table['name']] = new_table['id']
    print(f"Table ID: {new_table['id']}")
    print(f"Created table {new_table['name']} with a primary key")

    """ CREATING FIELDS FOR EACH TABLE """
    for field in full_tables[new_table["name"]]:
        field_response = client.create_database_table_field(new_table["id"], field)
        new_field = field_response.json()
        if field_response.status_code != 200:
            print(new_field)
            exit()
        print(f"Created new field {new_field['id']} called {new_field['name']}")

""" ADD LINK ROWS TO TABLES """
associations = get_associations()

for table_name, table_id in table_id_name.items():
    for association in associations[table_name]:
        field_response = client.create_database_table_field(table_id, {
            "name": association['name'] or association['class_name'],
            "type": "link_row",
            "link_row_table_id": table_id_name[association['class_name']],
            "has_related_field": True,
        })
        new_field = field_response.json()
        print(f"Created new link row field {new_field['id']} called {new_field['name']}")
