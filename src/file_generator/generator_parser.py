import xml.etree.ElementTree as Et
from pathlib import Path
import copy

from file_generator.generator_factory import GeneratorFactory
from file_generator.generator import Generator, relation
from file_generator.nested import type, choice, repeat, function
from file_generator import var
from file_generator import var_expression
from file_generator import file_creator
from file_generator.primitives import set_var
from file_generator import relation
from exception import FuzzerException


class GeneratorParser:
    """
    path - the path to the template format xml file
    """

    def __init__(self, path: Path):
        # will throw ParseError if path isn't a valid xml file
        try:
            self.xml_tree = Et.parse(path)
        except:
            raise FuzzerException("problem parsing xml structure")

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
            'custom' : self._handle_custom_generator,
            'function' : self._handle_function_generator,
            'set' : self._handle_set_var_generator
        }

        self._parse_variables()

        # parse all user defined types
        self.types = dict()
        for child in self.root:
            if child.tag == 'type':
                self.types[child.attrib['name']] = child

        self.file_generator = self.get_generator(self.types['file'])

    '''
    returns a FileCreator for the file format
    '''
    def get_creator(self) -> file_creator.FileCreator:
        return file_creator.FileCreator(self.file_generator, self._vars.values())

    '''
    read all variables from the file
    '''
    def _parse_variables(self):
        self._vars = dict()
        for child in self.root:
            if child.tag == 'var':
                self._vars[child.attrib['name']] = var.Var(**child.attrib)

    '''
    convert an attribute of an element into parameters for the generator
    '''
    def _parse_attribute(self, attr : str):
        if attr.startswith('var:'):
            expression = attr.split(':')[1]

            return var_expression.VarExpression(expression, self._vars)
        return attr

    '''
    convert the attributes of an element into parameters for the generator

    attributes - dictionary with the attributes
    return - dictionary with attributes after modifications.
    '''
    def _parse_attributes(self, attributes: dict) -> dict:
        res = attributes.copy()
        # replace 'var:x' attributes with the corresponding variable
        for attr in res:
            res[attr] = self._parse_attribute(res[attr])

        return res
    
    '''
    create type geneartor
    returns - a generator
    '''
    def _handle_type_generator(self, xml_element: Et.Element):
        generators = list()
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
    parse parameters for type element
    i.e replace every appearence  of the param
    '''
    def _replace_parameters(self, xml_element: Et.Element, params_names: list, params_values: list):
        num_of_params = len(params_names)
        element = copy.deepcopy(xml_element)
        element.attrib.pop('params')

        for child in element.iter():
            for attr in child.attrib:
                if attr != 'name':
                    for i in range(num_of_params):
                        child.attrib[attr] = child.attrib[attr].replace(params_names[i], params_values[i])


        return element
        
    '''
    create set_var geneartor
    returns - a generator
    '''
    def _handle_set_var_generator(self, xml_element: Et.Element):
        args = self._parse_attributes(xml_element.attrib)
        args['vars'] = self._vars
        return set_var.SetVarGenerator(**args)

    '''
    create custom geneartor
    returns - a generator
    '''
    def _handle_custom_generator(self, xml_element: Et.Element):
        # first we want to replace parameters
        t = xml_element.attrib['type']
        type_element = self.types[t]
        if 'params' in type_element.attrib:
            params_names = type_element.attrib['params'].split(',')
            params_names = list(map(lambda x: x.lstrip(), params_names))
            params_values = xml_element.attrib['params'].split(',')
            params_values = list(map(lambda x: x.lstrip(), params_values))

            if (len(params_names) != len(params_values)):
                raise FuzzerException(f'expected {len(params_names)} parameters for type {t} but got {len(params_values)}')

            type_element = self._replace_parameters(type_element, params_names, params_values)

        return self._handle_type_generator(type_element)

    '''
    create function geneartor
    returns - a generator
    '''
    def _handle_function_generator(self, xml_element: Et.Element):
        generators = []
        for child in xml_element:
            gen = self.get_generator(child)
            if gen is not None:
                generators.append(gen)

        # parse the params attribute
        if 'params' in xml_element.attrib:
            params = xml_element.attrib['params'].split(',')
            params = list(map(lambda x: x.lstrip(), params))
            params = list(map(self._parse_attribute, params))
            del xml_element.attrib['params']

        else:
            params = []

        args = self._parse_attributes(xml_element.attrib)
        args['generator'] = generators[0]
        args['params'] = params
            
        return function.FunctionGenerator(**args)

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
                    rel = relation.relation_by_name[child.attrib['type']](**child.attrib)
                    gen.set_relation(rel)

            return gen

    '''
    get a generator for an xml element
    returns - a generator
    '''
    def get_generator(self, xml_element: Et.Element) -> Generator:
        # find what function should hanle the parsing of the tag
        if xml_element.tag in self.handlers:
            handler = self.handlers[xml_element.tag]
            return handler(xml_element)

        # if no special case, then it is primitive type
        return self._handle_primitive_generator(xml_element)
