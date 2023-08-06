from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, filter_type: enums.FilterTypeC, rangePy=repcap.RangePy.Default) -> None:
		"""SCPI: [SENSe]:LIST:RANGe<ri>:FILTer:TYPE \n
		Snippet: driver.sense.listPy.range.filterPy.typePy.set(filter_type = enums.FilterTypeC.CFILter, rangePy = repcap.RangePy.Default) \n
		No command help available \n
			:param filter_type: No help available
			:param rangePy: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Range')
		"""
		param = Conversions.enum_scalar_to_str(filter_type, enums.FilterTypeC)
		rangePy_cmd_val = self._cmd_group.get_repcap_cmd_value(rangePy, repcap.RangePy)
		self._core.io.write(f'SENSe:LIST:RANGe{rangePy_cmd_val}:FILTer:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, rangePy=repcap.RangePy.Default) -> enums.FilterTypeC:
		"""SCPI: [SENSe]:LIST:RANGe<ri>:FILTer:TYPE \n
		Snippet: value: enums.FilterTypeC = driver.sense.listPy.range.filterPy.typePy.get(rangePy = repcap.RangePy.Default) \n
		No command help available \n
			:param rangePy: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Range')
			:return: filter_type: No help available"""
		rangePy_cmd_val = self._cmd_group.get_repcap_cmd_value(rangePy, repcap.RangePy)
		response = self._core.io.query_str(f'SENSe:LIST:RANGe{rangePy_cmd_val}:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.FilterTypeC)
