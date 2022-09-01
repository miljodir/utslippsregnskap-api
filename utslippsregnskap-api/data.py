import typing
import pandas as pd
import pyarrowfs_adlgen2
import pyarrow.fs


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


def make_categories_ordered(df):
    cats = df.columns[df.dtypes == "category"]
    return df.assign(**{cat: df[cat].cat.as_ordered() for cat in cats})


def excel_to_df(file_path_or_handle, sheet_name=0):
    return (
        pd.read_excel(
            file_path_or_handle,
            sheet_name=sheet_name,
            dtype={
                "Kategori_Nivå1": "category",
                "Kategori_Nivå2": "category",
                "Kategori_Nivå3": "category",
                "Kategori_Nivå4": "category",
                "Komponent": "category",
                "Enhet": "category",
                "TYPE_KOMP": "category",
            },
        )
        .pipe(make_categories_ordered)
        .rename(columns=str.lower)
    )


class DatalakeStorage:
    def __init__(self, fs_handler: pyarrowfs_adlgen2.FilesystemHandler):
        self.fs_handler = fs_handler


    def load_parquet(self, path):
        return pd.read_parquet(path, filesystem=self.fs_handler.to_fs()).astype(
            {"versjon": "category"}
        )

    def save_parquet(self, path, df: pd.DataFrame, overwrite=False):
        try:
            exists_already = self.fs_handler.get_file_info([path])[0]
            if overwrite:
                if exists_already.type == pyarrow.fs.FileType.Directory:
                    raise ValueError(f"Not overwriting directory {exists_already} with single file")
                else:
                    self.fs_handler.delete_file(exists_already.path)
            else:
                raise ValueError(f"Path exists already: {exists_already} and overwrite=False")
        except FileNotFoundError:
            pass  #  ignore
        return df.to_parquet(path, filesystem=self.fs_handler.to_fs())
