# usbrelay
usb relay command in python

This python script is design to control ICSE012A board from [icstation](http://www.icstation.com/).

 *Features :*
 - [x] Board initialization
 - [x] Individual relay control 
 - [x] Global relay control
 - [x] Custom relay controls
 - [ ] Reading relay state ( I didn't have any clue to do so) 
 - [ ] Modifying one relay state without modifying others by reading relay state

*Help output*

```~$ ./relay.py --help 
usage: python relay.py [-h] -p PORT [-b BAUDRATE] [-t TIMEOUT] [-i]
                       [-r [RELAY [RELAY ...]]] [-a ALLRELAY] [-c CUSTOM]

USB relay control, brand: http://www.icstation.com/ , model: ICSE012A

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Set the serial port eg: /dev/ttyUSB0 .
  -b BAUDRATE, --baudrate BAUDRATE
                        Set the serial port baudrate, default value : 9600
  -t TIMEOUT, --timeout TIMEOUT
                        Set the serial port timeout, default value : Infinite
  -i, --init            Init the relay, to be done once after plugging the
                        board
  -r [RELAY [RELAY ...]], --relay [RELAY [RELAY ...]]
                        Set the Relay Value, possible values 'k1' to 'k4',
                        with 'on' or 'off' : eg : './relay.py --port
                        /dev/ttyUSB1 --relay k1 on' if 'on' or 'off' is omited
                        relay is considered as 'on' 'on' is represented by Red
                        LED OFF on the board 'off' is represented by Red LED
                        ON on the board
  -a ALLRELAY, --allrelay ALLRELAY
                        All relay 'On' or 'Off'. If 'on' or 'off' is omited
                        relay is considered as 'on'
  -c CUSTOM, --custom CUSTOM
                        Send raw command (int) to relay board

example:
 python relay.py --port /dev/ttyUSB1 --init             # Board Initialization
 python relay.py --port /dev/ttyUSB1 --relay k1 on      # Switch On the first relay
 python relay.py --port /dev/ttyUSB1 --allrelay off     # Switch Off all relay
 python relay.py --port /dev/ttyUSB1 --cutom 8          # Switch On k4 relay
```
