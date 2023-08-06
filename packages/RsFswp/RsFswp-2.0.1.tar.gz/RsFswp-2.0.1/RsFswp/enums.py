from enum import Enum


# noinspection SpellCheckingInspection
class AccessType(Enum):
	"""2 Members, RO ... RW"""
	RO = 0
	RW = 1


# noinspection SpellCheckingInspection
class AdcPreFilterMode(Enum):
	"""2 Members, AUTO ... WIDE"""
	AUTO = 0
	WIDE = 1


# noinspection SpellCheckingInspection
class AdemMeasType(Enum):
	"""5 Members, MIDDle ... RMS"""
	MIDDle = 0
	MPEak = 1
	NPEak = 2
	PPEak = 3
	RMS = 4


# noinspection SpellCheckingInspection
class AdjustAlignment(Enum):
	"""3 Members, CENTer ... RIGHt"""
	CENTer = 0
	LEFT = 1
	RIGHt = 2


# noinspection SpellCheckingInspection
class AngleUnit(Enum):
	"""2 Members, DEG ... RAD"""
	DEG = 0
	RAD = 1


# noinspection SpellCheckingInspection
class AnnotationMode(Enum):
	"""2 Members, CSPan ... SSTop"""
	CSPan = 0
	SSTop = 1


# noinspection SpellCheckingInspection
class AttenuatorMode(Enum):
	"""3 Members, LDIStortion ... NORMal"""
	LDIStortion = 0
	LNOise = 1
	NORMal = 2


# noinspection SpellCheckingInspection
class AutoManualMode(Enum):
	"""2 Members, AUTO ... MANual"""
	AUTO = 0
	MANual = 1


# noinspection SpellCheckingInspection
class AutoManualUserMode(Enum):
	"""3 Members, AUTO ... USER"""
	AUTO = 0
	MANual = 1
	USER = 2


# noinspection SpellCheckingInspection
class AutoMode(Enum):
	"""3 Members, AUTO ... ON"""
	AUTO = 0
	OFF = 1
	ON = 2


# noinspection SpellCheckingInspection
class AutoOrOff(Enum):
	"""2 Members, AUTO ... OFF"""
	AUTO = 0
	OFF = 1


# noinspection SpellCheckingInspection
class AverageModeA(Enum):
	"""3 Members, LINear ... POWer"""
	LINear = 0
	LOGarithmic = 1
	POWer = 2


# noinspection SpellCheckingInspection
class AverageModeB(Enum):
	"""6 Members, LINear ... VIDeo"""
	LINear = 0
	LOGarithmic = 1
	MAXimum = 2
	POWer = 3
	SCALar = 4
	VIDeo = 5


# noinspection SpellCheckingInspection
class Band(Enum):
	"""14 Members, A ... Y"""
	A = 0
	D = 1
	E = 2
	F = 3
	G = 4
	J = 5
	K = 6
	KA = 7
	Q = 8
	U = 9
	USER = 10
	V = 11
	W = 12
	Y = 13


# noinspection SpellCheckingInspection
class BandB(Enum):
	"""12 Members, D ... Y"""
	D = 0
	E = 1
	F = 2
	G = 3
	J = 4
	KA = 5
	Q = 6
	U = 7
	USER = 8
	V = 9
	W = 10
	Y = 11


# noinspection SpellCheckingInspection
class BbInputSource(Enum):
	"""4 Members, AIQ ... RF"""
	AIQ = 0
	DIQ = 1
	FIQ = 2
	RF = 3


# noinspection SpellCheckingInspection
class BerRateFormat(Enum):
	"""17 Members, CURRent ... TTOTal"""
	CURRent = 0
	DSINdex = 1
	MAX = 2
	MIN = 3
	SECurrent = 4
	SEMax = 5
	SEMin = 6
	SETotal = 7
	TCURrent = 8
	TECurrent = 9
	TEMax = 10
	TEMin = 11
	TETotal = 12
	TMAX = 13
	TMIN = 14
	TOTal = 15
	TTOTal = 16


# noinspection SpellCheckingInspection
class BurstMode(Enum):
	"""2 Members, BURS ... MEAS"""
	BURS = 0
	MEAS = 1


# noinspection SpellCheckingInspection
class CalibrationScope(Enum):
	"""4 Members, ACLear ... ON"""
	ACLear = 0
	ALL = 1
	OFF = 2
	ON = 3


# noinspection SpellCheckingInspection
class CalibrationState(Enum):
	"""3 Members, EXPired ... OK"""
	EXPired = 0
	NAN = 1
	OK = 2


# noinspection SpellCheckingInspection
class ChannelType(Enum):
	"""31 Members, IqAnalyzer ... SpectrumAnalyzer"""
	IqAnalyzer = "IQ"
	K10_Gsm = "GSM"
	K106_NbIot = "NIOT"
	K10x_Lte = "LTE"
	K118_Verizon5G = "V5GT"
	K14x_5GnewRadio = "NR5G"
	K15_Avionics = "AVIonics"
	K17_MultiCarrierGroupDelay = "MCGD"
	K18_AmplifierMeas = "AMPLifier"
	K192_193_Docsis31 = "DOCSis"
	K201_OneWeb = "OWEB"
	K30_Noise = "NOISE"
	K40_PhaseNoise = "PNOISE"
	K50_FastSpurSearch = "SPUR"
	K6_PulseAnalysis = "PULSE"
	K60_TransientAnalysis = "TA"
	K7_AnalogModulation = "ADEM"
	K70_VectorSignalAnalyzer = "DDEM"
	K72_3GppFddBts = "BWCD"
	K73_3GppFddUe = "MWCD"
	K76_TdScdmaBts = "BTDS"
	K77_TdScdmaUe = "MTDS"
	K82_Cdma2000Bts = "BC2K"
	K83_Cdma2000Ms = "MC2K"
	K84_EvdoBts = "BDO"
	K85_EvdoMs = "MDO"
	K91_Wlan = "WLAN"
	K95_80211ad = "WIGIG"
	K97_80211ay = "EDMG"
	RealTimeSpectrum = "RTIM"
	SpectrumAnalyzer = "SANALYZER"


# noinspection SpellCheckingInspection
class CheckResult(Enum):
	"""2 Members, FAILED ... PASSED"""
	FAILED = 0
	PASSED = 1


# noinspection SpellCheckingInspection
class Color(Enum):
	"""16 Members, BLACk ... YELLow"""
	BLACk = 0
	BLUE = 1
	BROWn = 2
	CYAN = 3
	DGRay = 4
	GREen = 5
	LBLue = 6
	LCYan = 7
	LGRay = 8
	LGReen = 9
	LMAGenta = 10
	LRED = 11
	MAGenta = 12
	RED = 13
	WHITe = 14
	YELLow = 15


# noinspection SpellCheckingInspection
class ColorSchemeA(Enum):
	"""5 Members, COLD ... RADar"""
	COLD = 0
	COLor = 1
	GRAYscale = 2
	HOT = 3
	RADar = 4


# noinspection SpellCheckingInspection
class CompatibilityMode(Enum):
	"""9 Members, ATT ... FSW"""
	ATT = 0
	DEFault = 1
	FSET = 2
	FSL = 3
	FSP = 4
	FSQ = 5
	FSU = 6
	FSV = 7
	FSW = 8


# noinspection SpellCheckingInspection
class ComponentType(Enum):
	"""4 Members, AMPLifier ... MULTiplier"""
	AMPLifier = 0
	DIVider = 1
	MIXer = 2
	MULTiplier = 3


# noinspection SpellCheckingInspection
class ConfigMode(Enum):
	"""2 Members, DEFault ... USER"""
	DEFault = 0
	USER = 1


# noinspection SpellCheckingInspection
class CorrectionMeasType(Enum):
	"""2 Members, OPEN ... THRough"""
	OPEN = 0
	THRough = 1


# noinspection SpellCheckingInspection
class CorrectionMethod(Enum):
	"""2 Members, REFLexion ... TRANsmission"""
	REFLexion = 0
	TRANsmission = 1


# noinspection SpellCheckingInspection
class CorrectionMode(Enum):
	"""2 Members, SPOT ... TABLe"""
	SPOT = 0
	TABLe = 1


