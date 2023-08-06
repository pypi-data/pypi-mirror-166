"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1227 import ProSolveMpcType
    from ._1228 import ProSolveSolverType
