import string
from xml.etree.ElementTree import Element

parsing_function = None

def set_parsing_function(func):
    global parsing_function
    parsing_function = func

def get_parsing_function():
    return parsing_function

def compare_tag(element: Element, value: string):
    if "}" in element.tag:
        tag = element.tag.split("}")[1]
    else: tag = element.tag

    return tag == value

