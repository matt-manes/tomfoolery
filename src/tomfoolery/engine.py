import ast
from typing import Any

import black
from pathier import Pathier, Pathish

from tomfoolery import utilities

root = Pathier(__file__).parent


class TomFoolery:
    def __init__(self):
        self.module = ast.Module([], [])
        self.imports: list[ast.ImportFrom | ast.Import] = []
        self.classes: list[ast.ClassDef] = []

    @property
    def source(self) -> str:
        """Returns the source code this object represents."""
        self.module.body = [self.imports, self.classes]  # type: ignore
        return ast.unparse(self.module)

    # Seat |===================================== Import Nodes =====================================|

    @property
    def dacite_import_node(self) -> ast.Import:
        return ast.Import([ast.alias("dacite")])

    @property
    def dataclass_import_node(self) -> ast.ImportFrom:
        return ast.ImportFrom(
            "dataclasses", [ast.alias("dataclass"), ast.alias("asdict")], 0
        )

    @property
    def import_nodes(self) -> list[ast.Import | ast.ImportFrom]:
        return [
            self.dacite_import_node,
            self.dataclass_import_node,
            self.pathier_import_node,
            self.typing_extensions_import_node,
        ]

    @property
    def pathier_import_node(self) -> ast.ImportFrom:
        return ast.ImportFrom(
            "pathier", [ast.alias("Pathier"), ast.alias("Pathish")], 0
        )

    @property
    def typing_extensions_import_node(self) -> ast.ImportFrom:
        return ast.ImportFrom("typing_extensions", [ast.alias("Self")])

    # Seat |======================================== Nodes ========================================|

    @property
    def dataclass_node(self) -> ast.Name:
        """A node representing `@dataclass`."""
        return ast.Name("dataclass", ast.Load())

    @property
    def dump_node(self) -> ast.FunctionDef:
        """The dumping function for the generated `dataclass`."""
        return self.nodes_from_file(root / "_dump.py")[0]  # type: ignore

    @property
    def load_node(self) -> ast.FunctionDef:
        """The loading function for the generated `dataclass`."""
        return self.nodes_from_file(root / "_load.py")[0]  # type: ignore

    def nodes_from_file(self, file: Pathish) -> list[ast.stmt]:
        """Return ast-parsed module body from `file`."""
        return ast.parse(Pathier(file).read_text()).body

    # Seat |======================================= Builders =======================================|

    def annotated_assignments_from_dict(
        self, data: dict[str, Any]
    ) -> list[ast.AnnAssign]:
        """Return a list of annotated assignment nodes built from `data`.

        Any values in `data` that are themselves a dictionary, will have a `dataclass` built and inserted in `self.classes`.

        The field for that value will be annotated as an instance of that secondary `dataclass`."""
        assigns = []
        for key, val in data.items():
            if type(val) == dict:
                self.classes.append(self.build_dataclass(key, val))
                assigns.append(
                    self.build_annotated_assignment(
                        key, utilities.key_to_classname(key), False
                    )
                )
            else:
                assigns.append(self.build_annotated_assignment(key, val))
        return assigns

    def build_annotated_assignment(
        self, name: str, val: Any, evaluate_type: bool = True
    ) -> ast.AnnAssign:
        """Return an annotated assignment node with `name` and an annotation based on the type of `val`.

        If `evaluate_type` is `False`, then `val` will be used directly as the type annotation instead of `type(val).__name__`."""
        return ast.AnnAssign(
            ast.Name(name, ast.Store()),
            ast.Name(utilities.build_type(val) if evaluate_type else val, ast.Load()),
            None,
            1,
        )

    def build_dataclass(
        self, name: str, data: dict[str, Any], add_methods: bool = False
    ) -> ast.ClassDef:
        """Build a `dataclass` with `name` from `data` and insert it into `self.classes`.

        If `add_methods` is `True`, `load()` and `dump()` functions will be added to the class."""
        class_ = ast.ClassDef(
            utilities.key_to_classname(name),
            [],
            [],
            [self.annotated_assignments_from_dict(data)],
            [self.dataclass_node],
        )
        if add_methods:
            class_.body.extend([self.load_node, self.dump_node])
        return class_

    # Seat |======================================== Main ========================================|

    def generate(self, name: str, data: dict[str, Any]) -> str:
        """Generate a `dataclass` with `name` from `data` and return the source code.

        Currently, all keys in `data` and any of its nested dictionaries must be valid Python variable names."""
        for node in self.import_nodes:
            if node not in self.imports:
                self.imports.append(node)
        dataclass = self.build_dataclass(name, data, True)
        self.classes.append(dataclass)
        return self.source

    def generate_from_file(self, path: Pathish, write_result: bool = False) -> str:
        """Generate a `dataclass` named after the file `path` points at and return the source code.

        Can be any `.toml` or `.json` file where all keys are valid Python variable names.

        If `write_result` is `True`, the source code will be written to a file of the same name as `path`, but with a `.py` extension."""
        path = Pathier(path)
        name = path.stem
        data = path.loads()
        src = self.generate(name, data)
        src = src.replace("filepath", path.name)
        src = black.format_str(src, mode=black.Mode())  # type: ignore
        if write_result:
            path.with_suffix(".py").write_text(src)
        return src