# noinspection SpellCheckingInspection
class Counter(Enum):
	"""2 Members, CAPTure ... STATistics"""
	CAPTure = 0
	STATistics = 1


# noinspection SpellCheckingInspection
class CouplingTypeA(Enum):
	"""2 Members, AC ... DC"""
	AC = 0
	DC = 1


# noinspection SpellCheckingInspection
class CouplingTypeB(Enum):
	"""3 Members, AC ... DCLimit"""
	AC = 0
	DC = 1
	DCLimit = 2


# noinspection SpellCheckingInspection
class DataExportMode(Enum):
	"""2 Members, RAW ... TRACe"""
	RAW = 0
	TRACe = 1


# noinspection SpellCheckingInspection
class DataFormat(Enum):
	"""10 Members, ASCii ... UINT_cma_64"""
	ASCii = 0
	MATLAB_cma_16 = 1
	MATLAB_cma_32 = 2
	MATLAB_cma_64 = 3
	Real16 = "REAL,16"
	Real32 = "REAL,32"
	Real64 = "REAL,64"
	UINT_cma_16 = 7
	UINT_cma_32 = 8
	UINT_cma_64 = 9


# noinspection SpellCheckingInspection
class DdemGroup(Enum):
	"""8 Members, APSK ... UQAM"""
	APSK = 0
	ASK = 1
	FSK = 2
	MSK = 3
	PSK = 4
	QAM = 5
	QPSK = 6
	UQAM = 7


# noinspection SpellCheckingInspection
class DdemodFilter(Enum):
	"""13 Members, A25Fm ... RRCosine"""
	A25Fm = 0
	B22 = 1
	B25 = 2
	B44 = 3
	EMES = 4
	EREF = 5
	GAUSsian = 6
	QFM = 7
	QFR = 8
	QRM = 9
	QRR = 10
	RCOSine = 11
	RRCosine = 12


# noinspection SpellCheckingInspection
class DdemResultType(Enum):
	"""20 Members, ADR ... RHO"""
	ADR = 0
	DEV = 1
	DTTS = 2
	EVPK = 3
	EVPS = 4
	EVRM = 5
	FEPK = 6
	FERR = 7
	FSPK = 8
	FSPS = 9
	FSRM = 10
	IQIM = 11
	IQOF = 12
	MEPK = 13
	MEPS = 14
	MERM = 15
	PEPK = 16
	PEPS = 17
	PERM = 18
	RHO = 19


# noinspection SpellCheckingInspection
class DdemSignalType(Enum):
	"""2 Members, BURSted ... CONTinuous"""
	BURSted = 0
	CONTinuous = 1


# noinspection SpellCheckingInspection
class Detect(Enum):
	"""2 Members, DETected ... NDETected"""
	DETected = 0
	NDETected = 1


# noinspection SpellCheckingInspection
class DetectorB(Enum):
	"""13 Members, ACSine ... SMP"""
	ACSine = 0
	ACVideo = 1
	APEak = 2
	AVERage = 3
	CAVerage = 4
	CRMS = 5
	NEGative = 6
	NRM = 7
	POSitive = 8
	QPEak = 9
	RMS = 10
	SAMPle = 11
	SMP = 12


# noinspection SpellCheckingInspection
class DetectorC(Enum):
	"""8 Members, ACSine ... SAMPle"""
	ACSine = 0
	ACVideo = 1
	APEak = 2
	AVERage = 3
	NEGative = 4
	POSitive = 5
	RMS = 6
	SAMPle = 7


# noinspection SpellCheckingInspection
class DiagnosticSignal(Enum):
	"""8 Members, AIQ ... WBCal"""
	AIQ = 0
	CALibration = 1
	EMI = 2
	MCALibration = 3
	RF = 4
	SYNThtwo = 5
	TG = 6
	WBCal = 7


# noinspection SpellCheckingInspection
class DiqUnit(Enum):
	"""8 Members, AMPere ... WATT"""
	AMPere = 0
	DBM = 1
	DBMV = 2
	DBPW = 3
	DBUA = 4
	DBUV = 5
	VOLT = 6
	WATT = 7


# noinspection SpellCheckingInspection
class DisplayFormat(Enum):
	"""2 Members, SINGle ... SPLit"""
	SINGle = 0
	SPLit = 1


# noinspection SpellCheckingInspection
class DisplayPosition(Enum):
	"""3 Members, BOTTom ... TOP"""
	BOTTom = 0
	OFF = 1
	TOP = 2


# noinspection SpellCheckingInspection
class Duration(Enum):
	"""3 Members, LONG ... SHORt"""
	LONG = 0
	NORMal = 1
	SHORt = 2


# noinspection SpellCheckingInspection
class DutType(Enum):
	"""4 Members, AMPLifier ... UPConv"""
	AMPLifier = 0
	DDOWnconv = 1
	DOWNconv = 2
	UPConv = 3


# noinspection SpellCheckingInspection
class EgateType(Enum):
	"""2 Members, EDGE ... LEVel"""
	EDGE = 0
	LEVel = 1


# noinspection SpellCheckingInspection
class EnrType(Enum):
	"""3 Members, DIODe ... SMARt"""
	DIODe = 0
	RESistor = 1
	SMARt = 2


# noinspection SpellCheckingInspection
class EspectrumRtype(Enum):
	"""2 Members, CPOWer ... PEAK"""
	CPOWer = 0
	PEAK = 1


# noinspection SpellCheckingInspection
class EventOnce(Enum):
	"""1 Members, ONCE ... ONCE"""
	ONCE = 0


# noinspection SpellCheckingInspection
class EvmCalc(Enum):
	"""4 Members, MACPower ... SYMBol"""
	MACPower = 0
	MECPower = 1
	SIGNal = 2
	SYMBol = 3


# noinspection SpellCheckingInspection
class Factory(Enum):
	"""3 Members, ALL ... STANdard"""
	ALL = 0
	PATTern = 1
	STANdard = 2


# noinspection SpellCheckingInspection
class FftFilterMode(Enum):
	"""3 Members, AUTO ... WIDE"""
	AUTO = 0
	NARRow = 1
	WIDE = 2


# noinspection SpellCheckingInspection
class FileFormat(Enum):
	"""2 Members, CSV ... DAT"""
	CSV = 0
	DAT = 1


# noinspection SpellCheckingInspection
class FileFormatDdem(Enum):
	"""2 Members, FRES ... VAE"""
	FRES = 0
	VAE = 1


# noinspection SpellCheckingInspection
class FileSeparator(Enum):
	"""3 Members, COMMa ... TAB"""
	COMMa = 0
	SEMicolon = 1
	TAB = 2


# noinspection SpellCheckingInspection
class FilterTypeA(Enum):
	"""2 Members, FLAT ... GAUSs"""
	FLAT = 0
	GAUSs = 1


# noinspection SpellCheckingInspection
class FilterTypeB(Enum):
	"""9 Members, CFILter ... RRC"""
	CFILter = 0
	CISPr = 1
	FFT = 2
	MIL = 3
	NOISe = 4
	NORMal = 5
	P5 = 6
	PULSe = 7
	RRC = 8


# noinspection SpellCheckingInspection
class FilterTypeC(Enum):
	"""7 Members, CFILter ... RRC"""
	CFILter = 0
	CISPr = 1
	MIL = 2
	NORMal = 3
	P5 = 4
	PULSe = 5
	RRC = 6


# noinspection SpellCheckingInspection
class FilterTypeK91(Enum):
	"""5 Members, CFILter ... RRC"""
	CFILter = 0
	NORMal = 1
	P5 = 2
	PULSe = 3
	RRC = 4


# noinspection SpellCheckingInspection
class FineSync(Enum):
	"""3 Members, DDATa ... PATTern"""
	DDATa = 0
	KDATa = 1
	PATTern = 2


# noinspection SpellCheckingInspection
class FpeaksSortMode(Enum):
	"""2 Members, X ... Y"""
	X = 0
	Y = 1


# noinspection SpellCheckingInspection
class FrameModulation(Enum):
	"""3 Members, AUTO ... PATTern"""
	AUTO = 0
	DATA = 1
	PATTern = 2


