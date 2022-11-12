import xml.dom.minidom
import xml.etree.ElementTree as ET

f_s = lambda x: x.replace("%20", " ")


class BaseClass(object):
    def __init__(self, class_type):
        self._type = class_type


def ClassFactory(name, arg_names, BaseClass=BaseClass):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # here, the arg_names variable is the one passed to the
            # ClassFactory call
            if key not in arg_names:
                raise TypeError("Argument %s not valid for %s" 
                    % (key, self.__class__.__name__))
            setattr(self, key, value)
        BaseClass.__init__(self, name[:-len("Class")])
    new_class = type(name, (BaseClass,),{"__init__": __init__})
    return new_class


def get_attributes(classes):
    attributes_class_1 = classes[1].getElementsByTagName("ownedAttribute")
    print("==== Attributes of a second class ====")
    print(attributes_class_1)
    
    attributes_class_1_names = [attribute_name.getAttribute("name") for attribute_name in attributes_class_1]
    print("==== Attribute names of a second class ==== ")
    print(attributes_class_1_names)


def get_classes():
    # Classes
    classes = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:Class"]
    
    br_tables = [{
        "name": f_s(el.getAttribute("name")),
        "data": [["/"]], # Empty table with a primary key named "/"
        "first_row_header": True
    } for el in classes]
    
    return br_tables

    _classes = [{
        "id": el.getAttribute("xmi:id"),
        "name": f_s(el.getAttribute("name")),
        "visibility": el.getAttribute("visibility"),
        "is_abstract": bool(el.getAttribute("isAbstract")),
        "is_final_specialization": bool(el.getAttribute("isFinalSpecialization")),
        "is_leaf": bool(el.getAttribute("isLeaf")),
        "is_active": bool(el.getAttribute("isActive")),
    } for el in classes]
    # print("==== _CLASSES ====")
    # print(_classes)
    
    
    # print("==== TABLES ====")
    # print(br_tables)
    
    # Get any class value you want ex. "name"
    class_names = [c["name"] for c in _classes]
    # print("==== All class names ====")
    # print(class_names)
    
    # get_attributes(classes)


def get_enumerations():
    # Enumerations
    enumerations = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:Enumeration"]
    
    enumerations_names = [enumeration.getAttribute("name") for enumeration in enumerations]
    # print("==== All enumeration ====")
    # print(enumerations_names)
    
    all_literals = [enumeration.getElementsByTagName("ownedLiteral") for enumeration in enumerations]
    # print("==== Literals elements of all enumerations ====")
    # print(all_literals)
    
    en_literals = {name: {lit.getAttribute("name")
                          for lit in literals}
                   for name, literals in zip(enumerations_names, all_literals)}
    # print("==== Enumerations with their literals ==== ")
    # print(en_literals)

    return en_literals

def get_data_types():
    # Data Types
    __data_types__ = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:DataType"]
    
    data_types = [{
        "name" : _data_type.getAttribute("name"),
        "id":  _data_type.getAttribute("xmi:id")
        } for _data_type in __data_types__]
    print("==== All data types ====")
    print(data_types)


def main_et():
    tree = ET.parse('models/online_shopping_model.xmi')
    root = tree.getroot()
    print(root.tag)
    
    for child in root:
        print(child.tag, child.attrib)


doc = xml.dom.minidom.parse("models/online_shopping_model.xmi")

# print(doc.nodeName)
# print(doc.firstChild.tagName)

xmi = doc.firstChild
# print("xmi", xmi)

model = xmi.getElementsByTagName("uml:Model")[0]
# print("model", model)

packaged_elements = model.getElementsByTagName("packagedElement")
# print(f"{packaged_elements.length} packaged elements:")

def main():
    # get_classes()
    get_enumerations()
    # get_data_types()
    pass


if __name__ == '__main__':
    main()
