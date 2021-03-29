import os
import numpy as np
import matplotlib as mp
from scipy.interpolate import interp1d
import random
import math




class ArcGen():


    def __init__(self):
        self.output_text = ''
        self.segmentQueue = []
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.coordinateQueue = []


    def createArc(self, x_start, y_start, z_start, i, j, k, arc_angle, cw = True, threeD = False):
        #Check directionality to get first command string to parse into main line output
        if cw:
            g_command = 'G02'
        else:
            g_command = 'G03'

        x_offset = 0
        y_offset = 0
        #parse information together
        if threeD:
            radius = math.sqrt(i**2 + j**2 + k**2)
            g_code_string = g_command + ' X' + '{:.4f}'.format(x_start + i + i) + ' Y' + '{:.4f}'.format(y_start + j + j) + ' Z' + '{:.4f}'.format(z_start + k + k) + ' I' + '{:.4f}'.format(i) + ' J' + '{:.4f}'.format(j) + ' K' + '{:.4f}'.format(k)
        else:
            radius = math.sqrt(i**2 + j**2)
            #x_rel is x position relative to arcs centerpoint
            if i != 0 :
                theta = (180 / math.pi) * math.atan(j/i)
                if i<0 and j<0:
                    theta = (180 / math.pi) * math.atan(j/i)
                elif i >0 and j < 0:
                    theta = (180 / math.pi) * math.atan(j/i) + 180
                elif i > 0 and j > 0:
                    theta = (180 / math.pi) * math.atan(j/i) + 180
                elif i < 0 and j > 0:
                    theta = (180 / math.pi) * math.atan(j/i) + 360
            else:
                theta = 0

            lookup_angle = theta - arc_angle if cw else (theta + arc_angle)%360
            pure_angle = lookup_angle


            if cw:
                x_offset = radius * math.cos(lookup_angle * math.pi / 180)
                y_offset = radius * math.sin(lookup_angle * math.pi / 180)
            else:
                x_offset = radius * math.cos(lookup_angle * math.pi / 180)
                y_offset = radius * math.sin(lookup_angle * math.pi / 180)

            g_code_string = g_command + ' X' + '{:.4f}'.format(x_start + i + x_offset) + ' Y' + '{:.4f}'.format(y_start + j + y_offset) + ' I' + '{:.4f}'.format(i) + ' J' + '{:.4f}'.format(j)
        #Update x,y,z values. Hold current location for continuous motion generation
        self.x = x_start + i + x_offset
        self.y = y_start + j + y_offset
        self.z = z_start + k
        self.coordinateQueue.append([self.x, self.y, self.z])


        return g_code_string


    def createLineSegment(self,x_end, y_end, z_end):
        g_code_string = 'G1' + ' X' + '{:.4f}'.format(x_end) + ' Y' + '{:.4f}'.format(y_end) + ' Z' + '{:.4f}'.format(z_end)

        #Update x,y,z values. Hold current location for continuous motion generation
        self.x = x_end
        self.y = y_end
        self.z = z_end

        return g_code_string



    def boomerang(self, segments, size):

        for seg in range(1,segments + 1):

            if seg >= segments/2:
                size_multiplier =   (seg/(segments/2))
                mult = -1
                cw = False
            else:
                size_multiplier = ((segments/2) / seg)
                mult = 1
                cw = False
            if cw:
                i = mult * size * size_multiplier / 100
                j =  size * size_multiplier
                k = 0
            else:
                i = mult * size * size_multiplier / 100
                j =  mult * size * size_multiplier
                k = 0

            angle = 5
            threeD = False
            self.addToQueue('N' + str(len(self.segmentQueue)) + ' ' + self.createArc(self.x, self.y, self.z, i, j , k, angle, cw, threeD))


        return True

    def boomerangLines(self, segments, cw, sharpness):
        slopeQueue = []
        lengthQueue = []
        for i in range(int(segments/2)):
            slope =  -5 * (1 - (i/int(segments/2)))**sharpness
            length = (1.000 - (i/(segments/2)))**sharpness

            slopeQueue.append(slope)
            lengthQueue.append(length)



            self.segmentQueue.append('N' + str(len(self.segmentQueue)) + ' ' + self.createLineSegment(self.x - slope * length, self.y + (1/slope) * length, self.z))

        for i in range(int(segments/2)):
            #slope = 5 * (1 - (i - (segments/2)/(segments)))**sharpness
            #length = (1.000 - (i - (segments/2)/(segments)))**sharpness
            slope = -slopeQueue[-i]
            length = lengthQueue[-i]

            if i > 0:
                self.segmentQueue.append('N' +str(len(self.segmentQueue)) + ' ' + self.createLineSegment(self.x - slope * length, self.y - (1/slope) * length, self.z))







    def boomerang2(self):

        segments = 550 #more segments makes a deeper boomerang.
        cw= True #only tested for clockwise 2/16/2021 3:31 PM
        prev_angle = 0

        pivot_xyz = self.coordinateQueue[-1]
        for segment in range(int((segments/4)) + 1,  int((segments/4)) + int(segments/4) + 2):
            if cw:
                angle = 1
                i = -30   #(segments) / (1000 * (segment/(segments/4 + 1)))
                j = -1 * segments*(1 - segment/((segments/2) + 2)) #(1 - segment/(segments/4)) * -1 * segments / ((segment/(segments/4 + 1)))
                k = 0
                threeD = False

                self.segmentQueue.append(self.createArc(self.x, self.y, self.z, i, j , k, angle, cw, threeD))
            else:

                return True

        pivot_xyz = self.coordinateQueue[-1]
        for segment in range(int((segments/2)) + 2,  int((segments)) + 3):
            if cw:
                angle = 1
                i = -30   #(segments) / (1000 * (segment/(segments/4 + 1)))
                j = (segments/2 + 1) * (segment - (segments/2 + 2))/(segments/2 + 1) #(1 - segment/(segments/4)) * -1 * segments / ((segment/(segments/4 + 1)))
                k = 0
                threeD = False

                self.segmentQueue.append(self.createArc(self.x, self.y, self.z, i, j , k, angle, cw, threeD))
            else:

                return True




        return True


    def addToQueue(self, string):
        try:
            self.segmentQueue.append(string)

        except:
            print('AddToQueueError')
            return False

        return True


    def generateRandomArc(self, x_start, y_start, z_start, min, max, threeD = False):
        #outputs random i, j, k values between the min and max in the form [i, j, k]
        try:
            inter = interp1d([0, 1], [min, max])
            inter_angle = interp1d([0, 1], [0, 360])
            arc_angle = inter_angle(random.random())[()]
            if threeD:
                ijk_vector = [inter(random.random())[()] for i in range(1,4)]
                output = self.createArc(x_start, y_start, z_start, ijk_vector[0], ijk_vector[1], ijk_vector[2], arc_angle, random.random() > 0.5, threeD)

            else:
                ijk_vector = [inter(random.random())[()] for i in range(1,3)]
                output = self.createArc(x_start, y_start, z_start, ijk_vector[0], ijk_vector[1], z_start, arc_angle, random.random() > 0.5, threeD)


        except Exception as e:
            print(e)

            print('GenerateRandomNumberError')
            return False


        return output


    def generateRandomLine(self, x_start, y_start, z_start, min, max, threeD = False):

        try:
            inter = interp1d([0, 1], [min, max])
            if threeD:
                delta_vector = [inter(random.random())[()] for i in range(1,4)]
                output = self.createLineSegment(x_start + delta_vector[0], y_start + delta_vector[1], z_start + delta_vector[2])
            else:
                delta_vector = [inter(random.random())[()] for i in range(1,3)]
                output = self.createLineSegment(x_start + delta_vector[0], y_start + delta_vector[1], z_start)

        except:

            print("GenerateRandomLineError")
            return False

        return output


    def generateContinuous(self, numSegments, min, max, threeD = False):
        #First step is to clear the segment queue to make sure we have a clean slate
        #generate random segments for the specified amount of segments
        for i in range(numSegments):
            dice = random.random()
            if dice < 0.5:
                self.segmentQueue.append(self.generateRandomLine(self.x, self.y, self.z, min, max, threeD))
            else:
                self.segmentQueue.append(self.generateRandomArc(self.x, self.y, self.z, min, max, threeD))



    def generateMultipleLinesRandom(self, numSegments, min, max, threeD = False):
        for i in range(numSegments):
            self.segmentQueue.append(self.generateRandomLine(self.x, self.y, self.z, min, max, threeD))



    def writeFile(self, output, clearQueue = False):

        with open(output + '.txt', 'w') as output_file:
            for line in self.segmentQueue:
                output_file.write(line + '\n')

        if clearQueue:
            self.clearSegmentQueue()

        return True


    def clearSegmentQueue(self):

        self.segmentQueue = []

        return True

    def addNCode(self, file):
        with open(file, 'r') as f:
            data = f.readlines()


        for i in range(len(data)):
            data[i] = 'N{} '.format(i) + data[i]

        with open('new-{}'.format(file), 'w') as o:
            o.writelines(data)


        return True

    def createPolygon(self, N, length):
        interior_angle = (N - 2) * 180 / N
        current_angle = 0 #Start at 0 degrees on the unit circle. (East is 0)
        diviser = (N - 2)/2
        for i in range(N):
            x_end = self.x + length * math.cos((interior_angle - current_angle) * math.pi / 180)
            y_end = self.y + length * math.sin((interior_angle - current_angle) * math.pi / 180)
            current_angle = current_angle - (1/diviser) * interior_angle
            self.segmentQueue.append(self.createLineSegment(x_end, y_end, 0))