# noinspection SpellCheckingInspection
class FrameModulationB(Enum):
	"""2 Members, DATA ... PATTern"""
	DATA = 0
	PATTern = 1


# noinspection SpellCheckingInspection
class FramesScope(Enum):
	"""2 Members, ALL ... CHANnel"""
	ALL = 0
	CHANnel = 1


# noinspection SpellCheckingInspection
class FrequencyCouplingLinkA(Enum):
	"""3 Members, OFF ... SPAN"""
	OFF = 0
	RBW = 1
	SPAN = 2


# noinspection SpellCheckingInspection
class FrequencyType(Enum):
	"""3 Members, IF ... RF"""
	IF = 0
	LO = 1
	RF = 2


# noinspection SpellCheckingInspection
class FunctionA(Enum):
	"""2 Members, MAX ... OFF"""
	MAX = 0
	OFF = 1


# noinspection SpellCheckingInspection
class FunctionB(Enum):
	"""3 Members, MAX ... SUM"""
	MAX = 0
	NONE = 1
	SUM = 2


# noinspection SpellCheckingInspection
class GatedSourceK30(Enum):
	"""3 Members, EXT2 ... EXTernal"""
	EXT2 = 0
	EXT3 = 1
	EXTernal = 2


# noinspection SpellCheckingInspection
class GeneratorIntf(Enum):
	"""2 Members, GPIB ... TCPip"""
	GPIB = 0
	TCPip = 1


# noinspection SpellCheckingInspection
class GeneratorIntfType(Enum):
	"""3 Members, GPIB ... TCPip"""
	GPIB = 0
	PEXPress = 1
	TCPip = 2


# noinspection SpellCheckingInspection
class GeneratorLink(Enum):
	"""2 Members, GPIB ... TTL"""
	GPIB = 0
	TTL = 1


# noinspection SpellCheckingInspection
class GpibTerminator(Enum):
	"""2 Members, EOI ... LFEoi"""
	EOI = 0
	LFEoi = 1


# noinspection SpellCheckingInspection
class HardcopyContent(Enum):
	"""2 Members, HCOPy ... WINDows"""
	HCOPy = 0
	WINDows = 1


# noinspection SpellCheckingInspection
class HardcopyHeader(Enum):
	"""5 Members, ALWays ... SECTion"""
	ALWays = 0
	GLOBal = 1
	NEVer = 2
	ONCE = 3
	SECTion = 4


# noinspection SpellCheckingInspection
class HardcopyLogo(Enum):
	"""3 Members, ALWays ... NEVer"""
	ALWays = 0
	GLOBal = 1
	NEVer = 2


# noinspection SpellCheckingInspection
class HardcopyMode(Enum):
	"""2 Members, REPort ... SCReen"""
	REPort = 0
	SCReen = 1


# noinspection SpellCheckingInspection
class HardcopyPageSize(Enum):
	"""2 Members, A4 ... US"""
	A4 = 0
	US = 1


# noinspection SpellCheckingInspection
class HeadersK50(Enum):
	"""9 Members, ALL ... STOP"""
	ALL = 0
	DELTa = 1
	FREQuency = 2
	IDENt = 3
	POWer = 4
	RBW = 5
	SID = 6
	STARt = 7
	STOP = 8


# noinspection SpellCheckingInspection
class HumsFileFormat(Enum):
	"""2 Members, JSON ... XML"""
	JSON = 0
	XML = 1


# noinspection SpellCheckingInspection
class IdnFormat(Enum):
	"""3 Members, FSL ... NEW"""
	FSL = 0
	LEGacy = 1
	NEW = 2


# noinspection SpellCheckingInspection
class IfGainMode(Enum):
	"""2 Members, NORMal ... PULSe"""
	NORMal = 0
	PULSe = 1


# noinspection SpellCheckingInspection
class IfGainModeDdem(Enum):
	"""5 Members, AVERaging ... USER"""
	AVERaging = 0
	FREeze = 1
	NORMal = 2
	TRACking = 3
	USER = 4


# noinspection SpellCheckingInspection
class InOutDirection(Enum):
	"""2 Members, INPut ... OUTPut"""
	INPut = 0
	OUTPut = 1


# noinspection SpellCheckingInspection
class InputConnectorB(Enum):
	"""3 Members, AIQI ... RFPRobe"""
	AIQI = 0
	RF = 1
	RFPRobe = 2


# noinspection SpellCheckingInspection
class InputConnectorC(Enum):
	"""2 Members, RF ... RFPRobe"""
	RF = 0
	RFPRobe = 1


# noinspection SpellCheckingInspection
class InputSelect(Enum):
	"""2 Members, INPut1 ... INPut2"""
	INPut1 = 0
	INPut2 = 1


# noinspection SpellCheckingInspection
class InputSource(Enum):
	"""7 Members, ABBand ... RFAiq"""
	ABBand = 0
	AIQ = 1
	DIQ = 2
	FIQ = 3
	OBBand = 4
	RF = 5
	RFAiq = 6


# noinspection SpellCheckingInspection
class InputSourceB(Enum):
	"""2 Members, FIQ ... RF"""
	FIQ = 0
	RF = 1


# noinspection SpellCheckingInspection
class InstrumentMode(Enum):
	"""3 Members, MSRanalyzer ... SANalyzer"""
	MSRanalyzer = 0
	RTMStandard = 1
	SANalyzer = 2


# noinspection SpellCheckingInspection
class IqBandwidthMode(Enum):
	"""3 Members, AUTO ... MANual"""
	AUTO = 0
	FFT = 1
	MANual = 2


# noinspection SpellCheckingInspection
class IqDataFormat(Enum):
	"""4 Members, FloatComplex ... IntegerReal"""
	FloatComplex = "FLOat32,COMPlex"
	FloatReal = "FLOat32,REAL"
	IntegerComplex = "INT32,COMPlex"
	IntegerReal = "INT32,REAL"


# noinspection SpellCheckingInspection
class IqDataFormatDdem(Enum):
	"""10 Members, FloatComplex ... IntegerReal"""
	FloatComplex = "FLOat32,COMPlex"
	FloatIiQq = "FLOat32,IIQQ"
	FloatIqIq = "FLOat32,IQIQ"
	FloatPolar = "FLOat32,POLar"
	FloatReal = "FLOat32,REAL"
	IntegerComplex = "INT32,COMPlex"
	IntegerIiQq = "INT32,IIQQ"
	IntegerIqIq = "INT32,IQIQ"
	IntegerPolar = "INT32,POLar"
	IntegerReal = "INT32,REAL"


# noinspection SpellCheckingInspection
class IqRangeType(Enum):
	"""2 Members, CAPTure ... RRANge"""
	CAPTure = 0
	RRANge = 1


# noinspection SpellCheckingInspection
class IqType(Enum):
	"""3 Members, Ipart ... Qpart"""
	Ipart = "I"
	IQpart = "IQ"
	Qpart = "Q"


# noinspection SpellCheckingInspection
class LeftRightDirection(Enum):
	"""2 Members, LEFT ... RIGHt"""
	LEFT = 0
	RIGHt = 1


# noinspection SpellCheckingInspection
class LimitState(Enum):
	"""4 Members, ABSolute ... RELative"""
	ABSolute = 0
	AND = 1
	OR = 2
	RELative = 3


# noinspection SpellCheckingInspection
class LimitUnit(Enum):
	"""27 Members, A ... WATT"""
	A = 0
	AMPere = 1
	DB = 2
	DBM = 3
	DBM_mhz = 4
	DBMV = 5
	DBMV_mhz = 6
	DBPT = 7
	DBPT_mhz = 8
	DBPW = 9
	DBPW_mhz = 10
	DBUA = 11
	DBUa_m = 12
	DBUa_mhz = 13
	DBUa_mmhz = 14
	DBUV = 15
	DBUV_m = 16
	DBUV_mhz = 17
	DBUV_mmhz = 18
	DEG = 19
	HZ = 20
	PCT = 21
	RAD = 22
	S = 23
	UNITless = 24
	VOLT = 25
	WATT = 26


# noinspection SpellCheckingInspection
class LoadType(Enum):
	"""2 Members, NEW ... REPLace"""
	NEW = 0
	REPLace = 1


