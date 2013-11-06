import sys
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.proto.api import v1

# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('192.168.56.1', 161))
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

# Permite usuarios consultarem nossa MIB
config.addVacmUser(snmpEngine, 1, 'my-mibsmart-area', 'noAuthNoPriv', (1,3,6,5))


# Get default SNMP context this SNMP engine serves
snmpContext = context.SnmpContext(snmpEngine)



# --- create custom Managed Object Instance ---

mibBuilder = snmpContext.getMibInstrum().getMibBuilder()

#MibScalar eh a classe que representara o nodo(raiz) escalar,
#MibScalarInstance eh a classe que representa a instancia desse valor
MibScalar, MibScalarInstance = mibBuilder.importSymbols(
    'SNMPv2-SMI', 'MibScalar', 'MibScalarInstance'
) 

#Aqui definimos a classe para nosso valor de instancia. Obs.: ela extende
#a classe de representacao de instancias do pysnmp
class MyStaticMibScalarInstance(MibScalarInstance):
    def getValue(self, name, idx):
        return self.getSyntax().clone(
            'Python %s running on a %s platform' % (sys.version, sys.platform)
        )

#aqui exportamos o nosso objeto (instanciado a partir de MibScalar)
mibBuilder.exportSymbols(
  'MIB-SMART', MibScalar((1,3,6,5,1), v1.OctetString()),
              MyStaticMibScalarInstance((1,3,6,5,1), (0,), v1.OctetString())
)

# --- end of Managed Object Instance initialization ----



#---MIB UFRGS --#

    #Criar agora um nodo raiz, que nao seja escalar (MibScalar)


#---------------#

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
