import time
import math

class Touch:
    def __init__(self, memory_service):
        self.memory_service = memory_service
        self.sensors = {'Head_mid': 'Device/SubDeviceList/Head/Touch/Middle/Sensor/Value' ,
                        'LHand':      'Device/SubDeviceList/LHand/Touch/Back/Sensor/Value' ,
                        'RHand':      'Device/SubDeviceList/RHand/Touch/Back/Sensor/Value' }

    def print_name_sensor(self):
        for k in self.sensors.keys():
            print(k)
        
    def set(self, sensor, touch_time =1):
        try:
            sensor_key = self.sensors[sensor]
            print("Touching %s ..." %sensor)
            self.memory_service.insertData(sensor_key,1.0)
            time.sleep(touch_time)
            self.memory_service.insertData(sensor_key,0.0)
            print("Touching %s ... done" %sensor)
            return True
        except:
            print("ERROR: Sensor %s unknown" %sensor)
            return False

    def print_sensors(self):
        print(touch_service.getSensorList()) # vector of sensor names
        print(touch_service.getStatus())

class Sonar:
    def __init__(self, memory_service, sensor= "SonarFront", duration = 1.0):
        self.memory_service = memory_service
        self.sensor = sensor
        self.duration = duration
        self.sonarValueList = ['Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value',
                               'Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value' ]

        self.sonarValues = None

        self.robot_position = (0,0) # tuple (x:int, y:int)
        self.human_position = (0,5) 
        # self.humans_positions = self.get_positions()
        
    def setSonarFrontal(self, points = None):

        # compute distances from points if None last human pos saved
        distances = self._computeDistances(points)

        # set sensor value
        mkey = self.sonarValueList[0]
        for dist in distances: 
            self.memory_service.insertData(mkey,dist)
        time.sleep(self.duration)
        self.sonarValues =  self.memory_service.getListData(self.sonarValueList)

    def setSonarRear(self, points = None):

        # compute distances from points if None last human pos saved
        distances = self._computeDistances(points)

        # set sensor value      
        mkey = self.sonarValueList[1]
        for dist in distances: 
            self.memory_service.insertData(mkey,dist)
        time.sleep(self.duration)
        self.sonarValues =  self.memory_service.getListData(self.sonarValueList)

    def setPosRobot(self, pos):
        if type(pos) is not tuple:
            return
        self.robot_position = pos

    def setPosHuman(self, pos):          # for simplicity we handle the whole interaction with only one human
        if type(pos) is not tuple:
            return
        self.human_position = pos

    def _computeDistances(self, points = None, robot_position = None):   # points % robot_position 2D vectors in tuples (x,y)

        if robot_position is None: robot_position = self.robot_position
        if points is None:
            pos = self.human_position
            distance = [float(math.sqrt((robot_position[0]-pos[0])**2 + (robot_position[1]-pos[1])**2))]
            return distance

        else:
            distances = []
            for pos in points:
                distance = float(math.sqrt((robot_position[0]-pos[0])**2 + (robot_position[1]-pos[1])**2))
                distances.append(distance)
            return distances


    # turn values from sonar (frotal and rear)
    def get_values(self):
        sonarValues =  self.memory_service.getListData(self.sonarValueList)
        print(sonarValues)

    #we use only the frontal sonar, so it will discover only humans in front of him

class Animations:
    def __init__():
        pass

class Motion:
    def __init__(self, motion_service):
        self.motion_service = motion_service
        self.speed = 0.2        # [m/s] normal cruise speed
        self.max_speed = 0.5    # [m/s] maximum speed provided from pepper


    # method to perform a motion for a certain time.
    def setSpeed(self, lin_vel, ang_vel, motion_time):

        if lin_vel > self.speed: lin_vel = self.speed   # clamp value

        self.motion_service.move(lin_vel, ang_vel, ang_vel)
        time.sleep(motion_time)
        self.motion_service.stopMove()
        return 


    def forward(self, distance, lin_vel=0.2, ang_vel=0):
        if lin_vel > self.speed: lin_vel = self.speed   # clamp value

        self.setSpeed(lin_vel, ang_vel, abs((distance-0.5)/lin_vel))

      # Robot motion

    # def stop(self):
    #     print 'stop'
    #     self.motion_service.stopMove()
    #     if self.beh_service!=None:
    #         bns = self.beh_service.getRunningBehaviors()
    #         for b in bns:
    #             self.beh_service.stopBehavior(b)

    # def forward(self):
    #     x = self.speed
    #     y = 0.0
    #     theta = 0.0
    #     self.motion_service.moveTo(x, y, theta) #blocking function

    # def backward(self, r=1):
    #     if self.stop_request:
    #         return
    #     print 'backward',r
    #     x = -r
    #     y = 0.0
    #     theta = 0.0
    #     self.motion_service.moveTo(x, y, theta) #blocking function

    # def left(self, r=1):
    #     if self.stop_request:
    #         return
    #     print 'left',r
    #     #Turn 90deg to the left
    #     x = 0.0
    #     y = 0.0
    #     theta = math.pi/2 * r
    #     self.motion_service.moveTo(x, y, theta) #blocking function

    # def right(self, r=1):
    #     if self.stop_request:
    #         return
    #     print 'right',r
    #     #Turn 90deg to the right
    #     x = 0.0
    #     y = 0.0
    #     theta = -math.pi/2 * r
    #     self.motion_service.moveTo(x, y, theta) #blocking function

    # def turn(self, r):
    #     if self.stop_request:
    #         return
    #     print 'turn',r
    #     #Turn r deg
    #     vx = 0.0
    #     vy = 0.0
    #     vth = r * math.pi / 180 
    #     self.motion_service.moveTo(vx, vy, vth) #blocking function

    # def setSpeed(self,vx,vy,vth,tm,stopOnEnd=False):
    #     if self.stop_request:
    #         return
    #     self.motion_service.move(vx, vy, vth)
    #     time.sleep(tm)
    #     if stopOnEnd:
    #         self.motion_service.move(0, 0, 0)
    #         self.motion_service.stopMove()



    # def detect_person(self, sonar):
    #     for i in range(len(sonar.sonarValues)):
    #         if sonar.sonarValues[i] <= 0.75:
    #             if i==0:
    #                 print("Person detected with sonar SonarFront")
    #             else:
    #                 print("Person detected with sonar SonarBack")
    #             return True
    #     return False


    # def selectMinDistance(self, distances):
    #     min_distance = float("inf")
    #     index = 0

    #     for i in range(len(distances)):
    #         if distances[i] < min_distance:
    #             min_distance = distances[i]
    #             index = i

    #     return min_distance, index