# noinspection SpellCheckingInspection
class LoType(Enum):
	"""2 Members, FIXed ... VARiable"""
	FIXed = 0
	VARiable = 1


# noinspection SpellCheckingInspection
class LowHigh(Enum):
	"""2 Members, HIGH ... LOW"""
	HIGH = 0
	LOW = 1


# noinspection SpellCheckingInspection
class MarkerFunctionA(Enum):
	"""15 Members, ACPower ... TPOWer"""
	ACPower = 0
	AOBandwidth = 1
	AOBWidth = 2
	CN = 3
	CN0 = 4
	COBandwidth = 5
	COBWidth = 6
	CPOWer = 7
	GACLr = 8
	MACM = 9
	MCACpower = 10
	OBANdwidth = 11
	OBWidth = 12
	PPOWer = 13
	TPOWer = 14


# noinspection SpellCheckingInspection
class MarkerFunctionB(Enum):
	"""8 Members, ACPower ... OBWidth"""
	ACPower = 0
	AOBWidth = 1
	CN = 2
	CN0 = 3
	CPOWer = 4
	MCACpower = 5
	OBANdwidth = 6
	OBWidth = 7


# noinspection SpellCheckingInspection
class MarkerMode(Enum):
	"""3 Members, DENSity ... RPOWer"""
	DENSity = 0
	POWer = 1
	RPOWer = 2


# noinspection SpellCheckingInspection
class MarkerRealImagB(Enum):
	"""2 Members, IMAG ... REAL"""
	IMAG = 0
	REAL = 1


# noinspection SpellCheckingInspection
class MeasurementStep(Enum):
	"""4 Members, NESTimate ... SPOTstep"""
	NESTimate = 0
	SDETection = 1
	SOVerview = 2
	SPOTstep = 3


# noinspection SpellCheckingInspection
class MeasurementType(Enum):
	"""2 Members, DIRected ... WIDE"""
	DIRected = 0
	WIDE = 1


# noinspection SpellCheckingInspection
class MessageType(Enum):
	"""2 Members, REMote ... SMSG"""
	REMote = 0
	SMSG = 1


# noinspection SpellCheckingInspection
class MixerIdentifier(Enum):
	"""2 Members, CLOCk ... LO"""
	CLOCk = 0
	LO = 1


# noinspection SpellCheckingInspection
class MpowerDetector(Enum):
	"""2 Members, MEAN ... PEAK"""
	MEAN = 0
	PEAK = 1


# noinspection SpellCheckingInspection
class MskFormat(Enum):
	"""4 Members, DIFFerential ... TYPe2"""
	DIFFerential = 0
	NORMal = 1
	TYPe1 = 2
	TYPe2 = 3


# noinspection SpellCheckingInspection
class MsSyncMode(Enum):
	"""5 Members, MASTer ... SLAVe"""
	MASTer = 0
	NONE = 1
	PRIMary = 2
	SECondary = 3
	SLAVe = 4


# noinspection SpellCheckingInspection
class NoiseFigureLimit(Enum):
	"""7 Members, ENR ... YFACtor"""
	ENR = 0
	GAIN = 1
	NOISe = 2
	PCOLd = 3
	PHOT = 4
	TEMPerature = 5
	YFACtor = 6


# noinspection SpellCheckingInspection
class NoiseFigureResult(Enum):
	"""11 Members, CPCold ... YFACtor"""
	CPCold = 0
	CPHot = 1
	CYFactor = 2
	ENR = 3
	GAIN = 4
	NOISe = 5
	NUNCertainty = 6
	PCOLd = 7
	PHOT = 8
	TEMPerature = 9
	YFACtor = 10


# noinspection SpellCheckingInspection
class NoiseFigureResultCustom(Enum):
	"""10 Members, CPCold ... YFACtor"""
	CPCold = 0
	CPHot = 1
	CYFactor = 2
	ENR = 3
	GAIN = 4
	NOISe = 5
	PCOLd = 6
	PHOT = 7
	TEMPerature = 8
	YFACtor = 9


# noinspection SpellCheckingInspection
class OddEven(Enum):
	"""3 Members, EODD ... ODD"""
	EODD = 0
	EVEN = 1
	ODD = 2


# noinspection SpellCheckingInspection
class OffState(Enum):
	"""1 Members, OFF ... OFF"""
	OFF = 0


# noinspection SpellCheckingInspection
class OptimizationCriterion(Enum):
	"""2 Members, EVMMin ... RMSMin"""
	EVMMin = 0
	RMSMin = 1


# noinspection SpellCheckingInspection
class OptionState(Enum):
	"""3 Members, OCCupy ... ON"""
	OCCupy = 0
	OFF = 1
	ON = 2


# noinspection SpellCheckingInspection
class OutputType(Enum):
	"""4 Members, DEVice ... UDEFined"""
	DEVice = 0
	TARMed = 1
	TOFF = 2
	UDEFined = 3


# noinspection SpellCheckingInspection
class PageMarginUnit(Enum):
	"""2 Members, IN ... MM"""
	IN = 0
	MM = 1


# noinspection SpellCheckingInspection
class PageOrientation(Enum):
	"""2 Members, LANDscape ... PORTrait"""
	LANDscape = 0
	PORTrait = 1


# noinspection SpellCheckingInspection
class PictureFormat(Enum):
	"""11 Members, BMP ... WMF"""
	BMP = 0
	DOC = 1
	EWMF = 2
	GDI = 3
	JPEG = 4
	JPG = 5
	PDF = 6
	PNG = 7
	RTF = 8
	SVG = 9
	WMF = 10


# noinspection SpellCheckingInspection
class PmeterFreqLink(Enum):
	"""3 Members, CENTer ... OFF"""
	CENTer = 0
	MARKer1 = 1
	OFF = 2


# noinspection SpellCheckingInspection
class PmRpointMode(Enum):
	"""2 Members, MANual ... RIGHt"""
	MANual = 0
	RIGHt = 1


# noinspection SpellCheckingInspection
class PowerMeasFunction(Enum):
	"""7 Members, ACPower ... OBWidth"""
	ACPower = 0
	CN = 1
	CN0 = 2
	CPOWer = 3
	MCACpower = 4
	OBANdwidth = 5
	OBWidth = 6


# noinspection SpellCheckingInspection
class PowerMeterUnit(Enum):
	"""3 Members, DBM ... WATT"""
	DBM = 0
	W = 1
	WATT = 2


# noinspection SpellCheckingInspection
class PowerSource(Enum):
	"""2 Members, VSUPply ... VTUNe"""
	VSUPply = 0
	VTUNe = 1


# noinspection SpellCheckingInspection
class PowerUnit(Enum):
	"""25 Members, A ... WATT"""
	A = 0
	AMPere = 1
	DB = 2
	DBM = 3
	DBM_mhz = 4
	DBMV = 5
	DBMV_mhz = 6
	DBPT = 7
	DBPT_mhz = 8
	DBPW = 9
	DBPW_mhz = 10
	DBUA = 11
	DBUa_m = 12
	DBUa_mhz = 13
	DBUa_mmhz = 14
	DBUV = 15
	DBUV_m = 16
	DBUV_mhz = 17
	DBUV_mmhz = 18
	PCT = 19
	UNITless = 20
	V = 21
	VOLT = 22
	W = 23
	WATT = 24


# noinspection SpellCheckingInspection
class PowerUnitDdem(Enum):
	"""3 Members, DBM ... DBUV"""
	DBM = 0
	DBMV = 1
	DBUV = 2


# noinspection SpellCheckingInspection
class PreampOption(Enum):
	"""2 Members, B23 ... B24"""
	B23 = 0
	B24 = 1


# noinspection SpellCheckingInspection
class PresetCompatible(Enum):
	"""8 Members, MRECeiver ... VNA"""
	MRECeiver = 0
	MSRA = 1
	OFF = 2
	PNOise = 3
	RECeiver = 4
	RTMS = 5
	SANalyzer = 6
	VNA = 7


# noinspection SpellCheckingInspection
class Probability(Enum):
	"""4 Members, P0_01 ... P10"""
	P0_01 = 0
	P0_1 = 1
	P1 = 2
	P10 = 3


