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


def _classes(packaged_elements):
    # Classes
    classes = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:Class"]

    class_names = [f_s(_class.getAttribute("name")) for _class in classes]
    print("==== All class names ====")
    print(class_names)
    
    attributes_class_1 = classes[1].getElementsByTagName("ownedAttribute")
    print("==== Attributes of a second class ====")
    print(attributes_class_1)
    
    attributes_class_1_names = [attribute_name.getAttribute("name") for attribute_name in attributes_class_1]
    print("==== Attribute names of a second class ==== ")
    print(attributes_class_1_names)


def _enumerations(packaged_elements):
    # Enumerations
    enumerations = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:Enumeration"]
    
    enumerations_names = [f_s(_enumerator.getAttribute("name")) for _enumerator in enumerations]
    print("==== All enumeration names ====")
    print(enumerations_names)
    
    literals_enumeration_1 = enumerations[1].getElementsByTagName("ownedLiteral")
    print("==== Literals of a second enumerator ====")
    print(literals_enumeration_1)
    
    literals_enumeration_1_names = [literal_name.getAttribute("name") for literal_name in literals_enumeration_1]
    print("==== Literal names of a second class ==== ")
    print(literals_enumeration_1_names)


def _data_types(packaged_elements):
    # Data Types
    data_types = [el for el in packaged_elements if el.getAttribute("xmi:type") == "uml:DataType"]
    
    data_type_names = [f_s(_data_type.getAttribute("name")) for _data_type in data_types]
    print("==== All data type names ====")
    print(data_type_names)
    

def main_et():
    tree = ET.parse('models/online_shopping_model.xmi')
    root = tree.getroot()
    print(root.tag)
    
    for child in root:
        print(child.tag, child.attrib)


def main():
    doc = xml.dom.minidom.parse("models/online_shopping_model.xmi")
    
    # print(doc.nodeName)
    # print(doc.firstChild.tagName)

    xmi = doc.firstChild
    print("xmi", xmi)

    model = xmi.getElementsByTagName("uml:Model")[0]
    print("model", model)
    
    packaged_elements = model.getElementsByTagName("packagedElement")
    print(f"{packaged_elements.length} packaged elements:")
    
    _classes(packaged_elements)
    _enumerations(packaged_elements)
    _data_types(packaged_elements)


if __name__ == '__main__':
    main()
