## file generation logic
The logic of the file generation and mutaion is located in the [file_generator](../src/file_generator) directory.
<br>The use of the file generation is through the [`GeneratorParser`](../src/file_generator/generator_parser.py) class.
This class parse the XML and return a [`FileCreator`](..\src\file_generator\file_creator.py) class, (which is essentially a wrapper to a generator class) which is capable to create a file and mutate it through the `create_file` function.<br>
A class UML for the file generation  module can be found [here](./file_generation_UML.png).

### the Generator and Field interfaces
Each element in the XML template in converted to a [`Generator`](../src/file_generator/generator.py) object of the same type which holds information about how this field should be generated. Some generator types holds other generators, thus a hierarchy is created (the composite design pattern).<br>
The main method of the `Generator` is the `get_field`, which return a [`Field`](../src/file_generator/field.py) class of the same field type. Each `Field` have an equivalent `Generator` (which created it), but field holds a concrete value instead of information about the XML element. <br>Some fields also inherit from the `ParentField` class, this is special type of Fields that holds additional children field ('composite' elements). Upon a call to the `value` method, such field recursivaly calls to its children `value` method to get the data it containts.<br>
The prmitive ('leaf') generator and field types are located at the [primitives](../src/file_generator/primitives/) directory and the nested ones in the [nested](../src/file_generator/nested/) directory.

Some special case of generator that acts differently in `get_field` are the NoneGenerator (that return nothing), ChoiceGenerator (that return a field from different type), and SetVarGeneratot (that return nothing but change a var value before).

### relations
There are various [`Realtion`](../src/file_generator/relation.py) types, each of them implement the `resolve` method, which gets the target field and return the value of the relation.<br>
Upon a call to the `set_to_relation` method in a `Field`, a nested field calls recursivly to its children `set_to_relation`. A primitive `Field` will ask its parent to resolve the relation for him. A `ParentField` class implements the python operators `__getitem__` and `__contains__` which helps the parent Field to field to find the tharget field and then call to `resolve` on him.

### variables
An int member in a genenrator object can be of type [`VarExpression`](../src/file_generator/var_expression.py) instead of `int`, however it is always converted to `int` at the cration of a `Field` object. At the start of the `crate_file` function, all variables are set randomaly, thus maintaining that all fields in the same file crated from the same values of varibels while still having different values of the variables for each file.

### mutaions
Mutation changes one field in the file, the mutaion happens recursively, each primitive type change self in certain way, and nested types might call to mutaions on one of its children. The mutations are designed in such a way that it is more likely to trigger a bug.<br>

List of possible mutations:<br>
int:
- set the value to an extreme value (e.g maxint, 0...).
- set the value to a random value.
- increment or decrement the value by a small power of 2.

data:
- flip random bits.
- change random byte to random value.

str:
- change random char to random value.

type:
- delete a random child.
- duplicate a random child.
- mutate a random child.

repeat:
- delete a random child.
- mutate a random child.

function:
- swap a random byte in the function after the function activation.
- mutate the field the function acts on.
