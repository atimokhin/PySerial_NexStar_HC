import binascii

from HC_Exception import HC_Exception

class HC_TimeLocation:
    """
    Class for setting/getting time and location in Nexstar SE Hand Control (HC)
    from "NexStar Communication Protocol":
    http://www.celestron.com/media/795779/1154108406_nexstarcommprot.pdf
    """
    
    def __init__(self,ser):
        """
        ser: serial.Serial instance with opened serial port
        """
        self.ser=ser
        self.t_dict=None
        self.l_dict=None
        self.t_str=None
        self.l_str=None

    def GetLocation(self):
        """
        Retrieve time from HC and store it the class variables
        """
        # clear input
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write("w")
        # read all params
        param_names=["d_lat","m_lat","s_lat","NS","d_lon","m_lon","s_lon","EW"]
        self.l_dict = { k: int(binascii.hexlify(self.ser.read()), 16) for k in param_names }
        # check for Errors 
        if status!=1 self.ser.read()!='#':
            raise HC_Exception(self, "GetLocation")
        # make redable location representation
        self._l2str()

    def SetLocation(self, d_lat, m_lat, s_lat, NS, d_lon, m_lon, s_lon, EW):
        """
        d_lat - the number of degrees of latitude.
        m_lat - the number of minutes of latitude.
        s_lat - the number of seconds of latitude.
        NS    - 0 for north and 1 for south.
        d_lon - the number of degrees of longitude.
        m_lon - the number of minutes of longitude.
        s_lon - the number of seconds of longitude.
        EW    - 0 for east and 1 for west.
        """
        # make command string
        lat = map(chr, [d_lat, m_lat, s_lat, 0 if NS=='N' else 1] )
        lon = map(chr, [d_lon, m_lon, s_lon, 0 if EW=='E' else 1] )
        command ='W' + ''.join(lat) + ''.join(lon)
        # clear
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write(command)
        # check for Errors 
        if status!=9 self.ser.read()!='#':
            raise HC_Exception(self, "SetLocation")

    def GetTime(self):
        """
        Retrieve location from HC and store it the class variables
        """
        # clear
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write("h")
        # read all params
        param_names=["h","m","s","mon","day","yr","tz","ds"]
        self.t_dict = { k: int(binascii.hexlify(self.ser.read()), 16) for k in param_names }
        # check for Errors 
        if status!=1 self.ser.read()!='#':
            raise HC_Exception(self, "GetTime")
        # make redable time representation
        self._t2str()

    def SetTime(self, hour, minute, second, month, day, year, tz, daylight_savings):
        """
        hour   - the hour (24 hour clock).
        minute - the minutes.
        second - the seconds.
        month  - the month.
        day    - the day.
        year   - the year (century assumed as 20).
        tz     - the offset from GMT for the time zone (+/-)
        daylight_savings - 1 to enable Daylight Savings and 0 for Standard Time. 
        """
        # if zone is negative, use 256-zone
        tz = tz if tz>=0 else 256+tz
        # make command string
        t = map(chr, [hour, minute, second ] )
        d = map(chr, [month, day, year] )
        command ='H' + ''.join(t) + ''.join(d) + chr(tz) + chr(daylight_savings)
        # clear
        self.ser.flushOutput()
        self.ser.flushInput()
        # send command
        status=self.ser.write(command)
        # check for Errors 
        if status!=9 self.ser.read()!='#':
            raise HC_Exception(self, "SetTime")

    def _t2str(self):
        """
        make readable string representation of HC time and store it in self.t_str
        """
        t  = 'Time: %d:%d:%d' % (self.t_dict["h"], self.t_dict["m"], self.t_dict["s"])
        d  = 'Date: %02d/%02d/%02d' % (self.t_dict["mon"], self.t_dict["day"], self.t_dict["yr"])
        tz = 'TZ=%d' % ( self.t_dict["tz"] if self.t_dict["tz"]<128 else self.t_dict["tz"]-256 )
        ds = '%s' % ( 'Daylight Saving' if self.t_dict["ds"] else 'Standard' )
        self.t_str='%s  %s  %s %s' % (t,d,tz,ds)

    def _l2str(self):
        """
        make readable string representation of HC location and store it in self.l_str
        """
        lat  = "Latitude:  %d %d' %d\" %s" % \
               (self.l_dict["d_lat"], self.l_dict["m_lat"], self.l_dict["s_lat"], 'S' if self.l_dict["NS"] else 'N' )
        lon  = "Longitude: %d %d' %d\" %s" % \
               (self.l_dict["d_lon"], self.l_dict["m_lon"], self.l_dict["s_lon"], 'W' if self.l_dict["EW"] else 'E' )
        self.l_str='%s   %s' % (lat, lon)

    def __repr__(self):
        s  = self.t_str if self.t_str else 'Time not yet retrieved'
        s += '\n'
        s += self.l_str if self.l_str else 'Location not yet retrieved'
        return s















