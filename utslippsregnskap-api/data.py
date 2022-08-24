import typing


def to_tree(records: typing.Iterable[typing.List[str]]):
    """Create tree of containing each record, skipping non-str values

    Example:
    >>> to_tree([["a", "b", "c"], ["a", "c"]])
    {
        "a": {
            "b": {
                 "c": {}
            },
            "c": {}
        }
    }
    """
    tree = {}
    for record in records:
        current_node = tree
        for value in record:
            if not isinstance(value, str):
                break
            if value not in current_node:
                current_node[value] = {}
            current_node = current_node[value]
    return tree


def pretty_tree(tree: dict, key_name="kategori", child_name="nivaa"):
    """Take a tree where each node is a dict and turn it into a list

    Example:
    >>> pretty_tree({
        "a": {
            "b": {
                 "c": {}
            },
            "c": {}
        }
    })
    ...
    [
        {"kategori": "a", "nivaa": [
             {"kategori": "b", "nivaa": [
                  {"kategori": "c"}
            ]},
            {"kategori": "c"}
        ]}
    ]
    """
    values = []
    for key, children in tree.items():
        if not children:
            values.append({key_name: key})
        else:
            values.append({key_name: key, child_name: pretty_tree(children, key_name, child_name)})
    return values
