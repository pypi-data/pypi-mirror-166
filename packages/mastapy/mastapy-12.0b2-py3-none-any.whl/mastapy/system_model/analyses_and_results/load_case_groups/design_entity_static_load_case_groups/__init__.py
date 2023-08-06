"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5601 import AbstractAssemblyStaticLoadCaseGroup
    from ._5602 import ComponentStaticLoadCaseGroup
    from ._5603 import ConnectionStaticLoadCaseGroup
    from ._5604 import DesignEntityStaticLoadCaseGroup
    from ._5605 import GearSetStaticLoadCaseGroup
    from ._5606 import PartStaticLoadCaseGroup
