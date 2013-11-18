import os
import sys
import time
from threading import Thread
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.proto.api import v1
from pysnmp.proto import rfc1155

#DADOS DO EQUIPAMENTO------------------------------#
epochBoot=time.time()
dataBoot=time.ctime(epochBoot)
tempoCancelaAberta = 60
macAddressBt='FF:FF:A2:23:32:45'
pinBt='2354'
numeroTotalInterfacesRede=2

tempoAbertura=5 #tempo permanencia cancela em aberto
voltagemControlador=5
voltagemMotor=110
potenciaSinalNfc=4
potenciaSinalBt=6

statusCancela=0
carroFrenteCancela=0    

#----------------------------------------------------#
#CONFIGURACAO DO AGENTE--------------------------#
arqConfigName = 'agente.conf'
if os.path.isfile(arqConfigName):
   arqConfig = open(arqConfigName, 'r')
   agenteIP = arqConfig.readline().rstrip().split("=")[1]
   arqConfig.close()
else:
    agenteIP = '192.168.0.105'
    #agenteIP = '127.0.0.1'



def updateData():
    while True:
        arqConfig = open(arqConfigName, 'r')
    
        arqConfig.readline() #skip ip

        global statusCancela
        statusCancela = arqConfig.readline().split("=")[1]

        global carroFrenteCancela
        carroFrenteCancela = arqConfig.readline().split("=")[1]

        global nAberturas
        nAberturas  =  arqConfig.readline().rstrip().split("=")[1]

        global nFechadas 
        nFechadas = arqConfig.readline().rstrip().split("=")[1]

        global nCarrosPassaram
        nCarrosPassaram = arqConfig.readline().rstrip().split("=")[1]

        global macAddressBt
        macAddressBt = arqConfig.readline().split("=")[1]

        
        arqConfig.close()        
        time.sleep(1)

updateThread = Thread(target=updateData)
updateThread.daemon=True
updateThread.start()

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addSocketTransport(
snmpEngine,
udp.domainName,
udp.UdpTransport().openServerMode((agenteIP, 161))
)

# SNMPv1 setup

#comunidades
#adicionamos uma comunidade com nome 'public' (-c do snmpget), para a area
#'area-da-mib2'
config.addV1System(snmpEngine, 'area-da-mib2', 'public')

#uma segunda comunidade com nome 'private' para mib da ufrgs(que
#inclui nossa mib)
config.addV1System(snmpEngine, 'mibufrgs-area', 'private')

#adiciona usuario para area da mib 2
#os oids sao passados como os parametros readSubTree e writeSubTree,
#respectivamente (ver help da documentacao)
config.addVacmUser(snmpEngine, 1, 'area-da-mib2',
                   'noAuthNoPriv', readSubTree=(1,3,6,1,2,1),writeSubTree=(1,3,6,1,2,1))

#------------------MIB - UFRGS eh a nossa RAIZ---------------------
#adiciona usuarios para area da nossa mib. (1 eh o modelo de seguranca do snmpv1)
config.addVacmUser(snmpEngine, 1, 'mibufrgs-area', 'noAuthNoPriv', readSubTree=(1,3,6,1,4,1,12619),writeSubTree=(1,3,6,1,4,1,12619))


# Get default SNMP context this SNMP engine serves
snmpContext = context.SnmpContext(snmpEngine)


#-------------------- Criando um Identificador de Objeto e um nodo UFRGS
mibBuilder = snmpContext.getMibInstrum().getMibBuilder()

#Raiz da mib
#Obtem Classes para Identificador e Nodo da mib
MibIdentifier,MibNode,NotificationType = mibBuilder.importSymbols('SNMPv2-SMI', 'MibIdentifier','MibNode','NotificationType');

ufrgs = MibIdentifier((1,3,6,1,4,1,12619)) #MibIdentifier eh um nodo(MibNode) identificador
#ufrgsNodo = MibNodo((1,3,6,1,4,1,12619)) #MibIdentifier extende MibNode

#aqui exportamos o nosso objeto (instanciado a partir de MibIdentifier)
mibBuilder.exportSymbols(
'UFRGS', ufrgs
)

#------------------------------------------------------------------------
#--------------Criando o Identificador de Objeto da Nossa Mib

smartmib = MibIdentifier(ufrgs.name+(1,)) #.name armazena a tupla correspondente ao OID
#aqui exportamos o nosso objeto (instanciado a partir de MibScalar)
mibBuilder.exportSymbols(
'SMART-MIB', smartmib
)
#---------------------------------------------------------------
#restante dos identificadores
general = MibNode(smartmib.name+(1,))
cards = MibNode(smartmib.name+(2,))
stats = MibNode(smartmib.name+(3,))
hw = MibNode(smartmib.name+(4,))
network = MibNode(smartmib.name+(5,))



