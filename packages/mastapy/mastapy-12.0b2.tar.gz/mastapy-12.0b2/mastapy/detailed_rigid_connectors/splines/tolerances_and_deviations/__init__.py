"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1384 import FitAndTolerance
    from ._1385 import SAESplineTolerances
