"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1406 import AssemblyMethods
    from ._1407 import CalculationMethods
    from ._1408 import InterferenceFitDesign
    from ._1409 import InterferenceFitHalfDesign
    from ._1410 import StressRegions
    from ._1411 import Table4JointInterfaceTypes