mibBuilder.exportSymbols(general,cards,stats,hw,network)
#MibScalar eh a classe que representara o nodo(raiz) escalar,
#MibScalarInstance eh a classe que representa a instancia desse valor
MibScalar, MibScalarInstance = mibBuilder.importSymbols(
'SNMPv2-SMI', 'MibScalar', 'MibScalarInstance'
)
MibTable,MibTableRow,MibTableColumn = mibBuilder.importSymbols(
'SNMPv2-SMI', 'MibTable', 'MibTableRow', 'MibTableColumn'
)


#Aqui definimos a classe para nosso valor de instancia. Obs.: ela extende
#a classe de representacao de instancias do pysnmp. Coloquei mais um parametro 'Valor' com o valor do escalar
class MyStaticMibScalarInstance(MibScalarInstance):


    def __init__(self,typeName,instId,syntax,Valor): 
        self.valor=Valor

        MibScalarInstance.__init__(self,typeName,instId,syntax)

    def getValue(self, name, idx):
        return self.getSyntax().clone(
            self.valor 
        )

    def setValue(self,value, name, idx):
        self.valor=value
        return self.getSyntax().clone(
            self.valor
        )

class MyTimeMibScalarInstance(MibScalarInstance):


    def getValue(self, name, idx):
        return self.getSyntax().clone(
            time.time()-epochBoot
        )



class MyTempoAberturaMibScalarInstance(MibScalarInstance):

    def getValue(self, name, idx):
        return self.getSyntax().clone(
            tempoAbertura
        )

class MyNAberturasMibScalarInstance(MibScalarInstance):

    def getValue(self, name, idx):
        return self.getSyntax().clone(
            nAberturas
        )

class MyNFechadasMibScalarInstance(MibScalarInstance):

    def getValue(self, name, idx):
        return self.getSyntax().clone(
            nFechadas
        )

class MyNCarrosPassaramMibScalarInstance(MibScalarInstance):

    def getValue(self, name, idx):
        return self.getSyntax().clone(
            nCarrosPassaram
        )

class MyMacAddressBtMibScalarInstance(MibScalarInstance):


    def getValue(self, name, idx):
        return self.getSyntax().clone(
            macAddressBt
        )


class MyStatusCancelaMibScalarInstance(MibScalarInstance):


    def getValue(self, name, idx):
        return self.getSyntax().clone(
            statusCancela
        )


class MyCarroFrenteCancelaMibScalarInstance(MibScalarInstance):


    def getValue(self, name, idx):
        return self.getSyntax().clone(
            carroFrenteCancela
        )

trapFirmwareUpdate = NotificationType(general.name +(2,)).setObjects(*(("SMART-MIB", "gateTimeUp"), ) )

