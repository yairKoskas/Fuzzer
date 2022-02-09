import ast

'''
A node transformer class that changes every variable in an expression
so it will be read from a dictionary. "name" will be be tranformes to:
"int(self.vars['name'])"
'''
class VarTransformer(ast.NodeTransformer):

    '''
    modify a name node from "<name>" to "int(self._vars['<name>'])"
    '''
    def visit_Name(self, node):
        # self.vars
        self_vars = ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='_vars', ctx=ast.Load())

        # '<name>'
        var_name = ast.Str(s=node.id, ctx=ast.Load())

        # self._vars['<name>']
        var_from_dict = ast.Subscript(value=self_vars, slice=ast.Index(var_name), ctx=ast.Load())

        # int(self._vars['<name>'])
        res = ast.Call(func=ast.Name(id='int', ctx=ast.Load()), args=[var_from_dict], keywords=[])
        ast.copy_location(res, node)
        ast.fix_missing_locations(res)
        return res

'''
An expression that contains variables and python arithmetic operations.
'''
class VarExpression:
    '''
    expression - string that represent the expression (for example 'var1*var2+4')
    vars - dictionay that holds variables by their names
    '''
    def __init__(self, expression: str, vars: dict) -> None:
        self._vars = vars
        exp = ast.parse(expression, mode='eval')
        # swich each appearence of variable like "var" with "int(self._vars['var'])"
        transformer = VarTransformer()
        self._exp = transformer.visit(exp)

        # compile the new expression
        self._exp = compile(self._exp, '', 'eval')

    '''
    Get the current value of the expression as an int.
    '''
    def __int__(self) -> int:
        return eval(self._exp)
        
