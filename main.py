from scripts.ethernet.comm import EthernetComm
from scripts.image_processor.inferencer import Processor

if __name__ == '__main__':
    a = EthernetComm('192.168.207.140', 10000)
    a.open()
    #a.sendData('Hello World!', str)
    #a.sendData('DEADBEEF', str)
    #a.sendBoundingBox([0.12872, 0.5438, 0.44653, 0.8900212], 0.984142342, 9)

    a.openCommStream()
    im = Processor()
    im.openStream()
    im.setDimensions(360, 480)
    im.show_frames = True
    im.loadTensorflowData()
    i = 0

    while(i < 10):
        if im.inference_results:
            a.output_array = im.inference_results
            print(a.output_array)
            im.inference_results.clear()
            i +=1
