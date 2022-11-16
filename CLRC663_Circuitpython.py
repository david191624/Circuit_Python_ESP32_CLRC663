import board
import busio
import binascii
import time


CLRC663_Threshold = [0x37, 0x3C]        # Receiver Threshold value
CLRC663_T1_Control = [0x14, 0x92]       # Control register of the Timer1.
CLRC663_T2_Control = [0x19, 0x20]       # Control register of the Timer2.
CLRC663_CLean_FIFO = [0x20 ,0xB0]


class CLRC663():
    def __init__(self):
        self.initvalue1 = "0F98149219201A031BFF1E00029003FE0C80288829002A012B0534003812"
        #self.initvalue1 ="55550000000000000000000000000000FF03FDD414011700"

        self.initvalue2 = "000002B0067F077F0508050808100940"
        self.load_protocol = ["000D"]  # Load Protocol
        self.reset_interupt = "08000900"  # Reset Interupt
        self.clena_FFifo = "20B0"
        self.FelicaSetting = "2C092D092E082F003003310033013505373C3900368631C0320010191100150016002904288F0B00"
        self.FieldOn = "288F"
        self.FlushFIFO = "10A3114D15001600000002B0067F077F"  # Flush FIFO
        self.Read_FIFO_Length = "84"
        self.Read_FIFO_Data = "85"
    def devinit(self):
        initvalue1 = "0F98149219201A031BFF1E00029003FE0C80288829002A012B0534003812"
        initvalue2 = "000002B0067F077F0508050808100940"
        load_protocol="000D"       # Load Protocol
        reset_interupt="08000900"   # Reset Interupt
        clena_FFifo = "20B0"
        FelicaSetting="2C092D092E082F003003310033013505373C3900368631C0320010191100150016002904288F0B00"
        FieldOn="288F"
        Uart_663_write(initvalue1)
        Uart_663_write(initvalue2)
        #print("Load Felica Protocol")
        Uart_663_write(load_protocol)
        print("Field on")
        Uart_663_write(FieldOn)

        time.sleep(0.001)
        return ""
    def FelicaSetting_Reset(self):
        Felica_Setting="288F2C092D092E082F003003318032123301340035053610373C381239034A054B014C054DB24E4D10191100150016002904288F58185AB25B4D5CF05D195E205FF00B00"
        HB_Setting="3B1C"
        Uart_663_write(Felica_Setting)
        #Uart_663_write(HB_Setting)
        time.sleep(0.01)
    def HB(self):
        HB_Setting="3B1C"
        Uart_663_write(HB_Setting)
        time.sleep(0.01)
    
    
    def RequestC(self):
        #FlushFIFO = "10A3114D15001600000002B0067F077F"  #Flush FIFO
        WriteRequectC_IntoFIFO = "0506050005FF05FF050005000007"  #081809428708000900
        Uart_663_write(self.FlushFIFO)
        Uart_663_write(WriteRequectC_IntoFIFO)

    def ReadFIFO(self):

        #length_of_FIFO = Uart_663_write(self.Read_FIFO_Length)
        #print("Length of FIFO",self.length_of_FIFO)
        #Value_of_FIFO = Uart_663_write(int.from_bytes(length_of_FIFO,"big")*"85")
        Value_of_FIFO = Uart_663_write(40*"85")
        print("IDM is equal to :")
        if Value_of_FIFO != None:
            for i in Value_of_FIFO:
                print(hex(i))



def Uart_663_write(Data):
    tempe_bytearray = bytearray()
    byte_array = bytearray()
   #print("Leng of the message", len(Data))
    for i in range(int((len((Data))) / 2)):

        if i == 0:

            tempString = Data[0] + Data[1]
           # print(tempString)
            #print(type(tempString))
            #byte_array = byte_array.fromhex(tempString)
            #print("testa")
            #print(int(tempString,16).to_bytes(1,'big'))
            #print(type(int(tempString,16).to_bytes(1,'big')))
            #print("testb")
            #print(type(int(tempString,16)))
            byte_array = byte_array.append(int(tempString,16))
            #print(int(tempString,16))
            #print(byte_array)
            #tempe_bytearray.append(int(byte_array[0]))
            tempe_bytearray.append(int(tempString,16))
            #print("done")
        else:
            # print( int(str(reset_interupt[i*2] + reset_interupt[(i*2)+1]),16))
            tempString = Data[i * 2] + Data[(i * 2) + 1]
            #byte_array = byte_array.fromhex(tempString)
            #print("ByteArray Content", byte_array)
            tempe_bytearray.append(int(tempString,16))
    ## print(tempString)
    #print(tempe_bytearray)

      # open serial port
    #print(ser.name)  # check which port was really used
    #ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.0001 )
    ser = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0.01)
    print("uart")
    print(tempe_bytearray)
    ser.write(tempe_bytearray)
    
    #print(tempe_bytearray)
    x = ser.read(50)
    #print("received",len(x))
    print(x)  # write a string
    ser.deinit()
    return (x)

def Uart_663_write_HB(Data):
    tempe_bytearray = bytearray()
    byte_array = bytearray()
   #print("Leng of the message", len(Data))
    for i in range(int((len((Data))) / 2)):

        if i == 0:

            tempString = Data[0] + Data[1]

            byte_array = byte_array.fromhex(tempString)
            tempe_bytearray.append(byte_array[0])
        else:
            # print( int(str(reset_interupt[i*2] + reset_interupt[(i*2)+1]),16))
            tempString = Data[i * 2] + Data[(i * 2) + 1]
            byte_array = byte_array.fromhex(tempString)
            #print("ByteArray Content", byte_array)
            tempe_bytearray.append(byte_array[0])
    ## print(tempString)
    #print(tempe_bytearray)

     # open serial port
    #print(ser.name)  # check which port was really used
    return(tempe_bytearray)
    #print(tempe_bytearray)
    #x = ser.read(50)
    #print("received",len(x))
    #print(x)  # write a string
    #ser.close()
    #return (x)
#ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.0001 )
CLRC663_Poll=CLRC663()
CLRC663_Poll.devinit()
CLRC663_Poll.FelicaSetting_Reset()
#CLRC663_Poll.HB()
CLRC663_Poll.RequestC()
time.sleep(0.04)
CLRC663_Poll.ReadFIFO()
#ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.012 )

#WriteoclRequectC_IntoFIFO = "067F077F0506050005FF05FF050005000007"  # 081809428708000900

#nfcdata2=Uart_663_write_HB("000002B0067F077F0506050005FF05FF050005000007")
#ser.write(nfcdata2)
#y=ser.read(50)
#print(y)
#nfcdata3=Uart_663_write_HB("8485858585858585858585858585858585858585858585858585858585858585")
#time.sleep(0.135)
#ser.write(nfcdata3)
#x=ser.read(50)
#print("recevied")
#print(x)


#nfcdata1= Uart_663_write_HB("10A3114D15001600000002B0067F077F")
#ser.write(nfcdata1)