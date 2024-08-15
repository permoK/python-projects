# from pysnmp.hlapi import *

# def send_snmp_shutdown(ip):
#     errorIndication, errorStatus, errorIndex, varBinds = next(
#         setCmd(SnmpEngine(),
#                CommunityData('public', mpModel=0),
#                UdpTransportTarget((ip, 161)),
#                ContextData(),
#                ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.3.1.1'), Integer(2)))  # Replace with correct OID and value
#     )

#     if errorIndication:
#         print(errorIndication)
#     elif errorStatus:
#         print('%s at %s' % (errorStatus.prettyPrint(),
#                             errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#     else:
#         print('SNMP command sent successfully.')

# # Replace '192.168.1.100' with your printer's IP address
# send_snmp_shutdown('172.16.3.29')

from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, setCmd

def send_snmp_shutdown(ip):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),  # Replace 'public' with the correct community string if needed
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.3.1.1'), Integer(2)))  # Replace with correct OID and value
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        print('SNMP command sent successfully.')

# Replace '172.16.3.29' with your printer's IP address
send_snmp_shutdown('172.16.3.29')

