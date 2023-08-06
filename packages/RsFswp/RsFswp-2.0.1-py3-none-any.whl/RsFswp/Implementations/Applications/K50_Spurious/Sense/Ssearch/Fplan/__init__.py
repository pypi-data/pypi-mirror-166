from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fplan:
	"""Fplan commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fplan", core, parent)

	@property
	def tolerance(self):
		"""tolerance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tolerance'):
			from .Tolerance import Tolerance
			self._tolerance = Tolerance(self._core, self._cmd_group)
		return self._tolerance

	def set(self, state: bool) -> None:
		"""SCPI: [SENSe]:SSEarch:FPLan \n
		Snippet: driver.applications.k50Spurious.sense.ssearch.fplan.set(state = False) \n
		Enables or disables the the use of the frequency plan for identification of spurs. \n
			:param state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SENSe:SSEarch:FPLan {param}')

	def get(self) -> bool:
		"""SCPI: [SENSe]:SSEarch:FPLan \n
		Snippet: value: bool = driver.applications.k50Spurious.sense.ssearch.fplan.get() \n
		Enables or disables the the use of the frequency plan for identification of spurs. \n
			:return: state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on"""
		response = self._core.io.query_str(f'SENSe:SSEarch:FPLan?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'Fplan':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fplan(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
