import sigrokdecode as srd
from struct import *

#from sigrokdecode.common import *
#annload-config, ann_load-program, ann_load-data, ann_read-program, ann_read-data, ann_inc-addr, ann_begin-prog-int, ann_begin-prog-ext, ann_end-prog, ann_erase-prog, ann_erase-data, ann_bit, ann_warnings = range(13) 

class Decoder(srd.Decoder):
    api_version = 3
    id = 'pic12'
    name = 'pic12'
    longname = 'PIC12 In Circuit Serial Programmer'
    desc = 'Two-wire, serial bus.'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = ['PIC12']
    channels = (
        {'id': 'pgc', 'name': 'PGC', 'desc': 'Program clock line'},
        {'id': 'pgd', 'name': 'PGD', 'desc': 'Program data line'},
    )
    tags     = ['Debug/trace',]
    optional_channels = (
        {'id': 'vcc', 'name': 'VCC', 'desc': 'Target Voltage'},
        {'id': 'vpp', 'name': 'VPP', 'desc': 'Programming Voltage'},
    )
    options = (
        {'id': 'chip_model', 'desc': 'Chip Model', 'default': 'default',
            'values': ('default', 'PIC12F629',)},
        {'id': 'start_address', 'desc': 'Address at chip reset', 'default': 0}, 
        {'id': 'glitch_filter', 'desc': 'Glitch Filter Delay (in uS)', 'default': 0.1},
        {'id': 'TDLY', 'desc': 'delay between command and data (in uS)', 'default': 1},
        {'id': 'TPROG', 'desc': 'program write delay (in uS)', 'default': 2000}, 
    )
    annotations = (
        ('bit', 'data bit'),
        ('command', 'command data'), 
        ('picaddress', 'current PIC address'), 
    )
    annotation_rows = (
        ('bits', 'Bits', (0,)),
        ('commands', 'Command', (1,)),
        ('address','PIC Address', (2,)),
    )
    binary = (
        ('loadchip', 'Binary Loaded to Chip'),
        ('readchip', 'Binary Read from Chip'),
    )
    def __init__(self, **kwargs):
        self.reset()
        self.state = "FIND COMMAND"
        self.prevSample = 0
        self.command = 0 
        self.picaddress = 0 

    def reset(self):
        self.samplerate = None
        self.bitcount = 0
        self.state = "FIND COMMAND" 
        self.prevSample = 0
        self.command = 0
        self.picaddress = 0 
    
    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value
    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)
        self.out_python = self.register(srd.OUTPUT_PYTHON)
        self.out_binary = self.register(srd.OUTPUT_BINARY)

        if self.options['chip_model'] == 'default': #pull values from inputs
            self.picaddress = self.options['start_address']
            self.glitchfilter = self.options['glitch_filter']
            self.tdly = self.options['TDLY']
            self.tprog = self.options['TPROG']
        elif self.options['chip_model'] == 'pic12f629': 
            self.picaddress = 0 
            self.glitchfilter = 0.1 
            self.tdly = 3.5 
            self.tprog = self.options['TPROG']

    def decode(self):
        commandcounter = 0 #store current command
        #commandbits = list() 
        while True: 
           clockbit, databit,vcc,vpp  = self.wait({0: 'h'}) #filter???
           #make sure it's not a glitch value
           self.wait({'skip': round(0.1 * (self.samplerate/1000000))}) #wait 100ns
           clockbit, databit,vcc,vpp  = self.wait({0: 'f'}) #get clock falling edge
 
           n = self.samplenum
           self.put(n-1, n+1, self.out_ann, [0, [str(databit)]])
           if self.prevSample == 0: #store inital command sample
              self.prevSample = n 
           if(int(databit) == 1):
               self.command = self.command | 0x20 
           commandcounter = commandcounter + 1
           self.wait({'skip': round(1.5 * (self.samplerate/1000000))}) #wait 1.5uS between samples 
           #self.command = self.command | int(databit) 
           if(commandcounter == 6):
               commandcounter = 0
               #delay 5uS between cmd and data
               self.wait({'skip': round(3.5 * (self.samplerate/1000000))}) 
               #self.put(self.prevSample, n, self.out_ann, [1, [str(hex(self.command))]])
               if (self.command & 0x3F) == 0x00: #Load Config 
                   dataval = 0 
                   for i in range(16):
                       dataval = dataval >> 1
                       clockbit, databit,vcc,vpp  = self.wait({0: 'f'}) #get next 16 bits
                       self.wait({'skip': round(0.4 * (self.samplerate/1000000))}) #wait 0.4uS between samples 
                       if(int(databit) == 1):
                           dataval = dataval | 0x8000
                   dataval = dataval >> 1
                   dataval = dataval & 0x3FFF
                   self.picaddress = 0x2000
                   self.put(self.prevSample, self.samplenum, self.out_ann, [1, ["Load Config:" + hex(dataval)]])
                   self.put(self.prevSample, self.samplenum, self.out_ann, [2, [hex(self.picaddress)]])
               if (self.command & 0x3F) == 0x02: #Load Data for Program Memory
                   dataval = 0 
                   for i in range(16):
                       dataval = dataval >> 1
                       clockbit, databit,vcc,vpp  = self.wait({0: 'f'}) #get next 16 bits
                       self.wait({'skip': round(0.4 * (self.samplerate/1000000))}) #wait 0.4uS between samples 
                       if(int(databit) == 1):
                           dataval = dataval | 0x8000
                   dataval = dataval >> 1
                   dataval = dataval & 0x3FFF
                   self.put(self.prevSample, self.samplenum, self.out_ann, [1, ["Load Prog:" + hex(dataval)]])
                   self.put(self.prevSample, self.samplenum, self.out_binary, [0, dataval.to_bytes(2, byteorder='big')])
               if (self.command & 0x3F) == 0x03: #Load Data for Data Memory
                   dataval = 0 
                   for i in range(16):
                       dataval = dataval >> 1
                       clockbit, databit,vcc,vpp  = self.wait({0: 'f'}) #get next 16 bits
                       self.wait({'skip':round(0.4 * (self.samplerate/1000000))}) #wait 0.4uS between samples 
                       if(int(databit) == 1):
                           dataval = dataval | 0x8000
                   dataval = dataval >> 1
                   dataval = dataval & 0x3FFF
                   self.put(self.prevSample, self.samplenum, self.out_ann, [1, ["Load Data:" + hex(dataval)]])
                   #self.put(self.prevSample, self.samplenum, self.out_binary, [0, dataval.to_bytes(2, byteorder='little')])
               if (self.command & 0x3F) == 0x04: #Read Data from Program Memory
                   dataval = 0 
                   for i in range(16):
                       dataval = dataval >> 1
                       clockbit, databit,vcc,vpp  = self.wait({0: 'f'}) #get next 16 bits
                       self.wait({'skip': round(0.4 * (self.samplerate/1000000))}) #wait 0.4uS between samples 
                       if(int(databit) == 1):
                           dataval = dataval | 0x8000
                   dataval = dataval >> 1
                   dataval = dataval & 0x3FFF
                   self.put(self.prevSample, self.samplenum, self.out_ann, [1, ["Read Prog:" + hex(dataval)]])
                   self.put(self.prevSample, self.samplenum, self.out_binary, [1, dataval.to_bytes(2, byteorder='big')])
               if (self.command & 0x3F) == 0x05: #Read Data from Data Memory 
                   dataval = 0 
                   for i in range(16):
                       dataval = dataval >> 1
                       clockbit, databit,vcc,vpp  = self.wait({0: 'f'}) #get next 16 bits
                       self.wait({'skip': round(0.4 * (self.samplerate/1000000))}) #wait 0.4uS between samples 
                       if(int(databit) == 1):
                           dataval = dataval | 0x8000
                   dataval = dataval >> 1
                   dataval = dataval & 0x3FFF
                   self.put(self.prevSample, self.samplenum, self.out_ann, [0, ["Read Data:" + hex(dataval)]])
               if (self.command & 0x3F) == 0x06: #Increment Address
                   self.picaddress = self.picaddress + 1 
                   self.put(self.prevSample, n, self.out_ann, [1, ["Increment Address:" + hex(self.command)]])
                   self.put(self.prevSample, n, self.out_ann, [2, [hex(self.picaddress)]])
               if self.command == 0x08: #Begin Programming
                   self.put(self.prevSample, n, self.out_ann, [1, ["Begin Programming:" + hex(self.command)]])
               if self.command == 0x18: #Begin Programming
                   self.put(self.prevSample, n, self.out_ann, [1, ["Begin Programming:" +hex(self.command)]])
               if self.command == 0x0A: #End Programming
                   self.put(self.prevSample, n, self.out_ann, [1, ["End Programming:" +hex(self.command)]])
               if (self.command | 0x30) == 0x09: #Bulk Erase Program Memory
                   self.put(self.prevSample, n, self.out_ann, [1, ["Erase Program:" +hex(self.command)]])
               if (self.command | 0x30) == 0x0B: #Bulk Erase Data Memory
                   self.put(self.prevSample, n, self.out_ann, [1, ["Erase Data:" +hex(self.command)]])
               self.prevSample = 0
               self.command = 0
           self.command = self.command >> 1
                

