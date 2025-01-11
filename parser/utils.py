import string
from xml.etree.ElementTree import Element

parsing_function = None

def set_parsing_function(func):
    """
    Sets the parsing function.

    Args:
        func: the function to be set
    """

    global parsing_function
    parsing_function = func

def get_parsing_function():
    """
       Returns:
           func: the current parsing function
    """
    return parsing_function

def compare_tag(element: Element, value: string):
    """
    Compares XML node tag against a string. Use when XML element tag looks like <tag>{"<link>"}.

    Args:
        element (Element): XML node
        value (str): string to compare against

    Returns:
        Bool: if XML node tag matches the string
    """

    if "}" in element.tag:
        tag = element.tag.split("}")[1]
    else: tag = element.tag

    return tag == value

