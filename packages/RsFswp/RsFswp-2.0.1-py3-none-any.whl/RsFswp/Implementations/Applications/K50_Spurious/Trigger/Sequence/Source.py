from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source: enums.ReferenceSourceC) -> None:
		"""SCPI: TRIGger[:SEQuence]:SOURce \n
		Snippet: driver.applications.k50Spurious.trigger.sequence.source.set(source = enums.ReferenceSourceC.EXT2) \n
		This command selects the trigger source. Note on external triggers: If a measurement is configured to wait for an
		external trigger signal in a remote control program, remote control is blocked until the trigger is received and the
		program can continue. Make sure this situation is avoided in your remote control programs. \n
			:param source: IMMediate Free Run EXT | EXT2 Trigger signal from one of the 'Trigger Input/Output' connectors. Note: Connector must be configured for 'Input'.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ReferenceSourceC)
		self._core.io.write(f'TRIGger:SEQuence:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.ReferenceSourceC:
		"""SCPI: TRIGger[:SEQuence]:SOURce \n
		Snippet: value: enums.ReferenceSourceC = driver.applications.k50Spurious.trigger.sequence.source.get() \n
		This command selects the trigger source. Note on external triggers: If a measurement is configured to wait for an
		external trigger signal in a remote control program, remote control is blocked until the trigger is received and the
		program can continue. Make sure this situation is avoided in your remote control programs. \n
			:return: source: IMMediate Free Run EXT | EXT2 Trigger signal from one of the 'Trigger Input/Output' connectors. Note: Connector must be configured for 'Input'."""
		response = self._core.io.query_str(f'TRIGger:SEQuence:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ReferenceSourceC)
