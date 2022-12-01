import xml.dom.minidom
from collections import defaultdict

f_s = lambda x: x.replace("%20", " ")

doc = xml.dom.minidom.parse("models/online_shopping_model.xmi")
xmi = doc.firstChild
model = xmi.getElementsByTagName("uml:Model")[0]
packaged_elements = model.getElementsByTagName("packagedElement")

baserow_id = {}
"""
baserow_id = {
    "Web User": 115328,
    "Customer": 115329,
    "Account": 115330,
    "Payment": 115331,
    "Order": 115332,
    "Shopping Cart": 115333,
    "Line Item": 115334,
    "Product": 115335
}
"""

def get_classes(for_baserow=True):
    # Classes
    classes = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:Class"]
    
    br_tables = [{
        "name": f_s(el.getAttribute("name")),
        "data": [["/"]], # Empty table with a primary key named "/"
        "first_row_header": True
    } for el in classes]
    
    return br_tables if for_baserow else classes


def get_associations(classes):
    ll = {}
    for _class in classes:
        members_class = _class.getElementsByTagName("ownedMember")
        # print("==== Members of a single class ====")
        # print(members_class)
        # l_assoc = [member for member in members_class if member.getAttribute("xmi:type") == "uml:Association"]
        
        owned_ends = [member.getElementsByTagName("ownedEnd") for member in members_class]
        # print(owned_ends)
        
        l = []
        for pair in owned_ends:
            ends = [{
                "name": curr.getAttribute("name"),
                # "type": "association",
                "class_name": next(f_s(__class.getAttribute("name"))
                                    for __class in classes
                                    if __class.getAttribute("xmi:id") == curr.getAttribute("type")),
                # "aggregation": curr.getAttribute("aggregation"),
                # "lower_value": curr.getElementsByTagName("lowerValue")[0].getAttribute("value"),
                # "upper_value": curr.getElementsByTagName("upperValue")[0].getAttribute("value")
            } for curr in pair]
            # print(f"{ends[0]} - {ends[1]}")
            l.append(ends)

        ll[f_s(_class.getAttribute("name"))] = [end[1] for end in l]
    return ll


def setup_baserow_ids(names_ids):
    baserow_id = dict(names_ids)


def get_full_associations(table_name):
    classes = get_classes(for_baserow=False)
    assoc_class = get_associations(classes)
        
    associations = assoc_class[table_name]

    return [{
            'name': assoc['name'] if assoc['name'] else assoc['class_name'],
            "type": "link_row",
            "link_table_id": baserow_id[assoc['class_name']],
            "has_related_field": True,
    } for assoc in associations]


def get_attribute_names(classes, data_types):
    list_attributes = []
    for _class in classes:
        l_atr = []
        attributes_class = _class.getElementsByTagName("ownedAttribute")
        # print("==== Attributes of a second class ====")
        # print(attributes_class)
        
        for attribute_name in attributes_class:
            # print("attribute_name - type:", attribute_name.getAttribute("type"))
            # print("data_type - name:", [data_type["name"] for data_type in data_types])
            _type = ""
            if attribute_name.getAttribute("type") != "":
                _type = next(data_type["name"] for data_type in data_types if data_type["id"] == attribute_name.getAttribute("type"))
            attributes_name_type = {
                "name": attribute_name.getAttribute("name"),
                "type": _type
            }
            # print("==== Attribute names and id ==== ")
            # print(attributes_name_type)
        
            l_atr.append(attributes_name_type)

        # l_atr.extend(get_associations(_class))
        # print("================================")
        # print(l_atr)
        list_attributes.append(l_atr)
    return list_attributes


def get_enumerations():
    # Enumerations
    enumerations = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:Enumeration"]
    
    all_literals = [enumeration.getElementsByTagName("ownedLiteral") for enumeration in enumerations]
    # print("==== Literals elements of all enumerations ====")
    # print(all_literals)
    en_literals = [{
        "id": enum.getAttribute("xmi:id"),
        "name": enum.getAttribute("name"),
        "literals": {lit.getAttribute("name")
                     for lit in literals}
    } for enum, literals in zip(enumerations, all_literals)]
    # print("==== Enumerations with their literals ==== ")
    # print(en_literals)
    return en_literals

def get_data_types(enums):
    # Data Types
    __data_types__ = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:DataType"]
    
    data_types = [{
        "id":  _data_type.getAttribute("xmi:id"),
        "name" : f_s(_data_type.getAttribute("name"))
    } for _data_type in __data_types__]
    # print("==== All data types ====")
    # print(data_types)
    data_types.extend(enums)
    
    return data_types


