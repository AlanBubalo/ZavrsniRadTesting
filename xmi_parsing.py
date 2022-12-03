from xml.dom import minidom
from random import choice
from env import XMI_FILE

file = minidom.parse(f"models/{XMI_FILE}")
xmi = file.firstChild
# doc = xmi.firstChild
model = xmi.getElementsByTagName("uml:Model")[0]
packaged_elements = model.getElementsByTagName("packagedElement")

remove_percent_20 = lambda x: x.replace("%20", " ")


def get_classes(for_baserow=True):
    classes = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:Class"]
    
    br_tables = [{
        "name": remove_percent_20(el.getAttribute("name")),
        "data": [["/"]], # Empty table with a primary key named "/"
        "first_row_header": True
    } for el in classes]
    
    return br_tables if for_baserow else classes


def get_associations():
    classes = get_classes(for_baserow=False)
    class_associations = {}
    
    for _class in classes:
        class_name = remove_percent_20(_class.getAttribute("name"))
        owned_members = _class.getElementsByTagName("ownedMember")
        owned_ends = (member.getElementsByTagName("ownedEnd") for member in owned_members)
        
        associations = []
        for pair in owned_ends:
            ends = [{
                "name": curr.getAttribute("name").title().replace("_", " "),
                "class_name": next(remove_percent_20(__class.getAttribute("name"))
                                    for __class in classes
                                    if __class.getAttribute("xmi:id") == curr.getAttribute("type")),
                # "aggregation": curr.getAttribute("aggregation"),
                # "lower_value": curr.getElementsByTagName("lowerValue")[0].getAttribute("value"),
                # "upper_value": curr.getElementsByTagName("upperValue")[0].getAttribute("value")
            } for curr in pair]
            
            if ends[0]["class_name"] != class_name:
                associations.append(ends[0])
            associations.append(ends[1])

        class_associations[class_name] = associations
    return class_associations


def get_attributes(classes, data_types):
    list_attributes = {}

    for _class in classes:
        class_name = remove_percent_20(_class.getAttribute("name"))
        owned_attributes = _class.getElementsByTagName("ownedAttribute")
        
        attributes = []
        for attribute in owned_attributes:
            # print("attribute type:", attribute.getAttribute("type"))
            # print("data_type name:", [data_type for data_type in data_types])
            found_type = ""
            if attribute.getAttribute("type") != "":
                found_type = next(data_type["name"] for data_type in data_types
                                  if data_type["id"] == attribute.getAttribute("type"))
            
            attributes.append({
                "name": attribute.getAttribute("name"),
                "type": found_type
            })
        
        # print(f"{attributes=}")
        list_attributes[class_name] = attributes
    return list_attributes


def get_enumerations():
    # Enumerations
    enumerations = [element for element in packaged_elements
                    if element.getAttribute("xmi:type") == "uml:Enumeration"]
    all_literals = [enumeration.getElementsByTagName("ownedLiteral")
                    for enumeration in enumerations]

    return [{
        "id": enum.getAttribute("xmi:id"),
        "name": enum.getAttribute("name"),
        "literals": {lit.getAttribute("name")
                     for lit in literals}
    } for enum, literals in zip(enumerations, all_literals)]


def get_data_types():
    # Data Types
    data_type_elements = (element for element in packaged_elements
                          if element.getAttribute("xmi:type") == "uml:DataType")
    
    data_types = [{
        "id":  data_type.getAttribute("xmi:id"),
        "name" : remove_percent_20(data_type.getAttribute("name"))
    } for data_type in data_type_elements]
    
    data_types.extend(get_enumerations())
    return data_types


def get_ready_attributes(class_attributes):
    colors = (
        "light-blue", "blue", "dark-blue",
        "light-green", "green", "dark-green",
        "light-yellow", "yellow", "dark-yellow",
        "light-red", "red", "dark-red",
        "light-gray", "gray", "dark-gray"
    )
    
    enums = get_enumerations()
    for class_name, attributes in class_attributes.items():
        upgraded_attributes = []
        for attr in attributes:
            field = {}          
            field["name"] = attr["name"].title().replace("_", " ")
            lower_name = attr["type"].lower()
            
            # Handling Number Type
            if lower_name in ["integer", "int", "unsigned integer", "unsigned int", "float", "real"]:
                field["type"] = "number"
                field["number_decimal_places"] = 0
                field["number_negative"] = True
                if lower_name in ["unsigned integer", "unsigned int"]:
                    field["number_negative"] = False
                if lower_name in ["float", "real"]:
                    field["number_decimal_places"] = 5
            
            # Handling Long Text Type
            elif lower_name in ["blob", "text", "long text"]:
                field["type"] = "long_text"
            
            # Handling URL Type
            elif lower_name == "url":
                field["type"] = "url"
                
            # Handling Email Type
            elif lower_name == "email":
                field["type"] = "email"
            
            # Handling Rating Type
            elif lower_name == "rating":
                field["type"] = "rating"
                field["max_value"] = 5
                field["color"] = "yellow"
                field["style"] = "star"
            
            # Handling Boolean Type
            elif lower_name in ["boolean", "bool"]:
                field["type"] = "boolean"
            
            # Handling Date, Last Modified Type and Created on Type
            elif lower_name in ["last modified", "created on", "date", "time", "datetime"]:
                if lower_name in ["date", "time", "datetime"]:
                    field["type"] = "date"
                if lower_name == "last modified":
                    field["type"] = "last_modified"
                if lower_name == "created on":
                    field["type"] = "created_on"
                field["date_format"] = "EU"
                field["date_include_time"] = False
                if lower_name in ["time", "datetime"]:
                    field["date_include_time"] = True
                    field["date_time_format"] = "24"
                if lower_name in ["last modified", "created on"]:
                    field["date_include_time"] = True
                    field["timezone"] = "Europe/Zagreb"
            
            # Handling File Type
            elif lower_name == "file":
                field["type"] = "file"
            
            # Handling Phone Number Type
            elif lower_name in ["phone", "phone number", "telephone", "telephone number"]:
                field["type"] = "phone_number"

            # Handling Multiple_Collaborators Type
            elif lower_name in ["collaborators", "multiple collaborators"]:
                field["type"] = "multiple_collaborators"
            
            # Handling Multiple Select Type
            elif lower_name in [enum["name"].lower() for enum in enums]:
                exact_enum = next(enum for enum in enums if enum["name"] == attr["type"])
                field["type"] = "multiple_select"
                field["select_options"] = [{
                    "value": value,
                    "color": choice(colors)
                } for value in exact_enum["literals"]]
            
            # If a Data Type is not defined or is a string, it's probably just a text
            else:
                field["type"] = "text"
                field["text_default"] = "" # for now
            
            upgraded_attributes.append(field)
            
        class_attributes[class_name] = upgraded_attributes
        
    return class_attributes


def get_full_tables():
    classes = get_classes(for_baserow=False)
    data_types = get_data_types()
    attributes = get_attributes(classes, data_types)
    
    return get_ready_attributes(attributes)


"""
if __name__ == '__main__':
    classes = get_classes(for_baserow=False)
    #tables = get_classes()
    #assoc = get_associations(classes)
    #for i, aso in assoc.items():
    #    print(i, aso)
    # print(classes)
    # print(tables)
    # enums = get_enumerations()
    # print(enums)
    data_types = get_data_types()
    # print(data_types)
    attribute = get_attributes(classes, data_types)
    print(attribute)
    # table_fields = get_ready_attributes(attribute_names)
    # for class_name, fields in table_fields.items():
    #     print(class_name, fields)
"""
