"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2287 import ClutchConnection
    from ._2288 import ClutchSocket
    from ._2289 import ConceptCouplingConnection
    from ._2290 import ConceptCouplingSocket
    from ._2291 import CouplingConnection
    from ._2292 import CouplingSocket
    from ._2293 import PartToPartShearCouplingConnection
    from ._2294 import PartToPartShearCouplingSocket
    from ._2295 import SpringDamperConnection
    from ._2296 import SpringDamperSocket
    from ._2297 import TorqueConverterConnection
    from ._2298 import TorqueConverterPumpSocket
    from ._2299 import TorqueConverterTurbineSocket