#aqui exportamos o escalar e suas instancias (instanciados a partir das classe MibScalar e MyStaticMibScalarInstance)
mibBuilder.exportSymbols(
'SMART-MIB',
    trapFirmwareUpdate, 
    #----smartmib.general----#

    #obs: OctetString e os outros tipos sao definidos em v1.py
    MibScalar(general.name+(1,), v1.OctetString()).setMaxAccess('readwrite'), MyStaticMibScalarInstance(general.name+(1,), (0,), v1.OctetString(),"Cancela Smart LTDA."),
    MibScalar(general.name+(2,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(2,), (0,), v1.OctetString(),"Firmware MIBFIRM"),
    MibScalar(general.name+(3,), v1.Gauge()), MyStaticMibScalarInstance(general.name+(3,), (0,), v1.Gauge(),"1"),

    ##deve ser calculado a todo o momento
    MibScalar(general.name+(4,), v1.TimeTicks()), MyTimeMibScalarInstance(general.name+(4,), (0,), v1.TimeTicks()),

    MibScalar(general.name+(5,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(5,), (0,), v1.OctetString(),dataBoot),
    MibScalar(general.name+(6,), v1.TimeTicks()).setMaxAccess('readwrite'), MyStaticMibScalarInstance(general.name+(6,), (0,), v1.TimeTicks(),tempoAbertura),
   
    #deve ser controlado pela interface 
    MibScalar(general.name+(7,), v1.Gauge()), MyStatusCancelaMibScalarInstance(general.name+(7,), (0,), v1.Gauge()), 
    
    MibScalar(general.name+(8,), v1.Gauge()), MyCarroFrenteCancelaMibScalarInstance(general.name+(8,), (0,), v1.Gauge()),
    MibScalar(general.name+(9,), v1.Integer()), MyStaticMibScalarInstance(general.name+(9,), (0,), v1.Integer(),0),

    #----smartmib.cards----#
    MibTable(cards.name+(1,)).setMaxAccess('readcreate'),
    MibTableRow(cards.name+(1,1)).setMaxAccess('readcreate').setIndexNames((0, 'SMART-MIB', 'cardId')),
    MibTableColumn(cards.name+(1,1,1), v1.Integer()), #cardId - index da tabela
        MyStaticMibScalarInstance(cards.name+(1,1,1), (0,), v1.Integer(),1456),#instancia0
        MyStaticMibScalarInstance(cards.name+(1,1,1), (10,), v1.Integer(),223),#instancia1
        MyStaticMibScalarInstance(cards.name+(1,1,1), (35,), v1.Integer(),789),#instancia2


    MibTableColumn(cards.name+(1,1,2), v1.OctetString()).setMaxAccess('readcreate'), #cardDescription
        MyStaticMibScalarInstance(cards.name+(1,1,2), (0,), v1.OctetString(),"Bluetooth"),#instancia0
        MyStaticMibScalarInstance(cards.name+(1,1,2), (10,), v1.OctetString(),"RFID"),#instancia1
        MyStaticMibScalarInstance(cards.name+(1,1,2), (35,), v1.OctetString(),"QRCODE"),#instancia2


    MibTableColumn(cards.name+(1,1,3), v1.Counter()).setMaxAccess('readcreate'), #cardCount
        MyStaticMibScalarInstance(cards.name+(1,1,3), (0,), v1.Counter(),10),#instancia0
        MyStaticMibScalarInstance(cards.name+(1,1,3), (10,), v1.Counter(),4),#instancia1
        MyStaticMibScalarInstance(cards.name+(1,1,3), (35,), v1.Counter(),8),#instancia2


    #----smartmib.stats----#
    MibScalar(stats.name+(1,), v1.Counter()), MyNAberturasMibScalarInstance(stats.name+(1,), (0,), v1.Counter()),
    MibScalar(stats.name+(2,), v1.Counter()), MyNFechadasMibScalarInstance(stats.name+(2,), (0,), v1.Counter()),
    MibScalar(stats.name+(3,), v1.Counter()), MyNCarrosPassaramMibScalarInstance(stats.name+(3,), (0,), v1.Counter()),
    MibScalar(stats.name+(4,), v1.Counter()), MyStaticMibScalarInstance(stats.name+(4,), (0,), v1.Counter(),0),

    #----smartmib.hw----#
    MibScalar(hw.name+(1,), v1.TimeTicks()), MyTempoAberturaMibScalarInstance(hw.name+(1,), (0,), v1.TimeTicks()),
    MibScalar(hw.name+(2,), v1.Integer()), MyStaticMibScalarInstance(hw.name+(2,), (0,), v1.Integer(),voltagemControlador),
    MibScalar(hw.name+(3,), v1.Integer()), MyStaticMibScalarInstance(hw.name+(3,), (0,), v1.Integer(),voltagemMotor),
    MibScalar(hw.name+(4,), v1.Gauge()), MyStaticMibScalarInstance(hw.name+(4,), (0,), v1.Gauge(),potenciaSinalNfc),
    MibScalar(hw.name+(5,), v1.Gauge()), MyStaticMibScalarInstance(hw.name+(5,), (0,), v1.Gauge(),potenciaSinalBt),


    #----smartmib.network----#   
    #testar o network address e adicionar ao criar a tabela ifTable logo abaixo 
    #**alterar para NetworkAddress()
    MibScalar(network.name+(1,), v1.OctetString()), MyMacAddressBtMibScalarInstance(network.name+(1,), (0,), v1.OctetString()),
    MibScalar(network.name+(2,), v1.OctetString()).setMaxAccess('readwrite'), MyStaticMibScalarInstance(network.name+(2,), (0,), v1.OctetString(),pinBt),
    MibScalar(network.name+(3,), v1.Integer()), MyStaticMibScalarInstance(network.name+(3,), (0,), v1.Integer(),numeroTotalInterfacesRede),
    
    MibTable(network.name+(4,)).setMaxAccess('readcreate'),
    MibTableRow(network.name+(4,1)).setMaxAccess('readcreate').setIndexNames((0, 'SMART-MIB', 'ifId')),
    MibTableColumn(network.name+(4,1,1), v1.Integer()).setMaxAccess('readcreate'), #ifId - index da tabela
        MyStaticMibScalarInstance(network.name+(4,1,1), (0,), v1.Integer(),0),#instancia0
        MyStaticMibScalarInstance(network.name+(4,1,1), (100,), v1.Integer(),50),#instancia1
    MibTableColumn(network.name+(4,1,2), v1.OctetString()).setMaxAccess('readcreate'), #ifMacAddress    
        MyStaticMibScalarInstance(network.name+(4,1,2), (0,), v1.OctetString(),"AA:BB:CC:FF:EE:DD"), #instancia1
        MyStaticMibScalarInstance(network.name+(4,1,2), (100,), v1.OctetString(),"D5:76:00:00:C5:03"), #instancia 2
    MibTableColumn(network.name+(4,1,3), v1.Integer()).setMaxAccess('readcreate'), #ifType    
        MyStaticMibScalarInstance(network.name+(4,1,3), (0,), v1.Integer(),0), #instancia1
        MyStaticMibScalarInstance(network.name+(4,1,3), (100,), v1.Integer(),1)  #instancia2

)


# --- end of Managed Object Instance initialization ----



# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)

# Register an imaginary never-ending job to keep I/O dispatcher running forever
snmpEngine.transportDispatcher.jobStarted(1)
# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