def get_attributes_with_data_types(class_attributes, enums):
    # print(class_attributes)
    for class_name, attributes in class_attributes.items():
        upgraded_attributes = []
        upgraded_associations = []
        
        for attr in attributes:
            print(attr)
            dict_type = defaultdict(lambda x: None)
            """
            # Handling Association, that is, Link Row
            if (type(attr) == list):
                # Attribute is an association
                dict_type["name"] = attr[0]["name"] if attr[0]["name"] else attr[0]["class_name"]
                dict_type["type"] = "link_row"
                dict_type["link_row_table_id"] = ""
                dict_type["has_related_field"] = False
                
                upgraded_associations.append(dict(dict_type))
                continue
            """  
                
            dict_type["name"] = attr["name"].title().replace("_", " ")
            lower_name = attr["type"].lower()
            
            # Handling Number Type
            if lower_name in ["integer", "int", "unsigned integer", "unsigned int", "float", "real"]:
                dict_type["type"] = "number"
                dict_type["number_decimal_places"] = 0
                dict_type["number_negative"] = True
                if lower_name in ["unsigned integer", "unsigned int"]:
                    dict_type["number_negative"] = False
                if lower_name in ["float", "real"]:
                    dict_type["number_decimal_places"] = 5
        
            # Handling Text Type
            elif lower_name in ["string", "str"]:
                dict_type["type"] = "text"
                dict_type["text_default"] = "" # for now
            
            # Handling Long Text Type
            elif lower_name in ["blob", "text"]:
                dict_type["type"] = "long_text"
            
            # Handling URL Type
            elif lower_name == "url":
                dict_type["type"] = "url"
                
            # Handling Email Type
            elif lower_name == "email":
                dict_type["type"] = "email"
            
            # Handling Rating Type
            elif lower_name == "rating":
                dict_type["type"] = "rating"
                dict_type["max_value"] = 5
                dict_type["color"] = "yellow"
                dict_type["style"] = "star"
            
            # Handling Boolean Type
            elif lower_name in ["boolean", "bool"]:
                dict_type["type"] = "boolean"
            
            # Handling Date, Last Modified Type and Created on Type
            elif lower_name in ["last modified", "created on", "date", "time", "datetime"]:
                if lower_name in ["date", "time", "datetime"]:
                    dict_type["type"] = "date"
                if lower_name == "last modified":
                    dict_type["type"] = "last_modified"
                if lower_name == "created on":
                    dict_type["type"] = "created_on"
                dict_type["date_format"] = "EU"
                dict_type["date_include_time"] = False
                if lower_name in ["time", "datetime"]:
                    dict_type["date_include_time"] = True
                    dict_type["date_time_format"] = "24"
                if lower_name in ["last modified", "created on"]:
                    dict_type["date_include_time"] = True
                    dict_type["timezone"] = "Europe/Zagreb"
            
            # Handling File Type
            elif lower_name == "file":
                dict_type["type"] = "file"
            
            # Handling Phone Number Type
            elif lower_name in ["phone", "phone number", "telephone", "telephone number"]:
                dict_type["type"] = "phone_number"

            # Handling Multiple_Collaborators Type
            elif lower_name in ["collaborators", "multiple collaborators"]:
                dict_type["type"] = "multiple_collaborators"
            
            # Handling Multiple Select Type
            elif lower_name in [enum["name"].lower() for enum in enums]:
                exact_enum = next(enum for enum in enums if enum["name"] == attr["type"])
                dict_type["type"] = "multiple_select"
                dict_type["select_options"] = [{
                    "value": value,
                    "color": "red"
                } for value in exact_enum["literals"]]
            
            # If a Data Type is not defined, it's probably just a text
            else:
                dict_type["type"] = "text"
                dict_type["text_default"] = "" # for now
            
            # print(attr)
            # print(dict(dict_type))
            upgraded_attributes.append(dict(dict_type))
        
        class_attributes[class_name] = upgraded_attributes + upgraded_associations
        
    return class_attributes


def add_class_names_in_attributes(c, atr):
    return {
        f_s(_c.getAttribute("name")): _atr
        for _c, _atr in zip(c, atr)
    }


def sort_class_names_in_associations(class_assoc_name):
    return sorted(class_assoc_name, key=class_assoc_name.get)


def get_full_tables():
    classes = get_classes(for_baserow=False)
    enums = get_enumerations()
    data_types = get_data_types(enums)
    attribute_names = get_attribute_names(classes, data_types)
    class_attributes_names = add_class_names_in_attributes(classes, attribute_names)
    table_fields = get_attributes_with_data_types(class_attributes_names, enums)
    
    return table_fields


def main_et():
    tree = ET.parse('models/online_shopping_model.xmi')
    root = tree.getroot()
    print(root.tag)
    
    for child in root:
        print(child.tag, child.attrib)


if __name__ == '__main__':
    classes = get_classes(for_baserow=False)
    tables = get_classes()
    assoc = get_associations(classes)
    for i, aso in assoc.items():
        print(i, aso)
    final_assoc = get_full_associations("Web User")
    for i in final_assoc:
        print(i)
    # print(classes)
    # print(tables)
    # enums = get_enumerations()
    # print(enums)
    # data_types = get_data_types(enums)
    # print(data_types)
    # attribute_names = get_attribute_names(classes, data_types)
    # print(attribute_names)
    # class_attributes_names = add_class_names_in_attributes(classes, attribute_names)
    # print(class_attributes_names)
    # table_fields = get_attributes_with_data_types(class_attributes_names, enums)
    # for class_name, fields in table_fields.items():
    #     print(class_name, fields)
    """
    
    table_fields_one_fun = get_full_tables()
    for class_name, fields in table_fields_one_fun.items():
        print(class_name, fields)
    """
    
    # associations = get_associations(classes)
    # print(associations)
