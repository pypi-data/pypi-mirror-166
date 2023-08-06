"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5587 import AbstractDesignStateLoadCaseGroup
    from ._5588 import AbstractLoadCaseGroup
    from ._5589 import AbstractStaticLoadCaseGroup
    from ._5590 import ClutchEngagementStatus
    from ._5591 import ConceptSynchroGearEngagementStatus
    from ._5592 import DesignState
    from ._5593 import DutyCycle
    from ._5594 import GenericClutchEngagementStatus
    from ._5595 import LoadCaseGroupHistograms
    from ._5596 import SubGroupInSingleDesignState
    from ._5597 import SystemOptimisationGearSet
    from ._5598 import SystemOptimiserGearSetOptimisation
    from ._5599 import SystemOptimiserTargets
    from ._5600 import TimeSeriesLoadCaseGroup
