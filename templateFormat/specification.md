# Input template format specification

## structure of the file
The root of the xml must be `<file name="filename">`. Inside the `<file>` tag you can define variables and custom types.
The last `type` tag must have the name `file` and represents the whole file (this is what will be generated).<br>
example:
```xml
<file name="fileFormat">
    <var name="var1" .../>
    <var name="var2" .../>

    <type name="type1">
        <!-- some data -->
    </type>

    <type name="type2">
        <!-- some data -->
    </type>

    <!-- the file structure -->
    <type name="file">
        <!-- some data -->
    </type>

</file>
```

## Using primitive types
There are a few basic types you can use to specify the fields in the format. Every field is required to have the name attribute.<br>

### int
`int` represents a field with numerical value.<br>
Attributes:
- `size`: size of the integer in bytes (required).
- `value`: value of the integer.
- `min_val`: minimum value of the integer (meaningless if `value` is given).
- ``max_val`: maximum value of the integer (meaningless if `value` is given).
- ``endian`: endian - must be `little` or `big` (default is `little`).

Example
```xml
<int name="name" size="4" max_val="20" endian='big'/>
```

### str
`str` represents an ascii string.<br>
Attributes:
- `size`: size of the string in bytes.
- `value`: value of the string.
- `min_size`: minimum value of the string (meaningless if `size` is given).
- `max_size`: maximum value of the string (meaningless if `size` is given, default value is 20).

Example
```xml
<str name="name" size="4"/>
```

### data
`data` represents an arbirary binary data without certain structure.<br>
Attributes:
- `size`: size of the data in bytes.
- `value`: value of the data (as a hex string).
- `min_size`: minimum value of the data (meaningless if `size` is given).
- `max_size`: maximum value of the data (meaningless if `size` is given, default value is 20).

Example
```xml
<data name="name" value="deadbeef"/>
```

### padding
`padding` pad the file to a certain alignment.<br>
Attributes:
- `alignment`: the offset of the end of the padding will be a multiple of `alignment`.
- `value`: value to pad with.

Example
```xml
<data name="data" size="3"/>
<padding name="pad" value="255" alignment="8">
```
This will pad the content to be a multiple of 8. In our example the value of `pad` will be `'\xff'*5`.

### none
`none` basically does nothing. can be used for example to fill a `choice` tag to make optional field.<br>


## Using non-primitive types
There are some nested types which contains other elements:

### choice
`choice` choose one element from a group of elements inside the `choice` tag.<br>

Example
```xml
<chice name="name">
    <str name="poss1" value="poss1"/>
    <str name="poss2" value="poss2"/>
    <str name="poss3" value="poss3"/>
</choice>
```
In this example, when the data will be generated, the content will be choosed from `poss1`, `poss2` and `poss3`.

### repeat
`repeat` repeats a certain element multiple times.<br>
Attributes:
- `times`: times to repeat the element.
- `min_times`: minimum amount of times to repeat the element (meaningless if `times` is given).
- `max_times`: maximum amount of times to repeat the element (meaningless if `times` is given, default value is 20).

Example
```xml
<repeat name="name" times="4">
    <str name="str1" value="hello"/>
</repeat>
```
The value of the element in the example will be: `hellohellohellohello`.

### block
`block` unites multiple elements into one. It is essentially an anonymous `type` element<br>

Example
```xml
<block name="name">
    <str name="str1" value="hello"/>
    <int name="int1" size="4" value="42"/>
    <padding name="pad1" alignment="16"/>
</block>
```

### custom
`custom` is an appearance of an type element defined before<br>
Attributes:
- `type`: type of the element (must be a type that defined before the custom element).

Example
```xml
<type name="type1">
    <!-- some data -->
</type>
<custom name="name" type="type1">
```

### function
`function` to activate a function on some data in order to maintain more complex structure. The function acts on the field it contains.<br>
The function must get as fisrt parameter a bytes object (the data to act on), and can get additional int type parameters.
the function must return bytes object.

Attributes:
- `module_name`: the name of the module where the function located (should be full python-style path from the directory you run the fuzzer).
- `function_name`: name of the function within the module.
- `params`: parameters to the functions after the data, seperated by comma

Example
```python
def foo(data : bytes, param1 : int, param2 : int) -> bytes:
    # do some stuff
    return stuff
```
```xml
<function name="function" module_name="path.to.foo" function_name="foo" params="1,2">
    <data name="data_to_function" size="20">
</function>
```

## Relations
You can set the value of a `str`, `int` or `data` tag to be a relation, i.e be dependent on another field. A relation can be defined with the `relation` tag inside the element tag. A relation tag should have `type` attribute, which specify the kind of relation, and `target`, which specify the name of the field to relate to.<br />
The types of relation:
- `size` - size of a certain field.
- `offset` - offset of a certain field in the current block.
- `absOffset` - offset of a certain field in the whole file.
- `function` - set the field value to be `f(target)` where f is a given function. this type of relation requires 2 additional attributes:`module_name` and `function_name` (used exactly the same as in the `function` field).

Example:
```xml
<file name="image">
    <str name="magic" value="IMG">
    <int name="contentSize" size="4"> 
        <relation type="size" target="fileContent">
    </int>
    <data name="fileContent">
</file>
```

## Variables
Relations can only be used to moify the value of a certain element, but variables can be used to set any attribute.
Varibales defined by the name `var` at the start of a file and have the following attributes:
- `name` - name of the variable.
- `max_val` - maximal value of the element.
- `min_val` - minimal value of the element.

A variable can be used by giving `var:varname` as an attribute to any attribute that accepts integers.
You can also use variables with expressions containing python arithmetic operators, for example `var:var1*var2+3`.

Example:
```xml
<file name="fileFormat">
    <var name="helloTimes" min_val="1" max_val="10"/>

    <type name="file">
        <int name='timesOfHello' size="1" value="var:helloTimes">

        <repeat name="repeatHello" times="var:helloTimes">
            <str name="hello" value="hello"/>
        </repeat>
    </type>
</file>
```
In this example, the value of the `timesOfHello` integer will be equal to the number of times `hello` string is repeated.

### Changing variables
You can change a variable in the process of generating the data with the `set_var` field, it contains 2 attributes: `var_name` and `value`. This can be used to create simple loops and relations between variables.<br>
Example:
```xml
<file name="fileFormat">
    <var name="num" min_val="1" max_val="1"/>

    <type name="file">
        <repeat name="one_to_three" times="3">
            <int name="num" value="var:num"/>
            <set_var var_name="num" value="var:num+1"/>
        </repeat>
    </type>
</file>
```