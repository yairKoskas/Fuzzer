import xml.etree.ElementTree as Et

from file_generator.generator_factory import GeneratorFactory
from file_generator.generator import Generator, Relation
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
            gen = generator_class(**xml_element.attrib)

            # add relation
            for child in xml_element:
                if child.tag == 'relation':
                    gen.set_relation(Relation(**child.attrib))

            return gen
            
        return None
