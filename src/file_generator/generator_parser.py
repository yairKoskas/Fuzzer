import xml.etree.ElementTree as Et

from file_generator.generator_factory import GeneratorFactory
from file_generator.generator import Generator, Relation
from file_generator.nested import type, choice, repeat
from file_generator import var
from file_generator import file_creator
from pathlib import Path


class GeneratorParser:
    """
    path - the path to the template format xml file
    """

    def __init__(self, path: Path):
        # will throw ParseError if path isn't a valid xml file
        self.xml_tree = Et.parse(path)
        # check that the root tag is a file tag
        self.root = self.xml_tree.getroot()
        assert self.root.tag == 'file', 'Root tag in template xml should be a file tag'
        self.file_format = self.root.attrib

        # functions to handle different types of tags
        self.handlers = {
            'type' : self._handle_type_generator,
            'block' : self._handle_type_generator,
            'choice' : self._handle_choice_generator,
            'repeat' : self._handle_repeat_generator,
            'custom' : self._handle_custom_generator
        }

        self._parse_variables()

        # parse all user defined types
        self.generators = {}
        for child in self.root:
            self.generators[child.attrib['name']] = self.get_generator(child)

    '''
    returns a FileCreator for the file format
    '''
    def get_creator(self) -> file_creator.FileCreator:
        return file_creator.FileCreator(self.generators['file'], self._vars.values())

    '''
    read all variables from the file
    '''
    def _parse_variables(self):
        self._vars = dict()
        for child in self.root:
            if child.tag == 'var':
                self._vars[child.attrib['name']] = var.Var(**child.attrib)


    '''
    convert the attributes of an element into parameters for the generator

    attributes - dictionary with the attributes
    return - dictionary with attributes after modifications.
    '''
    def _parse_attributes(self, attributes: dict) -> dict:
        res = attributes.copy()
        # replace 'var:x' attributes with the corresponding variable
        for attr in res:
            if res[attr].startswith('var:'):
                var_name = res[attr].split(':')[1]

                if var_name in self._vars:
                    res[attr] = self._vars[var_name]
                else:
                    raise Exception(f'variable {var_name} is not defined')

        return res
    
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
        args['name'] = xml_element.attrib['name']
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
        args = self._parse_attributes(xml_element.attrib)
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
        args = self._parse_attributes(xml_element.attrib)
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
            gen = generator_class(**self._parse_attributes(xml_element.attrib))

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
