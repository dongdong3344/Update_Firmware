import os

bytesSize = 16   #bin文件按照16个字节进行分割
packageSize = 64  #一次发送64个包
chunkSize = bytesSize * packageSize #每次发送的字节组

class Model(object):
    def __init__(self):
        self.fileSize = 0       #文件大小
        self.chunks = []        #字节数组（按照16个字节读取）
        self.packages = []      #发送字节数组(每个数组含有64个16字节的数组)
        self.fileName = ''

    def isFileAviable(self):
        try:
           open(self.fileName)
           return True
        except:
            return False

    def getDataBytes(self):
        self.fileSize = os.path.getsize(self.fileName)
        with open(self.fileName, 'rb') as f:
            while True:
                chunk = f.read(bytesSize)  #每次读取固定长度的字节组
                if not chunk:break
                chunk = chunk + bytes((bytesSize - len(chunk)) * b'\x00')   #不足位数，在后面自动补全'\x00'
                self.chunks.append(chunk)
        return self.chunks

    # 获取文件切割后的CRC校验值
    def generateCRCs(self):
        CRCs = []
        with open(self.fileName,'rb') as f:
            while True:
                chunk = f.read(chunkSize)
                if not chunk: break
                CRCs.append(self.generateChecksum(8,chunk))
                # checksum = self.generateChecksum(chunk)
                # yield checksum
        # print(CRCs)
        return CRCs

    # 将字节数组按照固定长度切割成若干个子数组
    def getPackages(self):
        for i in range(0, len(self.chunks), packageSize):
            self.packages.append(self.chunks[i:i + packageSize])
        # print(self.packages)
        return self.packages


    # 字节累加计算checksum
    def generateChecksum(self,len,bytesData):
        '''
        :param len: checkSum 字节长度
        :param bytesData: 传入的字节
        :return: checksum bytes
        '''
        checkSumStr = '%0{}X'.format(len) % (sum(bytesData)) # 16进制字符串
        checkSumBytes = bytes().fromhex(checkSumStr)[::-1]  #低位在前，高位在后
        # print(checkSumBytes)
        return checkSumBytes



if __name__ == '__main__':
    crc = Model().generateChecksum(8,b'\x7fIAR\x00\x00\x00\x00\x00\x00$\x80\x00\x00\x02\x00')

    print(crc)



