class Command():
    def __init__(self):
        self.S0F        = 'FE'
        self.DeviceType = '40 05'
        self.OID        = '00'
        self.CMD        = '09'
        self.InAndOut   = '00 00 00 00 00 00'
        self.LEN        = ''
        self.DATA       = None


    def sendUpdateReq(self):
        self.LEN  = '16'
        self.DATA = bytes.fromhex('01 00 01 40 00 00 00 00 00')
        return self.generateData()

    def sendDeleteApp(self):
        self.LEN  = '0E'
        self.DATA = bytes.fromhex('02')
        return self.generateData()


    def sendDataPacket(self,index,dataByte):
        self.LEN  = '21'
        indexByte = index.to_bytes(2,byteorder='little',signed = True)   # 2字节，低位在前
        self.DATA = bytes.fromhex('04') + indexByte + dataByte
        # self.DATA = '04 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF'  # 04，00 00是number, 如第2包是01 00，低位在前面，后面16个字节是data
        return self.generateData()

    def resendDataPack(self,index,dataByte):
        self.LEN  = '21'
        indexByte = index.to_bytes(2,byteorder='little',signed = True)  # 2字节，低位在前
        self.DATA = bytes.fromhex('06') + indexByte + dataByte
        return self.generateData()

    # 64×16字节后发送，返回64bit,10101……格式
    def sendDataSectorCheck(self):
        self.LEN  = '14'
        self.DATA = bytes.fromhex('05 00 00 00 00 00 00')
        return self.generateData()


    def resendDataCheck(self):
        self.LEN  = '14'
        self.DATA = bytes.fromhex('07 00 00 00 00 00 00')
        return self.generateData()


    def sendWholeFirmwareCS(self):
        self.LEN  = '0E'
        self.DATA = bytes.fromhex('08')
        return self.generateData()

    def sendRestartApp(self):
        self.LEN  = '0E'
        self.DATA = bytes.fromhex('09')
        return self.generateData()


    def generateData(self):
        # 计算checksum值时去掉第一个字节'FE'
        dataStr =  self.DeviceType + self.OID + self.CMD + self.InAndOut + self.LEN
        byte = bytes.fromhex(dataStr) + self.DATA
        checkSumStr = '%04X' % (sum(byte))  # 16进制字符串
        checkSumBytes = bytes().fromhex(checkSumStr)[::-1]  #b'\x00\xa6'——> b'\xa6\x00'
        dataByte = bytes.fromhex(self.S0F + dataStr)+ self.DATA + checkSumBytes
        return dataByte


if __name__ == '__main__':
    pass
    # Command().sendUpdateReq()
    # Command().sendDeleteApp()
    # Command().sendDataPacket(1,bytes.fromhex('FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF' ))
    # Command().sendDataSectorCheck()
    # Command().sendWholeFirmwareCS()
    # Command().sendRestartApp()











