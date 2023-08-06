from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Calibration:
	"""Calibration commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def aiq(self):
		"""aiq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aiq'):
			from .Aiq import Aiq
			self._aiq = Aiq(self._core, self._cmd_group)
		return self._aiq

	@property
	def preSelection(self):
		"""preSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preSelection'):
			from .PreSelection import PreSelection
			self._preSelection = PreSelection(self._core, self._cmd_group)
		return self._preSelection

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Result import Result
			self._result = Result(self._core, self._cmd_group)
		return self._result

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import All
			self._all = All(self._core, self._cmd_group)
		return self._all

	def clone(self) -> 'Calibration':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Calibration(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
