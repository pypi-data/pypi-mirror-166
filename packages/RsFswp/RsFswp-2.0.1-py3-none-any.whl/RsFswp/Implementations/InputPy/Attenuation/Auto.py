from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Auto:
	"""Auto commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("auto", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: INPut:ATTenuation:AUTO \n
		Snippet: driver.inputPy.attenuation.auto.set(state = False) \n
		This command turns automatic configuration of the attenuation on and off. \n
			:param state: ON | 1 Automatically defines the ideal attenuation based on the current signal level. OFF | 0 Allows you to define the attenuation manually with method RsFswp.Applications.K60_Transient.InputPy.Attenuation.set
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'INPut:ATTenuation:AUTO {param}')
