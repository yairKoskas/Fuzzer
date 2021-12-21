# Input template format specification

### Defining data types
You can define your own data types by using the tag `type`, it only requires the `name` propery. The Structure of the file itself can be defined by `file`, there should be only 1 `file` tag.<br />
example:
```xml
<type name="type1">
    <!-- some data -->
</type>

<type name="type2">
    <!-- some data -->
</type>

<file name="fileFormat">

    <!-- some data -->

</file>
```

### Using predefined data types
There are a few basic types you can use to specify the fields in the format:
- `int` - a number.
- `str`- a string.
- `data` - arbitrary data with no clear structure.

Each of the tags can have the following attributes:
- `name` - name of the field.
- `size` - size of the field in bytes (optimal).
- `value` - value of the field (optimal).
- TODO: add more types

Additionally, You can use user defined types with `custom` tag. The `custom` tag only have the `name` attribute and the `type` attribute (whoch specify the name of the type).<br />
Example:
```xml
<type name="type2">
    <str name="aString" value="ABCD">
    <int name="aNumber" value="70" size="4">
    <int name="anotherNumber" size="2">
    <data name="fileContent">
    <custom name="usingType1" type="type1">
</type>
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