# noinspection SpellCheckingInspection
class ProbeMode(Enum):
	"""4 Members, CM ... PM"""
	CM = 0
	DM = 1
	NM = 2
	PM = 3


# noinspection SpellCheckingInspection
class ProbeSetupMode(Enum):
	"""2 Members, NOACtion ... RSINgle"""
	NOACtion = 0
	RSINgle = 1


# noinspection SpellCheckingInspection
class PskFormat(Enum):
	"""7 Members, DIFFerential ... PI8D8psk"""
	DIFFerential = 0
	DPI2 = 1
	MNPi2 = 2
	N3Pi8 = 3
	NORMal = 4
	NPI2 = 5
	PI8D8psk = 6


# noinspection SpellCheckingInspection
class PwrLevelMode(Enum):
	"""2 Members, CURRent ... VOLTage"""
	CURRent = 0
	VOLTage = 1


# noinspection SpellCheckingInspection
class PwrMeasUnit(Enum):
	"""3 Members, ABS ... PMHZ"""
	ABS = 0
	PHZ = 1
	PMHZ = 2


# noinspection SpellCheckingInspection
class QamFormat(Enum):
	"""4 Members, DIFFerential ... NPI4"""
	DIFFerential = 0
	MNPi4 = 1
	NORMal = 2
	NPI4 = 3


# noinspection SpellCheckingInspection
class QpskFormat(Enum):
	"""7 Members, DIFFerential ... SOFFset"""
	DIFFerential = 0
	DPI4 = 1
	N3Pi4 = 2
	NORMal = 3
	NPI4 = 4
	OFFSet = 5
	SOFFset = 6


# noinspection SpellCheckingInspection
class RangeClass(Enum):
	"""3 Members, LOCal ... WIDE"""
	LOCal = 0
	MEDium = 1
	WIDE = 2


# noinspection SpellCheckingInspection
class RangeParam(Enum):
	"""12 Members, ARBW ... TSTR"""
	ARBW = 0
	LOFFset = 1
	MFRBw = 2
	NFFT = 3
	PAValue = 4
	PEXCursion = 5
	RBW = 6
	RFATtenuation = 7
	RLEVel = 8
	SNRatio = 9
	TSTP = 10
	TSTR = 11


# noinspection SpellCheckingInspection
class RefChannel(Enum):
	"""3 Members, LHIGhest ... MINimum"""
	LHIGhest = 0
	MAXimum = 1
	MINimum = 2


# noinspection SpellCheckingInspection
class ReferenceMode(Enum):
	"""2 Members, ABSolute ... RELative"""
	ABSolute = 0
	RELative = 1


# noinspection SpellCheckingInspection
class ReferenceSource(Enum):
	"""2 Members, EXT ... INT"""
	EXT = 0
	INT = 1


# noinspection SpellCheckingInspection
class ReferenceSourceA(Enum):
	"""11 Members, E10 ... SYNC"""
	E10 = 0
	E100 = 1
	E1000 = 2
	EAUTo = 3
	EXT1 = 4
	EXT2 = 5
	EXTernal = 6
	EXTernal1 = 7
	EXTernal2 = 8
	INTernal = 9
	SYNC = 10


# noinspection SpellCheckingInspection
class ReferenceSourceB(Enum):
	"""3 Members, EAUTo ... INTernal"""
	EAUTo = 0
	EXTernal = 1
	INTernal = 2


# noinspection SpellCheckingInspection
class ReferenceSourceC(Enum):
	"""7 Members, EXT2 ... RFPower"""
	EXT2 = 0
	EXT3 = 1
	EXTernal = 2
	IFPower = 3
	IMMediate = 4
	IQPower = 5
	RFPower = 6


# noinspection SpellCheckingInspection
class ReferenceSourceD(Enum):
	"""4 Members, EXT2 ... IMMediate"""
	EXT2 = 0
	EXT3 = 1
	EXTernal = 2
	IMMediate = 3


# noinspection SpellCheckingInspection
class Relay(Enum):
	"""84 Members, AC_enable ... SWRF1in"""
	AC_enable = 0
	ACDC = 1
	AMPSw_2 = 2
	AMPSw_4 = 3
	ATT10 = 4
	ATT10db = 5
	ATT1db = 6
	ATT20 = 7
	ATT20db = 8
	ATT2db = 9
	ATT40 = 10
	ATT40db = 11
	ATT4db_a = 12
	ATT4db_b = 13
	ATT5 = 14
	ATTinput2 = 15
	CAL = 16
	CAL_enable = 17
	EATT = 18
	EMIMatt10 = 19
	EXT_relais = 20
	HP_Bypass = 21
	HP_Bypass_2 = 22
	HP_Hp100khz = 23
	HP_Hp1khz = 24
	HP_Hp1mhz = 25
	HP_Hp200khz = 26
	HP_Hp20khz = 27
	HP_Hp50khz = 28
	HP_Hp5mhz = 29
	HP_Hp9khz = 30
	HP_Sw = 31
	IFSW = 32
	INP2matt10r1 = 33
	INP2matt10r2 = 34
	INPut2 = 35
	LFMatt10 = 36
	LNA20db_1 = 37
	LNA20db_2 = 38
	LP_Lp100khz = 39
	LP_Lp14mhz = 40
	LP_Lp1mhz = 41
	LP_Lp20khz = 42
	LP_Lp40mhz = 43
	LP_Lp500khz = 44
	LP_Lp5mhz = 45
	LP_Sw = 46
	PREamp = 47
	PREamp30mhz = 48
	PRESab_bypr1 = 49
	PRESab_bypr2 = 50
	PRESab_swir1 = 51
	PRESab_swir2 = 52
	PRESel = 53
	RFAB = 54
	SATT10 = 55
	SATT20 = 56
	SATT40 = 57
	SCAL = 58
	SIGSourout = 59
	SP6T = 60
	SPAByp = 61
	SPDTinput = 62
	SPDTmwcamp = 63
	SWAMp1 = 64
	SWAMp1amp2 = 65
	SWAMp1toamp4 = 66
	SWAMp2 = 67
	SWAMp3 = 68
	SWAMp3amp4 = 69
	SWAMp4 = 70
	SWAMp5 = 71
	SWAMp6 = 72
	SWAMp7 = 73
	SWF1f2in = 74
	SWF1f2out = 75
	SWF1tof4out = 76
	SWF3f4out = 77
	SWF3in = 78
	SWF4in = 79
	SWF5in = 80
	SWF6f7in = 81
	SWFE = 82
	SWRF1in = 83


# noinspection SpellCheckingInspection
class ResultTypeB(Enum):
	"""4 Members, ALL ... PEAK"""
	ALL = 0
	CFACtor = 1
	MEAN = 2
	PEAK = 3


# noinspection SpellCheckingInspection
class ResultTypeC(Enum):
	"""2 Members, AVERage ... IMMediate"""
	AVERage = 0
	IMMediate = 1


# noinspection SpellCheckingInspection
class ResultTypeD(Enum):
	"""1 Members, TOTal ... TOTal"""
	TOTal = 0


# noinspection SpellCheckingInspection
class ResultTypeStat(Enum):
	"""9 Members, AVG ... TPEak"""
	AVG = 0
	PAVG = 1
	PCTL = 2
	PEAK = 3
	PPCTl = 4
	PSDev = 5
	RPEak = 6
	SDEV = 7
	TPEak = 8


# noinspection SpellCheckingInspection
class ScaleYaxisUnit(Enum):
	"""2 Members, ABS ... PCT"""
	ABS = 0
	PCT = 1


# noinspection SpellCheckingInspection
class ScalingMode(Enum):
	"""2 Members, LINear ... LOGarithmic"""
	LINear = 0
	LOGarithmic = 1


# noinspection SpellCheckingInspection
class SearchArea(Enum):
	"""2 Members, MEMory ... VISible"""
	MEMory = 0
	VISible = 1


# noinspection SpellCheckingInspection
class SearchRange(Enum):
	"""2 Members, GMAXimum ... RMAXimum"""
	GMAXimum = 0
	RMAXimum = 1


