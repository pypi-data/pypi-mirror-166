from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coupling:
	"""Coupling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coupling", core, parent)

	def set(self, coupling_type: enums.CouplingTypeB) -> None:
		"""SCPI: TRIGger[:SEQuence]:OSCilloscope:COUPling \n
		Snippet: driver.trigger.sequence.oscilloscope.coupling.set(coupling_type = enums.CouplingTypeB.AC) \n
		No command help available \n
			:param coupling_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(coupling_type, enums.CouplingTypeB)
		self._core.io.write(f'TRIGger:SEQuence:OSCilloscope:COUPling {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.CouplingTypeB:
		"""SCPI: TRIGger[:SEQuence]:OSCilloscope:COUPling \n
		Snippet: value: enums.CouplingTypeB = driver.trigger.sequence.oscilloscope.coupling.get() \n
		No command help available \n
			:return: coupling_type: No help available"""
		response = self._core.io.query_str(f'TRIGger:SEQuence:OSCilloscope:COUPling?')
		return Conversions.str_to_scalar_enum(response, enums.CouplingTypeB)
