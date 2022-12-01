from baserow_requests import BaserowClient
from env import EMAIL, PASSWORD, GROUP_NAME, DATABASE_NAME
from xmi_parsing import get_classes, get_full_tables, get_associations, get_full_associations, setup_baserow_ids

client = BaserowClient(EMAIL, PASSWORD)

tables = get_classes()
print(f"Baserow Tables: {tables}")

full_tables = get_full_tables()


def find(table: object, keys: list, values: list):
    """ Returns list of items where some of their keys match some values
        If only one item was found, return the item, otherwise return the whole list """
    l = [item for item in table if all(item[key] == value for key, value in zip(keys, values))]
    return l[0] if len(l) == 1 else False if len(l) == 0 else l


""" GET A GROUP ID """
list_groups_response = client.list_groups()
groups = list_groups_response.json()
group = find(groups, ["name"], [GROUP_NAME])
print(f"Group ID: {group['id']}")


""" GET ALL APPLICATIONS / DATABASES """
databases_response = client.list_all_applications()
databases = databases_response.json()
print("Databases:")
for db in databases:
    print(db)


""" GET DATABASES IN A GROUP"""
databases_in_group = [database for database in databases if database["group"]["id"] == group["id"]]
print("Databases with group GROUP:")
for db in databases_in_group:
    print(db)


""" CHECK IF A DATABASE ALREADY EXISTS """
database = find(databases_in_group, ["name"], [DATABASE_NAME])

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
table_id_name = []
for table in tables:
    table_response = client.create_database_table(database['id'], table)
    new_table = table_response.json()
    table_id_name.append((new_table['name'], new_table['id']))
    print(f"Table ID: {new_table['id']}")
    print(f"Created table {new_table['name']} with a primary key")

    """ CREATING FIELDS FOR EACH TABLE """
    fields = full_tables[new_table["name"]]
    
    for field in fields:
        field_response = client.create_database_table_field(new_table["id"], field)
        new_field = field_response.json()
        print(f"Created new field {new_field['id']} called {new_field['name']}")

""" ADD LINK ROWS TO TABLES """
baserow_id = dict(table_id_name)
classes = get_classes(for_baserow=False)
assoc_class = get_associations(classes)

for name, id in table_id_name:
    associations = assoc_class[name]
    
    for assoc in associations:
        field = {
            'name': assoc['name'] if assoc['name'] else assoc['class_name'],
            "type": "link_row",
            "link_row_table_id": baserow_id[assoc['class_name']],
            "has_related_field": True,
        }
        field_response = client.create_database_table_field(id, field)
        new_field = field_response.json()
        print(f"Created new link row field {new_field['id']} called {new_field['name']}")
        