# noinspection SpellCheckingInspection
class SelectAll(Enum):
	"""1 Members, ALL ... ALL"""
	ALL = 0


# noinspection SpellCheckingInspection
class SelectionRangeB(Enum):
	"""2 Members, ALL ... CURRent"""
	ALL = 0
	CURRent = 1


# noinspection SpellCheckingInspection
class SelectionScope(Enum):
	"""2 Members, ALL ... SINGle"""
	ALL = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class Separator(Enum):
	"""2 Members, COMMa ... POINt"""
	COMMa = 0
	POINt = 1


# noinspection SpellCheckingInspection
class SequencerMode(Enum):
	"""4 Members, CDEFined ... SINGle"""
	CDEFined = 0
	CONTinous = 1
	CONTinuous = 2
	SINGle = 3


# noinspection SpellCheckingInspection
class ServiceBandwidth(Enum):
	"""2 Members, BROadband ... NARRowband"""
	BROadband = 0
	NARRowband = 1


# noinspection SpellCheckingInspection
class ServiceState(Enum):
	"""4 Members, DEViations ... REQired"""
	DEViations = 0
	NAN = 1
	OK = 2
	REQired = 3


# noinspection SpellCheckingInspection
class SidebandPos(Enum):
	"""2 Members, INVerse ... NORMal"""
	INVerse = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class SignalLevel(Enum):
	"""3 Members, HIGH ... OFF"""
	HIGH = 0
	LOW = 1
	OFF = 2


# noinspection SpellCheckingInspection
class SignalType(Enum):
	"""3 Members, AC ... DCZero"""
	AC = 0
	DC = 1
	DCZero = 2


# noinspection SpellCheckingInspection
class SingleValue(Enum):
	"""13 Members, ALL ... RHO"""
	ALL = 0
	CFER = 1
	EVMP = 2
	EVMR = 3
	FDER = 4
	FEP = 5
	FERM = 6
	IQOF = 7
	MEP = 8
	MERM = 9
	PEP = 10
	PERM = 11
	RHO = 12


# noinspection SpellCheckingInspection
class Size(Enum):
	"""2 Members, LARGe ... SMALl"""
	LARGe = 0
	SMALl = 1


# noinspection SpellCheckingInspection
class SlopeType(Enum):
	"""2 Members, NEGative ... POSitive"""
	NEGative = 0
	POSitive = 1


# noinspection SpellCheckingInspection
class SnmpVersion(Enum):
	"""5 Members, DEFault ... V3"""
	DEFault = 0
	OFF = 1
	V12 = 2
	V123 = 3
	V3 = 4


# noinspection SpellCheckingInspection
class Source(Enum):
	"""13 Members, AM ... VIDeo"""
	AM = 0
	FM = 1
	FOCus = 2
	HVIDeo = 3
	IF = 4
	IF2 = 5
	IQ = 6
	OFF = 7
	OUT1 = 8
	OUT2 = 9
	PM = 10
	SSB = 11
	VIDeo = 12


# noinspection SpellCheckingInspection
class SourceInt(Enum):
	"""2 Members, EXTernal ... INTernal"""
	EXTernal = 0
	INTernal = 1


# noinspection SpellCheckingInspection
class SpacingY(Enum):
	"""4 Members, LDB ... PERCent"""
	LDB = 0
	LINear = 1
	LOGarithmic = 2
	PERCent = 3


# noinspection SpellCheckingInspection
class SpanSetting(Enum):
	"""2 Members, FREQuency ... TIME"""
	FREQuency = 0
	TIME = 1


# noinspection SpellCheckingInspection
class State(Enum):
	"""4 Members, ALL ... ON"""
	ALL = 0
	AUTO = 1
	OFF = 2
	ON = 3


# noinspection SpellCheckingInspection
class StatisticMode(Enum):
	"""2 Members, INFinite ... SONLy"""
	INFinite = 0
	SONLy = 1


# noinspection SpellCheckingInspection
class StatisticType(Enum):
	"""2 Members, ALL ... SELected"""
	ALL = 0
	SELected = 1


# noinspection SpellCheckingInspection
class Stepsize(Enum):
	"""2 Members, POINts ... STANdard"""
	POINts = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class StoreType(Enum):
	"""2 Members, CHANnel ... INSTrument"""
	CHANnel = 0
	INSTrument = 1


# noinspection SpellCheckingInspection
class SubBlockGaps(Enum):
	"""7 Members, AB ... GH"""
	AB = 0
	BC = 1
	CD = 2
	DE = 3
	EF = 4
	FG = 5
	GH = 6


# noinspection SpellCheckingInspection
class SweepModeC(Enum):
	"""3 Members, AUTO ... LIST"""
	AUTO = 0
	ESPectrum = 1
	LIST = 2


# noinspection SpellCheckingInspection
class SweepOptimize(Enum):
	"""3 Members, AUTO ... SPEed"""
	AUTO = 0
	DYNamic = 1
	SPEed = 2


# noinspection SpellCheckingInspection
class SweepType(Enum):
	"""3 Members, AUTO ... SWEep"""
	AUTO = 0
	FFT = 1
	SWEep = 2


# noinspection SpellCheckingInspection
class SymbolSelection(Enum):
	"""3 Members, ALL ... PATTern"""
	ALL = 0
	DATA = 1
	PATTern = 2


# noinspection SpellCheckingInspection
class Synchronization(Enum):
	"""2 Members, ALL ... NONE"""
	ALL = 0
	NONE = 1


# noinspection SpellCheckingInspection
class SyncMode(Enum):
	"""2 Members, MEAS ... SYNC"""
	MEAS = 0
	SYNC = 1


# noinspection SpellCheckingInspection
class SystemStatus(Enum):
	"""3 Members, ERR ... WARN"""
	ERR = 0
	OK = 1
	WARN = 2


# noinspection SpellCheckingInspection
class TechnologyStandardA(Enum):
	"""26 Members, GSM ... WCDMa"""
	GSM = 0
	LTE_1_40 = 1
	LTE_10_00 = 2
	LTE_15_00 = 3
	LTE_20_00 = 4
	LTE_3_00 = 5
	LTE_5_00 = 6
	NR5G_fr1_10 = 7
	NR5G_fr1_100 = 8
	NR5G_fr1_15 = 9
	NR5G_fr1_20 = 10
	NR5G_fr1_25 = 11
	NR5G_fr1_30 = 12
	NR5G_fr1_40 = 13
	NR5G_fr1_5 = 14
	NR5G_fr1_50 = 15
	NR5G_fr1_60 = 16
	NR5G_fr1_70 = 17
	NR5G_fr1_80 = 18
	NR5G_fr1_90 = 19
	NR5G_fr2_100 = 20
	NR5G_fr2_200 = 21
	NR5G_fr2_400 = 22
	NR5G_fr2_50 = 23
	USER = 24
	WCDMa = 25


# noinspection SpellCheckingInspection
class TechnologyStandardB(Enum):
	"""60 Members, AWLan ... WIMax"""
	AWLan = 0
	BWLan = 1
	CDPD = 2
	D2CDma = 3
	EUTRa = 4
	F19Cdma = 5
	F1D100nr5g = 6
	F1D20nr5g = 7
	F1U100nr5g = 8
	F1U20nr5g = 9
	F2D100nr5g = 10
	F2D200nr5g = 11
	F2U100nr5g = 12
	F2U200nr5g = 13
	F8CDma = 14
	FIS95a = 15
	FIS95c0 = 16
	FIS95c1 = 17
	FJ008 = 18
	FTCDma = 19
	FW3Gppcdma = 20
	FWCDma = 21
	GSM = 22
	L03R = 23
	L03S = 24
	L05R = 25
	L05S = 26
	L10R = 27
	L10S = 28
	L14R = 29
	L14S = 30
	L15R = 31
	L15S = 32
	L20R = 33
	L20S = 34
	M2CDma = 35
	MSR = 36
	NONE = 37
	NR5G = 38
	NR5Glte = 39
	PAPCo25 = 40
	PDC = 41
	PHS = 42
	R19Cdma = 43
	R8CDma = 44
	REUTra = 45
	RFID14443 = 46
	RIS95a = 47
	RIS95c0 = 48
	RIS95c1 = 49
	RJ008 = 50
	RTCDma = 51
	RW3Gppcdma = 52
	RWCDma = 53
	S2CDma = 54
	TCDMa = 55
	TETRa = 56
	USER = 57
	WIBRo = 58
	WIMax = 59


