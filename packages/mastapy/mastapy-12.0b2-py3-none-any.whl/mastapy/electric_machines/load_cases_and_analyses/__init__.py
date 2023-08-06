"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1314 import DynamicForceAnalysis
    from ._1315 import DynamicForceLoadCase
    from ._1316 import EfficiencyMapAnalysis
    from ._1317 import EfficiencyMapLoadCase
    from ._1318 import ElectricMachineAnalysis
    from ._1319 import ElectricMachineBasicMechanicalLossSettings
    from ._1320 import ElectricMachineControlStrategy
    from ._1321 import ElectricMachineEfficiencyMapSettings
    from ._1322 import ElectricMachineFEAnalysis
    from ._1323 import ElectricMachineLoadCase
    from ._1324 import ElectricMachineLoadCaseBase
    from ._1325 import ElectricMachineLoadCaseGroup
    from ._1326 import EndWindingInductanceMethod
    from ._1327 import LeadingOrLagging
    from ._1328 import LoadCaseType
    from ._1329 import LoadCaseTypeSelector
    from ._1330 import MotoringOrGenerating
    from ._1331 import NonLinearDQModelMultipleOperatingPointsLoadCase
    from ._1332 import NumberOfStepsPerOperatingPointSpecificationMethod
    from ._1333 import OperatingPointsSpecificationMethod
    from ._1334 import SingleOperatingPointAnalysis
    from ._1335 import SlotDetailForAnalysis
    from ._1336 import SpecifyTorqueOrCurrent
    from ._1337 import SpeedPointsDistribution
    from ._1338 import SpeedTorqueCurveAnalysis
    from ._1339 import SpeedTorqueCurveLoadCase
    from ._1340 import SpeedTorqueLoadCase
    from ._1341 import SpeedTorqueOperatingPoint
    from ._1342 import Temperatures