'''
if __name__ == '__main__':

    a = ArcGen()

    a.segmentQueue.append('G0 X0 Y0')
    a.coordinateQueue.append([0, 0, 0])
    a.addToQueue(a.createArc(a.x, a.y, a.z, -100, 300, 0, 120))
    a.addToQueue(a.createArc(a.x, a.y, a.z, 400, -800, 0, 300, False))
    a.addToQueue(a.createArc(a.x, a.y, a.z, 100, 300, 0, 270))
    a.writeFile('bigArc')
'''


'''
if __name__ == '__main__':

    a = ArcGen()
    a.segmentQueue.append('G0 X0 Y0')
    a.coordinateQueue.append([0, 0, 0])
    a.createPolygon(15, 100)
    a.createPolygon(15, 50)
    a.createPolygon(15, 20)
    a.createPolygon(15, 10)
    a.createPolygon(15, 5)
    a.createPolygon(15, 1)
    a.segmentQueue.append(a.createLineSegment(350, 0, 0))
    a.createPolygon(8, 100)
    a.createPolygon(8, 50)
    a.createPolygon(8, 20)
    a.createPolygon(8, 10)
    a.createPolygon(8, 5)
    a.createPolygon(8, 1)
    a.segmentQueue.append(a.createLineSegment(550, 0, 0))
    a.createPolygon(5, 100)
    a.createPolygon(5, 50)
    a.createPolygon(5, 20)
    a.createPolygon(5, 10)
    a.createPolygon(5, 5)
    a.createPolygon(5, 1)
    a.segmentQueue.append(a.createLineSegment(700, 0, 0))
    a.createPolygon(4, 100)
    a.createPolygon(4, 50)
    a.createPolygon(4, 20)
    a.createPolygon(4, 10)
    a.createPolygon(4, 5)
    a.createPolygon(4, 1)
    a.segmentQueue.append(a.createLineSegment(800, 0, 0))
    a.createPolygon(3, 100)
    a.createPolygon(3, 50)
    a.createPolygon(3, 20)
    a.createPolygon(3, 10)
    a.createPolygon(3, 5)
    a.createPolygon(3, 1)
    a.writeFile('polycreate')
'''