# noinspection SpellCheckingInspection
class TechnologyStandardDdem(Enum):
	"""3 Members, DECT ... GSM"""
	DECT = 0
	EDGE = 1
	GSM = 2


# noinspection SpellCheckingInspection
class Temperature(Enum):
	"""2 Members, COLD ... HOT"""
	COLD = 0
	HOT = 1


# noinspection SpellCheckingInspection
class TimeFormat(Enum):
	"""2 Members, DE ... US"""
	DE = 0
	US = 1


# noinspection SpellCheckingInspection
class TimeLimitUnit(Enum):
	"""2 Members, S ... SYM"""
	S = 0
	SYM = 1


# noinspection SpellCheckingInspection
class TimeOrder(Enum):
	"""2 Members, AFTer ... BEFore"""
	AFTer = 0
	BEFore = 1


# noinspection SpellCheckingInspection
class TouchscreenState(Enum):
	"""3 Members, FRAMe ... ON"""
	FRAMe = 0
	OFF = 1
	ON = 2


# noinspection SpellCheckingInspection
class TraceFormat(Enum):
	"""22 Members, BERate ... UPHase"""
	BERate = 0
	BINary = 1
	COMP = 2
	CONF = 3
	CONS = 4
	COVF = 5
	DECimal = 6
	FEYE = 7
	FREQuency = 8
	GDELay = 9
	HEXadecimal = 10
	IEYE = 11
	MAGNitude = 12
	MOVerview = 13
	NONE = 14
	OCTal = 15
	PHASe = 16
	QEYE = 17
	RCONstell = 18
	RIMag = 19
	RSUMmary = 20
	UPHase = 21


# noinspection SpellCheckingInspection
class TraceModeA(Enum):
	"""6 Members, AVERage ... WRITe"""
	AVERage = 0
	MAXHold = 1
	MINHold = 2
	OFF = 3
	VIEW = 4
	WRITe = 5


# noinspection SpellCheckingInspection
class TraceModeB(Enum):
	"""4 Members, AVERage ... WRITe"""
	AVERage = 0
	MAXHold = 1
	MINHold = 2
	WRITe = 3


# noinspection SpellCheckingInspection
class TraceModeC(Enum):
	"""6 Members, AVERage ... WRITe"""
	AVERage = 0
	BLANk = 1
	MAXHold = 2
	MINHold = 3
	VIEW = 4
	WRITe = 5


# noinspection SpellCheckingInspection
class TraceModeD(Enum):
	"""2 Members, MAXHold ... WRITe"""
	MAXHold = 0
	WRITe = 1


# noinspection SpellCheckingInspection
class TraceModeE(Enum):
	"""3 Members, AVERage ... WRITe"""
	AVERage = 0
	MAXHold = 1
	WRITe = 2


# noinspection SpellCheckingInspection
class TraceModeF(Enum):
	"""7 Members, AVERage ... WRITe"""
	AVERage = 0
	BLANk = 1
	DENSity = 2
	MAXHold = 3
	MINHold = 4
	VIEW = 5
	WRITe = 6


# noinspection SpellCheckingInspection
class TraceModeH(Enum):
	"""3 Members, BLANk ... WRITe"""
	BLANk = 0
	VIEW = 1
	WRITe = 2


# noinspection SpellCheckingInspection
class TraceNumber(Enum):
	"""15 Members, BTOBits ... TRACe6"""
	BTOBits = 0
	BTOFm = 1
	ESPLine = 2
	HMAXhold = 3
	LIST = 4
	PSPectrum = 5
	SGRam = 6
	SPECtrogram = 7
	SPURious = 8
	TRACe1 = 9
	TRACe2 = 10
	TRACe3 = 11
	TRACe4 = 12
	TRACe5 = 13
	TRACe6 = 14


# noinspection SpellCheckingInspection
class TracePresetType(Enum):
	"""3 Members, ALL ... MCM"""
	ALL = 0
	MAM = 1
	MCM = 2


# noinspection SpellCheckingInspection
class TraceReference(Enum):
	"""3 Members, BURSt ... TRIGger"""
	BURSt = 0
	PATTern = 1
	TRIGger = 2


# noinspection SpellCheckingInspection
class TraceRefType(Enum):
	"""4 Members, ERRor ... TCAP"""
	ERRor = 0
	MEAS = 1
	REF = 2
	TCAP = 3


# noinspection SpellCheckingInspection
class TraceSymbols(Enum):
	"""4 Members, BARS ... ON"""
	BARS = 0
	DOTS = 1
	OFF = 2
	ON = 3


# noinspection SpellCheckingInspection
class TraceTypeDdem(Enum):
	"""15 Members, MSTRace ... TRACe6"""
	MSTRace = 0
	PSTRace = 1
	STRace = 2
	TRACe1 = 3
	TRACe1i = 4
	TRACe1r = 5
	TRACe2 = 6
	TRACe2i = 7
	TRACe2r = 8
	TRACe3 = 9
	TRACe3i = 10
	TRACe3r = 11
	TRACe4 = 12
	TRACe5 = 13
	TRACe6 = 14


# noinspection SpellCheckingInspection
class TraceTypeK30(Enum):
	"""4 Members, TRACe1 ... TRACe4"""
	TRACe1 = 0
	TRACe2 = 1
	TRACe3 = 2
	TRACe4 = 3


# noinspection SpellCheckingInspection
class TraceTypeK60(Enum):
	"""8 Members, SGRam ... TRACe6"""
	SGRam = 0
	SPECtrogram = 1
	TRACe1 = 2
	TRACe2 = 3
	TRACe3 = 4
	TRACe4 = 5
	TRACe5 = 6
	TRACe6 = 7


# noinspection SpellCheckingInspection
class TraceTypeList(Enum):
	"""7 Members, LIST ... TRACe6"""
	LIST = 0
	TRACe1 = 1
	TRACe2 = 2
	TRACe3 = 3
	TRACe4 = 4
	TRACe5 = 5
	TRACe6 = 6


# noinspection SpellCheckingInspection
class TraceTypeNumeric(Enum):
	"""6 Members, TRACe1 ... TRACe6"""
	TRACe1 = 0
	TRACe2 = 1
	TRACe3 = 2
	TRACe4 = 3
	TRACe5 = 4
	TRACe6 = 5


# noinspection SpellCheckingInspection
class TriggerOutType(Enum):
	"""3 Members, DEVice ... UDEFined"""
	DEVice = 0
	TARMed = 1
	UDEFined = 2


# noinspection SpellCheckingInspection
class TriggerPort(Enum):
	"""4 Members, EXT1 ... OFF"""
	EXT1 = 0
	EXT2 = 1
	HOST = 2
	OFF = 3


# noinspection SpellCheckingInspection
class TriggerSeqSource(Enum):
	"""40 Members, ACVideo ... VIDeo"""
	ACVideo = 0
	AF = 1
	AM = 2
	AMRelative = 3
	BBPower = 4
	EXT2 = 5
	EXT3 = 6
	EXT4 = 7
	EXTernal = 8
	FM = 9
	GP0 = 10
	GP1 = 11
	GP2 = 12
	GP3 = 13
	GP4 = 14
	GP5 = 15
	IFPower = 16
	IMMediate = 17
	INTernal = 18
	IQPower = 19
	LXI = 20
	MAGNitude = 21
	MAIT = 22
	MANual = 23
	MASK = 24
	PM = 25
	PMTRigger = 26
	PSENsor = 27
	RFPower = 28
	SLEFt = 29
	SMONo = 30
	SMPX = 31
	SPILot = 32
	SRDS = 33
	SRIGht = 34
	SSTereo = 35
	TDTRigger = 36
	TIME = 37
	TV = 38
	VIDeo = 39


