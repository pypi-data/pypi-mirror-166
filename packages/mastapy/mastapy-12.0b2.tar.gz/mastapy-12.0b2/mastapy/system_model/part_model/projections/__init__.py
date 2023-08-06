"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2429 import SpecifiedConcentricPartGroupDrawingOrder
    from ._2430 import SpecifiedParallelPartGroupDrawingOrder
