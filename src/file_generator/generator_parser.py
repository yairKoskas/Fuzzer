import xml.etree.ElementTree as Et
from generator_factory import GeneratorFactory
from generator import Generator
from pathlib import Path


class GeneratorParser:

    """
    path - the path to the template format xml file
    """
    def __init__(self, path: Path):
        # will throw ParseError if path isn't a valid xml file
        self.xml_tree = Et.parse(path)
        # check that the root tag is a file tag
        root = self.xml_tree.getroot()
        assert root.tag == 'file', 'Root tag in template xml should be a file tag'
        self.file_format = root.attrib
        self.generators = []
        for child in root:
            self.generators.append(self.get_generator(child))

    '''
    get a generator for an xml element
    returns - a generator
    '''
    def get_generator(self, xml_element: Et.Element) -> Union[List[Generator], Generator]:
        if xml_element.tag == 'type':
            generators = []
            for child in xml_element:
                generators.append(self.get_generator(child))
            args = xml_element.attrib
            return GeneratorFactory.get_generator(xml_element.tag)(args.update({'generators': generators}))
        else:
            generator_class = GeneratorFactory.get_generator(xml_element.tag)
            if generator_class:
                return generator_class(**xml_element.attrib)
            return None