# noinspection SpellCheckingInspection
class TriggerSourceB(Enum):
	"""30 Members, ACVideo ... TV"""
	ACVideo = 0
	AF = 1
	AM = 2
	AMRelative = 3
	BBPower = 4
	EXT2 = 5
	EXT3 = 6
	EXT4 = 7
	EXTernal = 8
	FM = 9
	GP0 = 10
	GP1 = 11
	GP2 = 12
	GP3 = 13
	GP4 = 14
	GP5 = 15
	IFPower = 16
	IMMediate = 17
	IQPower = 18
	MAGNitude = 19
	PM = 20
	RFPower = 21
	SLEFt = 22
	SMONo = 23
	SMPX = 24
	SPILot = 25
	SRDS = 26
	SRIGht = 27
	SSTereo = 28
	TV = 29


# noinspection SpellCheckingInspection
class TriggerSourceD(Enum):
	"""10 Members, EXT2 ... VIDeo"""
	EXT2 = 0
	EXT3 = 1
	EXT4 = 2
	EXTernal = 3
	IFPower = 4
	IMMediate = 5
	IQPower = 6
	PSENsor = 7
	RFPower = 8
	VIDeo = 9


# noinspection SpellCheckingInspection
class TriggerSourceE(Enum):
	"""8 Members, EXT2 ... RFPower"""
	EXT2 = 0
	EXT3 = 1
	EXTernal = 2
	IFPower = 3
	IMMediate = 4
	IQPower = 5
	MANual = 6
	RFPower = 7


# noinspection SpellCheckingInspection
class TriggerSourceListPower(Enum):
	"""10 Members, EXT2 ... VIDeo"""
	EXT2 = 0
	EXT3 = 1
	EXT4 = 2
	EXTernal = 3
	IFPower = 4
	IMMediate = 5
	LINE = 6
	LXI = 7
	RFPower = 8
	VIDeo = 9


# noinspection SpellCheckingInspection
class TriggerSourceMpower(Enum):
	"""7 Members, EXT2 ... VIDeo"""
	EXT2 = 0
	EXT3 = 1
	EXT4 = 2
	EXTernal = 3
	IFPower = 4
	RFPower = 5
	VIDeo = 6


# noinspection SpellCheckingInspection
class TuningRange(Enum):
	"""2 Members, SMALl ... WIDE"""
	SMALl = 0
	WIDE = 1


# noinspection SpellCheckingInspection
class UnitMode(Enum):
	"""2 Members, DB ... PCT"""
	DB = 0
	PCT = 1


# noinspection SpellCheckingInspection
class UpDownDirection(Enum):
	"""2 Members, DOWN ... UP"""
	DOWN = 0
	UP = 1


# noinspection SpellCheckingInspection
class UserLevel(Enum):
	"""3 Members, AUTH ... PRIV"""
	AUTH = 0
	NOAuth = 1
	PRIV = 2


# noinspection SpellCheckingInspection
class WindowDirection(Enum):
	"""4 Members, ABOVe ... RIGHt"""
	ABOVe = 0
	BELow = 1
	LEFT = 2
	RIGHt = 3


# noinspection SpellCheckingInspection
class WindowDirReplace(Enum):
	"""5 Members, ABOVe ... RIGHt"""
	ABOVe = 0
	BELow = 1
	LEFT = 2
	REPLace = 3
	RIGHt = 4


# noinspection SpellCheckingInspection
class WindowName(Enum):
	"""1 Members, FOCus ... FOCus"""
	FOCus = 0


# noinspection SpellCheckingInspection
class WindowTypeBase(Enum):
	"""5 Members, Diagram ... Spectrogram"""
	Diagram = "DIAGram"
	MarkePeakList = "PEAKlist"
	MarkeTable = "MTABle"
	ResultSummary = "RSUMmary"
	Spectrogram = "SGRam"


# noinspection SpellCheckingInspection
class WindowTypeIq(Enum):
	"""9 Members, Diagram ... Spectrum"""
	Diagram = "DIAGram"
	IqImagReal = "RIMAG"
	IqVector = "VECT"
	Magnitude = "MAGN"
	MarkePeakList = "PEAKlist"
	MarkeTable = "MTABle"
	ResultSummary = "RSUMmary"
	Spectrogram = "SGRam"
	Spectrum = "FREQ"


# noinspection SpellCheckingInspection
class WindowTypeK30(Enum):
	"""12 Members, CalPowerCold ... YfactorResult"""
	CalPowerCold = "CPCold"
	CalPowerHot = "CPHot"
	CalYfactor = "CYFactor"
	EnrMeasured = "ENR"
	GainResult = "GAIN"
	MarkerTable = "MTABle"
	NoiseFigureResult = "NOISe"
	NoiseTemperatureResult = "TEMPerature"
	PowerColdResult = "PCOLd"
	PowerHotResult = "PHOT"
	ResultTable = "RESults"
	YfactorResult = "YFACtor"


# noinspection SpellCheckingInspection
class WindowTypeK40(Enum):
	"""9 Members, FrequencyDrift ... SweepResultList"""
	FrequencyDrift = "FDRift"
	MarkerTable = "MTABle"
	PhaseNoiseDiagram = "PNOise"
	ResidualNoiseTable = "RNOise"
	SpectrumMonitor = "SPECtrum"
	SpotNoiseTable = "SNOise"
	SpurList = "SPURs"
	StabilityFreqLevel = "STABility"
	SweepResultList = "SRESults"


# noinspection SpellCheckingInspection
class WindowTypeK50(Enum):
	"""5 Members, MarkerTable ... SpurDetectionTable"""
	MarkerTable = "MTABle"
	NoiseFloorEstimate = "NESTimate"
	SpectralOverview = "SOVerview"
	SpurDetectionSpectrum = "SDETection"
	SpurDetectionTable = "SDTable"


# noinspection SpellCheckingInspection
class WindowTypeK60(Enum):
	"""15 Members, ChirpRateTimeDomain ... StatisticsTable"""
	ChirpRateTimeDomain = "CRTime"
	FmTimeDomain = "FMTime"
	FreqDeviationTimeDomain = "FDEViation"
	IqTimeDomain = "IQTime"
	MarkerTable = "MTABle"
	ParameterDistribution = "PDIStribution"
	ParameterTrend = "PTRend"
	PhaseDeviationTimeDomain = "PDEViation"
	PmTimeDomain = "PMTime"
	PMTimeDomainWrapped = "PMWRapped"
	ResultsTable = "RTABle"
	RfPowerTimeDomain = "RFPTime"
	RfSpectrum = "RFSPectrum"
	Spectrogram = "SGR"
	StatisticsTable = "STABle"


# noinspection SpellCheckingInspection
class WindowTypeK7(Enum):
	"""11 Members, AmSpectrum ... RfTimeDomain"""
	AmSpectrum = "'XTIM:AM:RELative:AFSPectrum'"
	AmTimeDomain = "'XTIM:AM:RELative'"
	FmSpectrum = "'XTIM:FM:AFSPectrum'"
	FmTimeDomain = "'XTIM:FM'"
	MarkerPeakList = "PEAKlist"
	MarkerTable = "MTABle"
	PmSpectrum = "'XTIM:PM:AFSPectrum'"
	PmTimeDomain = "'XTIM:PM'"
	ResultSummary = "RSUMmary"
	RfSpectrum = "'XTIM:SPECtrum'"
	RfTimeDomain = "'XTIM:AM'"


# noinspection SpellCheckingInspection
class WindowTypeK70(Enum):
	"""9 Members, CaptureBufferMagnAbs ... SymbolsHexa"""
	CaptureBufferMagnAbs = "CBUFfer"
	Equalizer = "EQUalizer"
	ErrorVectorMagnitude = "EVECtor"
	MeasMagnRel = "MEAS"
	ModulationAccuracy = "MACCuracy"
	ModulationErrors = "MERRor"
	MultiSource = "MCOMbination"
	RefMagnRel = "REF"
	SymbolsHexa = "SYMB"


# noinspection SpellCheckingInspection
class Xdistribution(Enum):
	"""2 Members, BINCentered ... STARtstop"""
	BINCentered = 0
	STARtstop = 1


# noinspection SpellCheckingInspection
class XyDirection(Enum):
	"""2 Members, HORizontal ... VERTical"""
	HORizontal = 0
	VERTical = 1
