from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Osc:
	"""Osc commands group definition. 10 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("osc", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def tcpip(self):
		"""tcpip commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcpip'):
			from .Tcpip import Tcpip
			self._tcpip = Tcpip(self._core, self._cmd_group)
		return self._tcpip

	@property
	def balanced(self):
		"""balanced commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_balanced'):
			from .Balanced import Balanced
			self._balanced = Balanced(self._core, self._cmd_group)
		return self._balanced

	@property
	def fullscale(self):
		"""fullscale commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fullscale'):
			from .Fullscale import Fullscale
			self._fullscale = Fullscale(self._core, self._cmd_group)
		return self._fullscale

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePy
			self._typePy = TypePy(self._core, self._cmd_group)
		return self._typePy

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def skew(self):
		"""skew commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_skew'):
			from .Skew import Skew
			self._skew = Skew(self._core, self._cmd_group)
		return self._skew

	def clone(self) -> 'Osc':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Osc(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
