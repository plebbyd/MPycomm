from scripts.ethernet.comm import EthernetComm


if __name__ == '__main__':
    a = EthernetComm('192.168.207.35', 10000)
    a.open()
    #a.sendData('Hello World!', str)
    #a.sendData('DEADBEEF', str)
    a.sendBoundingBox([0.12872, 0.5438, 0.44653, 0.8900212], 0.984142342, 9)
