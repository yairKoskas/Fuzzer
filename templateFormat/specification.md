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


### Relations
You can set the value of a `str` or `int` tag to be a relation, i.e be dependent on another field. A relation can be defined woth the `relation` tag. A relation tag should have `type` attribute, which specify the kind of relation, and `target`, which specify the name of the field to relate to.<br />
The types of relation:
- `size` - size of a certain field.
- `offset` - offset of a certain field on the file.
- TODO: add more.

Example:
```xml
<file name="image">
    <str name="magic" value="IMG">
    <int name="contentSize" size="4"> <relation type="size" target="fileContent"> </int>
    <data name="fileContent">
</file>
```