import sys
import time
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.proto.api import v1

#DADOS DO EQUIPAMENTO------------------------------#
epochBoot=time.time()
dataBoot=time.ctime(epochBoot)
tempoCancelaAberta = 60



#----------------------------------------------------#

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('192.168.57.1', 161))
)

# SNMPv1 setup

# SecurityName <-> CommunityName mapping.
# Here we configure two distinct CommunityName's to control read and write
# operations.
config.addV1System(snmpEngine, 'my-read-area', 'public')
config.addV1System(snmpEngine, 'my-write-area', 'private')
config.addV1System(snmpEngine, 'my-mibsmart-area', 'public') #adiciona comunidade publica

# Allow full MIB access for this user / securityModels at VACM
config.addVacmUser(snmpEngine, 1, 'my-read-area',
                   'noAuthNoPriv', (1,3,6,1,2,1))
config.addVacmUser(snmpEngine, 1, 'my-write-area',
                   'noAuthNoPriv', (1,3,6,1,2,1), (1,3,6,1,2,1))

#------------------MIB - UFRGS eh a nossa RAIZ---------------------
# Permite usuarios consultarem nossa MIB
config.addVacmUser(snmpEngine, 1, 'my-mibsmart-area', 'noAuthNoPriv', (1,3,6,1,4,1,12619))


# Get default SNMP context this SNMP engine serves
snmpContext = context.SnmpContext(snmpEngine)


#-------------------- Criando um Identificador de Objeto e um nodo UFRGS
mibBuilder = snmpContext.getMibInstrum().getMibBuilder()

#Raiz da mib
#Obtem Classes para Identificador e Nodo da mib
MibIdentifier,MibNode = mibBuilder.importSymbols('SNMPv2-SMI', 'MibIdentifier','MibNode')

ufrgs = MibIdentifier((1,3,6,1,4,1,12619,)) #MibIdentifier eh um nodo(MibNode) identificador
#ufrgsNodo = MibNodo((1,3,6,1,4,1,12619,)) #MibIdentifier extende MibNode

#aqui exportamos o nosso objeto (instanciado a partir de MibScalar)
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
 
#Aqui definimos a classe para nosso valor de instancia. Obs.: ela extende
#a classe de representacao de instancias do pysnmp. Coloquei mais um parametro 'Valor' com o valor do escalar
class MyStaticMibScalarInstance(MibScalarInstance):

    
    def __init__(self,typeName,instId,syntax,Valor): 
        self.valor=Valor

        MibScalarInstance.__init__(self,typeName,instId,syntax)
    
    def getValue(self, name, idx):
        return self.getSyntax().clone(
            #'Python %s running on a %s platform' % (sys.version, sys.platform)
            self.valor 
        )



#aqui exportamos o escalar e suas instancias (instanciados a partir das classe MibScalar e MyStaticMibScalarInstance)
mibBuilder.exportSymbols(
  'MIB-SMART', 
        #smartmib.general

        MibScalar(general.name+(1,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(1,), (0,), v1.OctetString(),"Cancela Smart LTDA."),
        MibScalar(general.name+(2,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(2,), (0,), v1.OctetString(),"Firmware MIBFIRM"),
        MibScalar(general.name+(3,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(3,), (0,), v1.OctetString(),"versao 1.0"),

         ##deve ser calculado a todo o momento
        MibScalar(general.name+(4,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(4,), (0,), v1.TimeTicks(),time.time()-epochBoot),

        MibScalar(general.name+(5,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(5,), (0,), v1.OctetString(),dataBoot),
        MibScalar(general.name+(6,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(6,), (0,), v1.TimeTicks(),tempoCancelaAberta),
       
        #deve ser controlado pela interface 
        MibScalar(general.name+(7,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(7,), (0,), v1.Gauge(),0), 
        
        MibScalar(general.name+(8,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(8,), (0,), v1.Gauge(),0),
        MibScalar(general.name+(9,), v1.OctetString()), MyStaticMibScalarInstance(general.name+(9,), (0,), v1.Integer(),0)
    
        #smartmib.cards
)

# --- end of Managed Object Instance initialization ----



# Register SNMP Applications at the SNMP engine for particular SNMP context
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)

# Register an imaginary never-ending job to keep I/O dispatcher running forever
snmpEngine.transportDispatcher.jobStarted(1)
# Run I/O dispatcher which would receive queries and send responses
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
