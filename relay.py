#!/usr/bin/env python3
import serial
import time
import argparse
import struct


#Relay Def
k1_val=0x01
k2_val=0x02
k3_val=0x04
k4_val=0x08
k1_name="k1"
k2_name="k2"
k3_name="k3"
k4_name="k4"
kOff="on"
kOn="off"

relayPossibleValue=[k1_name,k2_name,k3_name,k4_name,kOn,kOff]

relayHelp=("Set the Relay Value, possible values 'k1' to 'k4', with 'on' or 'off' : " + "\n"
                   "eg : './relay.py --port /dev/ttyUSB1 --relay k1 on' " + "\n"
                   "if 'on' or 'off' is omited relay is considered as 'on'" + "\n"
                   "'on' is represented by Red LED OFF on the board" + "\n"
                   "'off' is represented by Red LED ON on the board" )


# Debug Def
INFO=1
WARN=2
ERROR=3

# Serial Port
serialPort=None

#######################################################################################################################
#######################################################################################################################
############################################     function section       ###############################################
#######################################################################################################################
#######################################################################################################################

def areRelayArgsOk(relayArgs):
    # To lowercase
    localRelayArgs=[x.lower() for x in relayArgs]
    # Check key words
    for args in localRelayArgs:
        if args not in relayPossibleValue:
            return False
    #check first arg, must be k1,k2,k3 or k4
    if localRelayArgs[0] not in relayPossibleValue[0:4]:
        return False

    return True

def getRelayState(relayName, relayArgs):

    indexRelayName=relayArgs.index(relayName)

    if ((indexRelayName+1) < len(relayArgs)) :
        if relayArgs[indexRelayName+1] == kOff :
            return kOff
        else:
            return kOn
    else :
        return kOn

def getRelayConfig(relayArgs):
    # To lowercase
    localRelayArgs=[x.lower() for x in relayArgs]
    result = 0
    if k1_name in localRelayArgs :
        if getRelayState(k1_name,localRelayArgs) == kOn:
            result |= k1_val
    if k2_name in localRelayArgs :
        if getRelayState(k2_name,localRelayArgs) == kOn:
            result |= k2_val
    if k3_name in localRelayArgs :
        if getRelayState(k3_name,localRelayArgs) == kOn:
            result |= k3_val
    if k4_name in localRelayArgs :
        if getRelayState(k4_name,localRelayArgs) == kOn:
            result |= k4_val

    return struct.pack('!B',result)

def closeSerialAndExit():
    serialPort.close()
    quit()

#######################################################################################################################
#######################################################################################################################
##############################################     main section      ##################################################
#######################################################################################################################
#######################################################################################################################
if __name__ == '__main__':

    example_text = '''example:
 python relay.py --port /dev/ttyUSB1 --init             # Board Initialization
 python relay.py --port /dev/ttyUSB1 --relay k1 on      # Switch On the first relay
 python relay.py --port /dev/ttyUSB1 --allrelay off     # Switch Off all relay
 python relay.py --port /dev/ttyUSB1 --cutom 8          # Switch On k4 relay
 '''

    parser = argparse.ArgumentParser(prog='python relay.py',
                                     description='USB relay control, brand: http://www.icstation.com/ , model: ICSE012A',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-p", "--port", help="Set the serial port eg: /dev/ttyUSB0 .", required=True)
    parser.add_argument("-b", "--baudrate", help="Set the serial port baudrate, default value : 9600", type=int)
    parser.add_argument("-t", "--timeout", help="Set the serial port timeout, default value : Infinite", type=int)
    parser.add_argument("-i", "--init", help="Init the relay, to be done once after plugging the board",action='store_true')
    parser.add_argument("-r", "--relay", nargs='*', help=relayHelp)
    parser.add_argument("-a", "--allrelay", help="All relay 'On' or 'Off'. If 'on' or 'off' is omited relay is considered as 'on'")
    parser.add_argument("-c", "--custom", help="Send raw command (int) to relay board",type=int)
    parser.add_argument('-v', '--verbosity', action="count", help="increase output verbosity (e.g., -vv is more than -v)")


    args = parser.parse_args()

    argPort = args.port

    if args.baudrate is None:
        argBaudrate = 9600
    else:
        argBaudrate = args.baudrate

    if args.timeout is None:
        argTimeout = None
    else:
        argTimeout = args.timeout

    if args.verbosity:
        def _v_print(*verb_args):
            if verb_args[0] > (ERROR - args.verbosity):
                print (verb_args[1])
    else:
        _v_print = lambda *a: None  # do-nothing function

    global v_print
    v_print = _v_print

# Configure serial
    try:
        serialPort = serial.Serial(
            port=argPort,
            baudrate=argBaudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=argTimeout
        )
    except:
        print( "Serial port " + argPort +" not found")
        quit()

# Do relay init if needed
    if args.init is True:
        serialPort.write(struct.pack('!B',0x50))
        time.sleep(0.1)
        serialPort.write(struct.pack('!B',0x51))
        v_print(INFO, "Init Done")

# Send cmd to all relay if needed
    if args.allrelay:
        if args.allrelay.lower() == kOn:
            serialPort.write(struct.pack('!B',k1_val+k2_val+k3_val+k4_val))
            v_print(INFO, args.allrelay + " all relay command applied")
            closeSerialAndExit()

        elif args.allrelay.lower() == kOff:
            serialPort.write(struct.pack('!B',0))
            v_print(INFO,  args.allrelay + " all relay command applied")
            closeSerialAndExit()

        else:
            v_print(INFO,  args.allrelay + " Wrong all relay command")
            closeSerialAndExit()

# Send cmd to relay if needed
    if args.relay:
        if areRelayArgsOk(args.relay) is not True:
            v_print(INFO, " ".join(str(x) for x in args.relay) + " Wrong relay command")
            v_print(INFO, relayHelp)
            closeSerialAndExit()
        else:
            serialPort.write(getRelayConfig(args.relay))
            v_print(INFO, " ".join(str(x) for x in args.relay) + " relay command applied")
            closeSerialAndExit()

# Send raw cmd to relay if needed
    if args.custom != None:
        serialPort.write(struct.pack('!B',args.custom))
        v_print(INFO, str(args.custom) + " custom command applied")
        closeSerialAndExit()


    closeSerialAndExit()
