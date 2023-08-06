from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Link:
	"""Link commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("link", core, parent)

	@property
	def factor(self):
		"""factor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_factor'):
			from .Factor import Factor
			self._factor = Factor(self._core, self._cmd_group)
		return self._factor

	def set(self, coupling_type: enums.FrequencyCouplingLinkA) -> None:
		"""SCPI: [SENSe]:FREQuency:CENTer:STEP:LINK \n
		Snippet: driver.sense.frequency.center.step.link.set(coupling_type = enums.FrequencyCouplingLinkA.OFF) \n
		This command selects the frequency step size mode. \n
			:param coupling_type: The step size is either a function of the span (x % of the span) or an absolute value. OFF Step size is a custom percentage of the span or an absolute custom value in Hz. You can define a percentage with [SENSe:]FREQuency:CENTer:STEP:LINK:FACTor. You can define a custom value with [SENSe:]FREQuency:CENTer:STEP. SPAN Step size is 10 % of the span.
		"""
		param = Conversions.enum_scalar_to_str(coupling_type, enums.FrequencyCouplingLinkA)
		self._core.io.write(f'SENSe:FREQuency:CENTer:STEP:LINK {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.FrequencyCouplingLinkA:
		"""SCPI: [SENSe]:FREQuency:CENTer:STEP:LINK \n
		Snippet: value: enums.FrequencyCouplingLinkA = driver.sense.frequency.center.step.link.get() \n
		This command selects the frequency step size mode. \n
			:return: coupling_type: No help available"""
		response = self._core.io.query_str(f'SENSe:FREQuency:CENTer:STEP:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.FrequencyCouplingLinkA)

	def clone(self) -> 'Link':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Link(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
