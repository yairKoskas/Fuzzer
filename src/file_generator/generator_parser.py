import xml.etree.ElementTree as Et

from file_generator.generator_factory import GeneratorFactory
from file_generator.generator import Generator, Relation
from file_generator.nested import type, choice, repeat
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

        # functions to handle different types of tags
        self.handlers = {
            'type' : self._handle_type_generator,
            'choice' : self._handle_choice_generator,
            'repeat' : self._handle_repeat_generator,
            'custom' : self._handle_custom_generator
        }

        self.generators = {}
        for child in root:
            self.generators[child.attrib['name']] = self.get_generator(child)

    '''
    create type geneartor
    returns - a generator
    '''
    def _handle_type_generator(self, xml_element: Et.Element):
        generators = []
        for child in xml_element:
            gen = self.get_generator(child)
            if gen is not None:
                generators.append(gen)
        args = xml_element.attrib
        args['generators'] = generators
        return type.TypeGenerator(**args)

    '''
    create choice geneartor
    returns - a generator
    '''
    def _handle_choice_generator(self, xml_element: Et.Element):
        generators = []
        for child in xml_element:
            gen = self.get_generator(child)
            if gen is not None:
                generators.append(gen)
        args = xml_element.attrib
        args['generators'] = generators
        return choice.ChoiceGenerator(**args)

    '''
    create repeat geneartor
    returns - a generator
    '''
    def _handle_repeat_generator(self, xml_element: Et.Element):
        generators = []
        for child in xml_element:
            gen = self.get_generator(child)
            if gen is not None:
                generators.append(gen)
        args = xml_element.attrib
        args['generator'] = generators[0]
        return repeat.RepeatGenerator(**args)

    '''
    create custom geneartor
    returns - a generator
    '''
    def _handle_custom_generator(self, xml_element: Et.Element):
        t = xml_element.attrib['type']
        if t in self.generators:
            return self.generators[t].copy_with_name(xml_element.attrib['name'])

    '''
    create primitive geneartor
    returns - a generator
    '''
    def _handle_primitive_generator(self, xml_element: Et.Element):
        generator_class = GeneratorFactory.get_generator(xml_element.tag)
        if generator_class:
            gen = generator_class(**xml_element.attrib)

            # add relation
            for child in xml_element:
                if child.tag == 'relation':
                    gen.set_relation(Relation(**child.attrib))

            return gen

    '''
    get a generator for an xml element
    returns - a generator
    '''
    def get_generator(self, xml_element: Et.Element) -> Generator:
        if xml_element.tag in self.handlers:
            handler = self.handlers[xml_element.tag]
            return handler(xml_element)

        return self._handle_primitive_generator(xml_element)
