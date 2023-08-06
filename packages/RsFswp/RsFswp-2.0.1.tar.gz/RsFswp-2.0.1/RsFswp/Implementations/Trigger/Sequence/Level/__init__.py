from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 9 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	@property
	def am(self):
		"""am commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_am'):
			from .Am import Am
			self._am = Am(self._core, self._cmd_group)
		return self._am

	@property
	def fm(self):
		"""fm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import Fm
			self._fm = Fm(self._core, self._cmd_group)
		return self._fm

	@property
	def pm(self):
		"""pm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pm'):
			from .Pm import Pm
			self._pm = Pm(self._core, self._cmd_group)
		return self._pm

	@property
	def video(self):
		"""video commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_video'):
			from .Video import Video
			self._video = Video(self._core, self._cmd_group)
		return self._video

	@property
	def external(self):
		"""external commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_external'):
			from .External import External
			self._external = External(self._core, self._cmd_group)
		return self._external

	@property
	def ifPower(self):
		"""ifPower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ifPower'):
			from .IfPower import IfPower
			self._ifPower = IfPower(self._core, self._cmd_group)
		return self._ifPower

	@property
	def iqPower(self):
		"""iqPower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqPower'):
			from .IqPower import IqPower
			self._iqPower = IqPower(self._core, self._cmd_group)
		return self._iqPower

	@property
	def rfPower(self):
		"""rfPower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfPower'):
			from .RfPower import RfPower
			self._rfPower = RfPower(self._core, self._cmd_group)
		return self._rfPower

	def clone(self) -> 'Level':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Level(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
