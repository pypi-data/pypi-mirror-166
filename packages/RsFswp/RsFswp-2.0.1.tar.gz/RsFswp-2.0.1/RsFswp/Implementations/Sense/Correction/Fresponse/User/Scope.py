from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scope:
	"""Scope commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scope", core, parent)

	def set(self, scope: enums.FramesScope) -> None:
		"""SCPI: [SENSe]:CORRection:FRESponse:USER:SCOPe \n
		Snippet: driver.sense.correction.fresponse.user.scope.set(scope = enums.FramesScope.ALL) \n
		No command help available \n
			:param scope: No help available
		"""
		param = Conversions.enum_scalar_to_str(scope, enums.FramesScope)
		self._core.io.write(f'SENSe:CORRection:FRESponse:USER:SCOPe {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.FramesScope:
		"""SCPI: [SENSe]:CORRection:FRESponse:USER:SCOPe \n
		Snippet: value: enums.FramesScope = driver.sense.correction.fresponse.user.scope.get() \n
		No command help available \n
			:return: scope: No help available"""
		response = self._core.io.query_str(f'SENSe:CORRection:FRESponse:USER:SCOPe?')
		return Conversions.str_to_scalar_enum(response, enums.FramesScope)
