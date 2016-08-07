import binascii
from time import sleep

from HC_Exception import HC_Exception

class HC_Misc:
    """
    Class for HC Miscellaneous Commands
    from "NexStar Communication Protocol":
    http://www.celestron.com/media/795779/1154108406_nexstarcommprot.pdf
    """

    models = { 1: 'GPS Series',
               3: 'i-Series',
               4: 'i-Series SE',
               5: 'CGE',
               6: 'Advanced GT',
               7: 'SLT',
               9:  'CPC',
               10:  'GT',
               11: '4/5 SE',
               12: '6/8 SE' }

    devices = { 16:  "AZM/RA Motor",
                17:  "ALT/DEC Motor",
                176: "GPS Unit",
                178: "RTC (CGE only)" }
    
    def __init__(self,ser):
        """
        ser: serial.Serial instance with opened serial port
        """
        self.ser=ser

    def GetVersion(self):
        """
        Retrieve Version %d.$d
        """
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write("V")
        # read all params
        param_names=["Maj","Min"]
        v = { k: int(binascii.hexlify(self.ser.read()), 16) for k in param_names }
        # check for Errors 
        if status!=1 self.ser.read()!='#':
            raise HC_Exception(self, "GetVersion")
        # version str
        return '%d.%d' % ( v["Maj"], v["Min"])

    def GetDeviceVersion(self,dev):
        """
        Retrieve Device Version %d.%d or None if device is not present
        NB: sleeps for 1 sec after sending write command to get correct status

        dev - device code
        """
        # make command string
        command ='P' + ''.join( map(chr, [1,dev,254,0,0,0,2]) )
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write(command)
        # sleep to let HC to respond
        sleep(1)
        if self.ser.inWaiting()==3:
            # device present, read version
            param_names=["Maj","Min"]
            v = { k: int(binascii.hexlify(self.ser.read()), 16) for k in param_names }
            version = '%d.%d' % ( v["Maj"], v["Min"])
        else:
            # no such device, skip zero bytes
            self.ser.read(3)
            version = 'None'
        # check for Errors 
        if status!=8 or self.ser.read()!='#':
            raise HC_Exception(self, "getDeviceVersion")
        # version str
        return version

    def getModel(self):
        """
        Retrieve *numerical code* for the Model
        """
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write("m")
        # read params
        m = int(binascii.hexlify(self.ser.read()), 16)
        # check for Errors 
        if status!=1 self.ser.read()!='#':
            raise HC_Exception(self, "getModel")
        return m

    def GetModel(self):
        """
        Retrieve Model %s
        """
        return HC_Misc.models[ self.getModel() ]
        
    def Echo(self,c):
        """
        Send character c, gets echo and returns it
        """
        # make command string
        command ='K' + c
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write(command)
        # read all params
        x = self.ser.read()
        # check for Errors 
        if status!=2 or x!=c self.ser.read()!='#':
            raise HC_Exception(self, "Echo")
        # version str
        return x

    def IsAlignmentComplete(self):
        """
        Returns 0/1
        """
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write("J")
        # read 
        align = int(binascii.hexlify(self.ser.read()), 16)
        # check for Errors 
        if status!=1 self.ser.read()!='#':
            raise HC_Exception(self, "IsAlignmentComplete")
        # version str
        return align

    def IsGOTOInProgress(self):
        """
        Returns 0/1
        """
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write("J")
        # read 
        prog = self.ser.read()
        # check for Errors 
        if status!=1 self.ser.read()!='#':
            raise HC_Exception(self, "IsGOTOInProgress")
        # version str
        return 1 if prog=='1' else 0

    def CancelGOTO(self):
        """
        Cancels GOTO
        """
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write("M")
        # check for Errors 
        if status!=1 self.ser.read()!='#':
            raise HC_Exception(self, "CancelGOTO")
    
    def PrintFullInfo(self):
        s   = 'Model:      "%s"\n' % self.GetModel()
        s  += 'HC Version:  %s\n'  % self.GetVersion()
        # get devices info
        for dev,dev_str in HC_Misc.devices.items():
            s  += '%14s:  %s\n'  % (dev_str,self.GetDeviceVersion(dev))
        s  += '\n'
        s  += 'Alignment complete  : %d\n'  % self.IsAlignmentComplete()
        s  += 'Is GOTO in progress : %d\n'  % self.IsGOTOInProgress()
        print s















