import xml.etree.ElementTree as Et
from generator_factory import GeneratorFactory
from generator import Generator
from pathlib import Path


class GeneratorParser:

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

    def get_generator(self, xml_element: Et.Element):
        if xml_element.tag == 'type':
            generators = []
            for child in xml_element:
                generators.append(self.get_generator(child))
            generator_args = xml_element.attrib
            generator_args['generators'] = generators
            return GeneratorFactory.get_generator(xml_element.tag)(**generator_args)
        else:
            generator_class = GeneratorFactory.get_generator(xml_element.tag)
            if generator_class:
                return generator_class(**xml_element.attrib)
            return None
