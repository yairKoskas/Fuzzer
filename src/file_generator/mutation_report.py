
'''
This class holds information of one mutation on a generted file.
'''
class MutationReport:
    '''
    field name - name of the mutated field
    description - description of the mutation
    '''
    def __init__(self, field_name : str, description : str) -> None:
        self._field_name = field_name
        self._description = description
        # the names of the parents of the mutated field
        self._parents = [field_name]

    # add a parent to the list of parents
    def add_parent(self, parent_name : str):
        self._parents.append(parent_name)

    def __str__(self) -> str:
        mut_at = 'mutation at :' + ' -> '.join(self._parents[::-1])
        return f'{mut_at}\n{self._description}'
        