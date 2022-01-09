import xml.etree.ElementTree as Et
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))  # import shit, gotta fix this

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
        self.generators = {}
        for child in root:
            self.generators[child.attrib['name']] = self.get_generator(child)

    '''
    get a generator for an xml element
    returns - a generator
    '''

    def get_generator(self, xml_element: Et.Element) -> Generator:
        if xml_element.tag == 'type':
            generators = []
            for child in xml_element:
                gen = self.get_generator(child)
                if gen is not None:
                    generators.append(gen)
            args = xml_element.attrib
            args.update({'generators': generators})
            return GeneratorFactory.get_generator(xml_element.tag)(**args)

        if xml_element.tag == 'custom':
            t = xml_element.attrib['type']
            if t in self.generators:
                return self.generators[t]

        generator_class = GeneratorFactory.get_generator(xml_element.tag)
        if generator_class:
            return generator_class(**xml_element.attrib)
        return None
