#!env python

# sorry, this is very ugly, but I'm in python 2.5
import sys
sys.path.insert(0,"../..")

from dot11 import Dot11,Dot11DataFrame
from binascii import hexlify
import unittest

class TestDot11DataFrames(unittest.TestCase):

    def setUp(self):
        # 802.11 Data Frame 
        #
        self.frame_orig='\x08\x01\x30\x00\x00\x08\x54\xac\x2f\x85\x00\x23\x4d\x09\x86\xfe\x00\x08\x54\xac\x2f\x85\x40\x44\xaa\xaa\x03\x00\x00\x00\x08\x00\x45\x00\x00\x28\x72\x37\x40\x00\x80\x06\x6c\x22\xc0\xa8\x01\x02\xc3\x7a\x97\x51\xd7\xa0\x00\x50\xa5\xa5\xb1\xe0\x12\x1c\xa9\xe1\x50\x10\x4e\x75\x59\x74\x00\x00\xed\x13\x22\x91'
        self.data=Dot11DataFrame(self.frame_orig)
        
    def test_01_Type(self):
        'Test Type field'
        self.assertEqual(self.data.get_type(), Dot11.DOT11_TYPE_DATA)
        data=Dot11DataFrame()
        a=data.get_type()
        self.assertEqual(data.get_type(), Dot11.DOT11_TYPE_DATA)

    def test_02_SubType(self):
        'Test SubType field'
        self.assertEqual(self.data.get_subtype(), Dot11.DOT11_SUBTYPE_DATA)
        data=Dot11DataFrame()
        self.assertEqual(data.get_subtype(), Dot11.DOT11_SUBTYPE_DATA)
    
    def test_03_TypeSubtype(self):
        'Test Type and SubType field'
        self.assertEqual(self.data.get_type_n_subtype(), Dot11.DOT11_TYPE_DATA_SUBTYPE_DATA)
        data=Dot11DataFrame()
        self.assertEqual(data.get_type_n_subtype(), Dot11.DOT11_TYPE_DATA_SUBTYPE_DATA)

    def test_04_HeaderSize(self):
        'Test Header Size field'
        self.assertEqual(self.data.get_header_size(), 76)
        
        # Only the Frame control field
        data=Dot11DataFrame()
        self.assertEqual(data.get_header_size(), 2)
    
    def test_05_Duration(self):
        'Test Duration field'
        
        self.assertEqual(self.data.get_duration(), 0x30)
        self.data.set_duration(0x1234)
        self.assertEqual(self.data.get_duration(), 0x1234)
    
    def test_06_Address_1(self):
        'Test Address 1 field'
        
        addr=self.data.get_address1()
        
        self.assertEqual(addr.tolist(), [0x00,0x08,0x54,0xac,0x2f,0x85])
        addr[0]=0x12
        addr[5]=0x34
        self.data.set_address1(addr)
        self.assertEqual(self.data.get_address1().tolist(), [0x12,0x08,0x54,0xac,0x2f,0x34])

    def test_07_Address_2(self):
        'Test Address 2 field'
        
        addr=self.data.get_address2()
        
        self.assertEqual(addr.tolist(), [0x00,0x23,0x4d,0x09,0x86,0xfe])
        addr[0]=0x12
        addr[5]=0x34
        self.data.set_address2(addr)
        self.assertEqual(self.data.get_address2().tolist(), [0x12,0x23,0x4d,0x09,0x86,0x34])

    def test_08_Address_3(self):
        'Test Address 3 field'
        
        addr=self.data.get_address3()
    
        self.assertEqual(addr.tolist(), [0x00,0x08,0x54,0xac,0x2f,0x85])
        addr[0]=0x12
        addr[5]=0x34
        self.data.set_address3(addr)
        self.assertEqual(self.data.get_address3().tolist(), [0x12,0x08,0x54,0xac,0x2f,0x34])
    
    def test_09_sequence_control(self):
        'Test Secuence control field'
        self.assertEqual(self.data.get_sequence_control(), 0x4440)
        self.data.set_sequence_control(0x1234)
        self.assertEqual(self.data.get_sequence_control(), 0x1234)

    def test_10_fragment_number(self):
        'Test Fragment number field'
        self.assertEqual(self.data.get_fragment_number(), 0x0000)
        self.data.set_fragment_number(0xF1) # Es de 4 bit
        self.assertEqual(self.data.get_fragment_number(), 0x01)

    def test_11_secuence_number(self):
        'Test Secuence number field'
        self.assertEqual(self.data.get_secuence_number(), 0x0444)
        self.data.set_secuence_number(0xF234) # Es de 12 bit
        self.assertEqual(self.data.get_secuence_number(), 0x0234)
        
    def test_12_Address_4(self):
        'Test Address 4 field'
        
        # original packet has not addr4
        self.assertEqual(self.data.get_address4(), None)

        # This packet has its
        frame='\x08\x4b\x2c\x00\x00\x11\x3b\x0c\x6d\x67\x00\x11\x3b\x0c\x6f\xc9\x00\x11\x2f\xa0\x49\xe1\x90\xb7\x00\x18\xf3\xd0\xdc\xc7\x2b\xee\x00\x20\x15\x00\x00\x00\x96\xb5\x0c\xff\x81\x62\x06\x51\x60\xf9\xc3\x75\x3b\x6d\x8f\x62\x05\x36\x2e\xcc\xa4\x35\x1c\x68\xf3\xde\x30\x04\x1f\xe3\xab\x2d\x58\xd8\x12\xc5\x22\x2a\x34\xca\x6f\x9a\x2f\x1e\x1d\x63\x26\x1b\xff\x80\x2a\x6d\x02\x76\x8c\xe4\xc7\x45\x07\x10\xae\x2f\x6f\x0e\xb2\x90'
        data=Dot11DataFrame(frame)
        
        addr=data.get_address4()
        
        self.assertEqual(addr.tolist(), [0x00,0x18,0xf3,0xd0,0xdc,0xc7])
        addr[0]=0x12
        addr[5]=0x34
        data.set_address4(addr)
        self.assertEqual(data.get_address4().tolist(), [0x12,0x18,0xf3,0xd0,0xdc,0x34])

    def test_13_frame_data(self):
        'Test Frame Data field'
        # Test with packet without addr4
        frame_body="\xaa\xaa\x03\x00\x00\x00\x08\x00\x45\x00\x00\x28\x72\x37\x40\x00\x80\x06\x6c\x22\xc0\xa8\x01\x02\xc3\x7a\x97\x51\xd7\xa0\x00\x50\xa5\xa5\xb1\xe0\x12\x1c\xa9\xe1\x50\x10\x4e\x75\x59\x74\x00\x00"
        self.assertEqual(self.data.get_frame_body(), frame_body)

        # Test with packet with addr4
        frame='\x08\x4b\x2c\x00\x00\x11\x3b\x0c\x6d\x67\x00\x11\x3b\x0c\x6f\xc9\x00\x11\x2f\xa0\x49\xe1\x90\xb7\x00\x18\xf3\xd0\xdc\xc7\x2b\xee\x00\x20\x15\x00\x00\x00\x96\xb5\x0c\xff\x81\x62\x06\x51\x60\xf9\xc3\x75\x3b\x6d\x8f\x62\x05\x36\x2e\xcc\xa4\x35\x1c\x68\xf3\xde\x30\x04\x1f\xe3\xab\x2d\x58\xd8\x12\xc5\x22\x2a\x34\xca\x6f\x9a\x2f\x1e\x1d\x63\x26\x1b\xff\x80\x2a\x6d\x02\x76\x8c\xe4\xc7\x45\x07\x10\xae\x2f\x6f\x0e\xb2\x90'
        data=Dot11DataFrame(frame)
        frame_body='\x2b\xee\x00\x20\x15\x00\x00\x00\x96\xb5\x0c\xff\x81\x62\x06\x51\x60\xf9\xc3\x75\x3b\x6d\x8f\x62\x05\x36\x2e\xcc\xa4\x35\x1c\x68\xf3\xde\x30\x04\x1f\xe3\xab\x2d\x58\xd8\x12\xc5\x22\x2a\x34\xca\x6f\x9a\x2f\x1e\x1d\x63\x26\x1b\xff\x80\x2a\x6d\x02\x76\x8c\xe4\xc7\x45\x07\x10\xae\x2f'
        self.assertEqual(data.get_frame_body(), frame_body)
        
        # Test with packet with QoS
        frame='\x98\xa6\x2f\xe1\xab\x39\x65\x63\x28\xf1\xc9\x93\x7d\x19\xea\x0a\x04\x60\x02\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1b\x9e\xce\x54\x09\x00\x1b\x9e\xce\x54\x09\xa0\x84\x2c\xd0\x5b\xed\x3c\x05\x00\x00\x64\x00\x01\x04\x00\x06\x73\x70\x65\x65\x64\x79\x01\x04\x82\x84\x8b\x96\x03\x01\x01\x05\x04\x00\x01\x00\x00\x2a\x01\x06\x32\x08\x0c\x12\x18\x24\x30\x48\x60\x6c\x5c\xad\x8e\x78'
        data=Dot11DataFrame(frame)
        frame_body='\xff\xff\xff\xff\x00\x1b\x9e\xce\x54\x09\x00\x1b\x9e\xce\x54\x09\xa0\x84\x2c\xd0\x5b\xed\x3c\x05\x00\x00\x64\x00\x01\x04\x00\x06\x73\x70\x65\x65\x64\x79\x01\x04\x82\x84\x8b\x96\x03\x01\x01\x05\x04\x00\x01\x00\x00\x2a\x01\x06\x32\x08\x0c\x12\x18\x24\x30\x48\x60\x6c'
        self.assertEqual(data.get_frame_body(), frame_body)

    def test_14_FCS(self):
        'Test FCS field'
        
        fcs=self.data.get_fcs()
        self.assertEqual(fcs, 0xed132291)
        self.data.set_fcs(0x44332211)
        self.assertEqual(self.data.get_fcs(), 0x44332211)
        
    def test_15_GetPacket(self):
        'Test FCS with auto_checksum field'
        
        fcs=self.data.get_fcs()
        self.assertEqual(fcs,0xed132291)
        frame=self.data.get_packet()
        self.assertEqual(frame,self.frame_orig)

    def test_16_is_QoS_frame(self):
        'Test QoS frame check'
        
        self.assertEqual(self.data.is_QoS_frame(),False)
        
        frame='\xe8\xba\x60\x56\xce\x5b\xa8\xfe\x14\x3f\xde\x70\x4e\xa3\x40\x0a\x04\x60\x02\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1b\x9e\xce\x54\x09\x00\x1b\x9e\xce\x54\x09\xf0\x4e\xfc\x46\xe2\x49\x52\x00\x00\x00\x64\x00\x01\x04\x00\x06\x73\x70\x65\x65\x64\x79\x01\x04\x82\x84\x8b\x96\x03\x01\x01\x05\x04\x00\x01\x00\x02\x2a\x01\x04\x32\x08\x0c\x12\x18\x24\x30\x48\x60\x6c\x6d\x1a\x84\x17'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_QoS_frame(),True)
        
        frame='\xe8\xde\x62\x77\xcf\x59\xac\xba\x12\x3b\xfc\x76\x48\x92\x44\x0a\x04\xa8\x05\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1d\x0f\xd5\xdd\xd6\x00\x1d\x0f\xd5\xdd\xd6\x40\x17\xbe\xdd\xec\xd2\x01\x00\x00\x00\x64\x00\x31\x04\x00\x0a\x48\x45\x52\x5f\x4d\x41\x44\x52\x49\x44\x01\x08\x82\x84\x8b\x96\x0c\x18\x30\x48\x03\x01\x01\x05\x04\x00\x01\x00\x00\x07\x06\x41\x52\x20\x01\x0d\x14\x2a\x01\x02\x32\x04\x12\x24\x60\x6c\x30\x18\x01\x00\x00\x0f\xac\x02\x02\x00\x00\x0f\xac\x02\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02\x01\x00\xdd\x1a\x00\x50\xf2\x01\x01\x00\x00\x50\xf2\x02\x02\x00\x00\x50\xf2\x02\x00\x50\xf2\x04\x01\x00\x00\x50\xf2\x02\xdd\x09\x00\x03\x7f\x01\x01\x00\x08\xff\x7f\xdd\x1a\x00\x03\x7f\x03\x01\x00\x00\x00\x00\x1d\x0f\xd5\xdd\xd6\x02\x1d\x0f\xd5\xdd\xd6\x64\x00\x2c\x01\x08\x08\xa2\x2c\x97\xc9'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_QoS_frame(),True)

    def test_18_is_no_framebody_frame(self):
        'Test frames without framebody'
        
        self.assertEqual(self.data.is_no_framebody_frame(),False)
        
        frame='\xe8\xba\x60\x56\xce\x5b\xa8\xfe\x14\x3f\xde\x70\x4e\xa3\x40\x0a\x04\x60\x02\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1b\x9e\xce\x54\x09\x00\x1b\x9e\xce\x54\x09\xf0\x4e\xfc\x46\xe2\x49\x52\x00\x00\x00\x64\x00\x01\x04\x00\x06\x73\x70\x65\x65\x64\x79\x01\x04\x82\x84\x8b\x96\x03\x01\x01\x05\x04\x00\x01\x00\x02\x2a\x01\x04\x32\x08\x0c\x12\x18\x24\x30\x48\x60\x6c\x6d\x1a\x84\x17'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_no_framebody_frame(),True)
        
        frame='\xe8\xde\x62\x77\xcf\x59\xac\xba\x12\x3b\xfc\x76\x48\x92\x44\x0a\x04\xa8\x05\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1d\x0f\xd5\xdd\xd6\x00\x1d\x0f\xd5\xdd\xd6\x40\x17\xbe\xdd\xec\xd2\x01\x00\x00\x00\x64\x00\x31\x04\x00\x0a\x48\x45\x52\x5f\x4d\x41\x44\x52\x49\x44\x01\x08\x82\x84\x8b\x96\x0c\x18\x30\x48\x03\x01\x01\x05\x04\x00\x01\x00\x00\x07\x06\x41\x52\x20\x01\x0d\x14\x2a\x01\x02\x32\x04\x12\x24\x60\x6c\x30\x18\x01\x00\x00\x0f\xac\x02\x02\x00\x00\x0f\xac\x02\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02\x01\x00\xdd\x1a\x00\x50\xf2\x01\x01\x00\x00\x50\xf2\x02\x02\x00\x00\x50\xf2\x02\x00\x50\xf2\x04\x01\x00\x00\x50\xf2\x02\xdd\x09\x00\x03\x7f\x01\x01\x00\x08\xff\x7f\xdd\x1a\x00\x03\x7f\x03\x01\x00\x00\x00\x00\x1d\x0f\xd5\xdd\xd6\x02\x1d\x0f\xd5\xdd\xd6\x64\x00\x2c\x01\x08\x08\xa2\x2c\x97\xc9'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_no_framebody_frame(),True)
        
    def test_19_is_cf_poll_frame(self):
        'Test CF_POLL frame type check'
        
        self.assertEqual(self.data.is_cf_poll_frame(),False)
        
        frame='\xe8\xba\x60\x56\xce\x5b\xa8\xfe\x14\x3f\xde\x70\x4e\xa3\x40\x0a\x04\x60\x02\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1b\x9e\xce\x54\x09\x00\x1b\x9e\xce\x54\x09\xf0\x4e\xfc\x46\xe2\x49\x52\x00\x00\x00\x64\x00\x01\x04\x00\x06\x73\x70\x65\x65\x64\x79\x01\x04\x82\x84\x8b\x96\x03\x01\x01\x05\x04\x00\x01\x00\x02\x2a\x01\x04\x32\x08\x0c\x12\x18\x24\x30\x48\x60\x6c\x6d\x1a\x84\x17'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_cf_poll_frame(),True)

        frame='\x3b\x66\x09\xd2\xff\x37\x2f\x6f\x88\xd9\xf1\x29\x61\x1a\x60\x0a\x04\x58\x02\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1b\x9e\xce\x4a\x18\x00\x1b\x9e\xce\x4a\x18\xd0\x02\x2c\x6c\x7d\x4d\x52\x00\x00\x00\x64\x00\x11\x04\x00\x05\x43\x41\x4d\x32\x34\x01\x04\x82\x84\x8b\x96\x03\x01\x01\x05\x04\x00\x01\x00\x00\x2a\x01\x04\x32\x08\x0c\x12\x18\x24\x30\x48\x60\x6c\xf1\xe8\x32\xfd'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_cf_poll_frame(),True)

        frame='\xe8\xde\x62\x77\xcf\x59\xac\xba\x12\x3b\xfc\x76\x48\x92\x44\x0a\x04\xa8\x05\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1d\x0f\xd5\xdd\xd6\x00\x1d\x0f\xd5\xdd\xd6\x40\x17\xbe\xdd\xec\xd2\x01\x00\x00\x00\x64\x00\x31\x04\x00\x0a\x48\x45\x52\x5f\x4d\x41\x44\x52\x49\x44\x01\x08\x82\x84\x8b\x96\x0c\x18\x30\x48\x03\x01\x01\x05\x04\x00\x01\x00\x00\x07\x06\x41\x52\x20\x01\x0d\x14\x2a\x01\x02\x32\x04\x12\x24\x60\x6c\x30\x18\x01\x00\x00\x0f\xac\x02\x02\x00\x00\x0f\xac\x02\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02\x01\x00\xdd\x1a\x00\x50\xf2\x01\x01\x00\x00\x50\xf2\x02\x02\x00\x00\x50\xf2\x02\x00\x50\xf2\x04\x01\x00\x00\x50\xf2\x02\xdd\x09\x00\x03\x7f\x01\x01\x00\x08\xff\x7f\xdd\x1a\x00\x03\x7f\x03\x01\x00\x00\x00\x00\x1d\x0f\xd5\xdd\xd6\x02\x1d\x0f\xd5\xdd\xd6\x64\x00\x2c\x01\x08\x08\xa2\x2c\x97\xc9'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_cf_poll_frame(),True)

    def test_20_is_cf_ack_frame(self):
        'Test CF_ACK frame type check'

        self.assertEqual(self.data.is_cf_ack_frame(),False)

        frame='\x3b\x66\x09\xd2\xff\x37\x2f\x6f\x88\xd9\xf1\x29\x61\x1a\x60\x0a\x04\x58\x02\x0f\x80\x00\x00\x00\xff\xff\xff\xff\xff\xff\x00\x1b\x9e\xce\x4a\x18\x00\x1b\x9e\xce\x4a\x18\xd0\x02\x2c\x6c\x7d\x4d\x52\x00\x00\x00\x64\x00\x11\x04\x00\x05\x43\x41\x4d\x32\x34\x01\x04\x82\x84\x8b\x96\x03\x01\x01\x05\x04\x00\x01\x00\x00\x2a\x01\x04\x32\x08\x0c\x12\x18\x24\x30\x48\x60\x6c\xf1\xe8\x32\xfd'
        data=Dot11DataFrame(frame)
        self.assertEqual(data.is_cf_ack_frame(),True)

    def test_21_AutoChecksum(self):
        'Test auto_checksum feature'
        
        self.data.set_duration(0x1234)
        frame=self.data.get_packet()

        fcs=self.data.get_fcs()
        self.assertEqual(fcs,0xF3F38D63)

        newframe='\x08\x01\x34\x12\x00\x08\x54\xac\x2f\x85\x00\x23\x4d\x09\x86\xfe\x00\x08\x54\xac\x2f\x85\x40\x44\xaa\xaa\x03\x00\x00\x00\x08\x00\x45\x00\x00\x28\x72\x37\x40\x00\x80\x06\x6c\x22\xc0\xa8\x01\x02\xc3\x7a\x97\x51\xd7\xa0\x00\x50\xa5\xa5\xb1\xe0\x12\x1c\xa9\xe1\x50\x10\x4e\x75\x59\x74\x00\x00\xf3\xf3\x8d\x63'
        #original \x08\x01\x30\x00\x00\x08\x54\xac\x2f\x85\x00\x23\x4d\x09\x86\xfe\x00\x08\x54\xac\x2f\x85\x40\x44\xaa\xaa\x03\x00\x00\x00\x08\x00\x45\x00\x00\x28\x72\x37\x40\x00\x80\x06\x6c\x22\xc0\xa8\x01\x02\xc3\x7a\x97\x51\xd7\xa0\x00\x50\xa5\xa5\xb1\xe0\x12\x1c\xa9\xe1\x50\x10\x4e\x75\x59\x74\x00\x00\xed\x13\x22\x91
        self.assertEqual(frame  ,newframe)    
      
suite = unittest.TestLoader().loadTestsFromTestCase(TestDot11DataFrames)
unittest.TextTestRunner(verbosity=2).run(suite)
