"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1350 import DetailedRigidConnectorDesign
    from ._1351 import DetailedRigidConnectorHalfDesign
