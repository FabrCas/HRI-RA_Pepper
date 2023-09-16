import time
import math

class Touch:
    def __init__(self, memory_service):
        self.memory_service = memory_service
        self.sensors = {'Head': 'Device/SubDeviceList/Head/Touch/Middle/Sensor/Value' , 
                        'LHand':      'Device/SubDeviceList/LHand/Touch/Back/Sensor/Value' ,
                        'RHand':      'Device/SubDeviceList/RHand/Touch/Back/Sensor/Value' }
        # left and right hands, head middle sensors

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
    def __init__(self, motion_service, posture_service):
        self.motion     = motion_service
        self.posture    = posture_service
        self.open_hand  = True   # boolean flag to indicate if the hand has to remain close
        self.continue_dance = False

        # set posture standard init and save angles
        self.stand_init()
        self.angles_start = self._get_angles()


    def _get_angles(self):
        joint_angle = {}
        use_sensor = False
        joint_angle['HeadYaw']          = self.motion.getAngles("HeadYaw", use_sensor)
        joint_angle['HeadPitch']        = self.motion.getAngles("HeadPitch", use_sensor)
        joint_angle['HipRoll']          = self.motion.getAngles("HipRoll", use_sensor)
        joint_angle['HipPitch']         = self.motion.getAngles("HipPitch", use_sensor)
        joint_angle['KneePitch']        = self.motion.getAngles("KneePitch", use_sensor)
        joint_angle['LShoulderPitch']   = self.motion.getAngles("LShoulderPitch", use_sensor)
        joint_angle['LShoulderRoll']    = self.motion.getAngles("LShoulderRoll", use_sensor)
        joint_angle['LElbowYaw']        = self.motion.getAngles("LElbowYaw", use_sensor)
        joint_angle['LElbowRoll']       = self.motion.getAngles("LElbowRoll", use_sensor)
        joint_angle['LWristYaw']        = self.motion.getAngles("LWristYaw", use_sensor)
        joint_angle['RShoulderPitch']   = self.motion.getAngles("RShoulderPitch", use_sensor)
        joint_angle['RShoulderRoll']    = self.motion.getAngles("RShoulderRoll", use_sensor)
        joint_angle['RElbowYaw']        = self.motion.getAngles("RElbowYaw", use_sensor)
        joint_angle['RElbowRoll']       = self.motion.getAngles("RElbowRoll", use_sensor)
        joint_angle['RWristYaw']        = self.motion.getAngles("RWristYaw", use_sensor)



        return joint_angle

    def print_angles_start(self):
        print(self.angles_start)


    def stopDance(self):
        self.continue_dance = False

    # --------------------- default animations from posture service

    def stand(self, speed = 1):   # time: 5 [s]
        jointNames = ["HeadYaw", "HeadPitch"]
        angles = [0, 0]
        times  = [5.0, 5.0]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)
        self.posture.goToPosture("Stand",speed)

    def crouch(self, speed = 1):  # time: 2 [s]
        self.posture.goToPosture("Crouch",0.7)
        return

    def stand_zero(self, speed = 1):
        self.posture.goToPosture("StandZero",speed)
        return

    def stand_init(self,speed = 1):
        self.posture.goToPosture("StandInit", speed)
        return

    def wakeUp(self):
        self.motion.wakeUp()
        return

    def rest(self):
        self.motion.rest()
        return


    # --------------------- custom animations
    def default(self):    # time: 2 [s]

        if self.open_hand:
            self.stand_init()
        else: # custom default with closed hand
            jointNames = [k for k,v in self.angles_start.items()]
            angles = [v for k,v in self.angles_start.items()]
            times  = [2]*len(self.angles_start)
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # # close hand
        # if not self.open_hand:
        #     names  = ["RHand"]
        #     angles  = [0]
        #     fractionMaxSpeed  = 0.2
        #     self.motion.setAngles(names, angles, fractionMaxSpeed)


    def greet(self):  # time: 6 [s] + default = 8 [s]

        # move arm  
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch"]
        angles = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07]
        times  = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # move hand
        for i in range(2):
            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1.8, -0.07, -0.07]
            times  = [1,1,1]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1, -0.07, -0.07]
            times  = [1,1,1]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # move back to init stand
        self.default() 
        return
    
    def yes(self):    # time: 3 [s]
        for i in range(2):
            jointNames = ["HeadPitch"]
            angles = [-0.3]
            times  = [0.5]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["HeadPitch"]
            angles = [0.1]
            times  = [0.5]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        jointNames = ["HeadPitch"]
        angles = [self.angles_start['HeadPitch'][0]]
        times  = [1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)
        return 

    def no(self):  # time: 2 [s]
        jointNames = ["HeadYaw"]
        angles = [-0.5]
        times  = [0.5]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        jointNames = ["HeadYaw"]
        angles = [0.5]
        times  = [1.0]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        jointNames = ["HeadYaw"]
        angles = [self.angles_start['HeadYaw'][0]]
        times  = [0.5]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)
        return 

    # --------------------- custom animations (actions)

    def search(self):  # time: 3 [s]
        for i in range(1):
            jointNames = ["HeadYaw", "HeadPitch"]
            angles = [0.5, 0.3]
            times  = [1,1]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["HeadYaw", "HeadPitch"]
            angles = [-0.5, 0.3]
            times  = [1,1]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # jointNames = ["HeadYaw", "HeadPitch"]
        # angles = [0, 0]
        # times  = [1.5, 1.5]
        # isAbsolute = True
        # self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        jointNames = ["HeadYaw", "HeadPitch"]     
        angles = [self.angles_start['HeadYaw'][0], 0.3]    # 0.3 same pitch used even for grab and place and object
        times  = [1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)
        return

    def grab(self): # time: 5 [s] + default = 7 [s]

        # look 
        jointNames = ["HeadPitch"]
        angles = [0.3]
        times  = [1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # inflect body
        jointNames = ["KneePitch", "HipPitch"]
        angles = [-0.3, -1]
        times  = [1, 1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # move shoulder, elbow and twist while to take central object, while opening hand

        jointNames = ["RShoulderPitch","RShoulderRoll", "RElbowRoll", "RElbowYaw","RHand","RWristYaw"]   
        angles = [1, -0.2,  1, 0.9, 1, 0.6]  #0.8
        times  = [1,1, 2, 2, 2, 2]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # close hand
        jointNames = ["RHand"]   
        angles = [0]
        times  = [1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        self.open_hand = False
        self.default()
        return 


    def place(self):   # time: 5 [s] + default = 7 [s]

        # names  = ["RHand"]
        # angles  = [0]
        # fractionMaxSpeed  = 0.2
        # self.motion.setAngles(names, angles, fractionMaxSpeed)
        
        # look  
        jointNames = ["HeadPitch"]
        angles = [0.3]
        times  = [1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # inflect body
        jointNames = ["KneePitch", "HipPitch"]
        angles = [-0.3, -1]
        times  = [1, 1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # move shoulder, elbow and twist while to take central object, while opening hand
        jointNames = ["RShoulderPitch","RShoulderRoll", "RElbowRoll", "RElbowYaw","RWristYaw"]   
        angles = [0.8, -0.2,  1, 0.7, -0.8]  #0.8
        times  = [1,1, 2, 2, 2]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # open hand
        jointNames = ["RHand"]   
        angles = [1]
        times  = [1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        self.open_hand = True
        self.default()
        return
        


    def interactDoor(self, time_wheel_motion = 4):  # time: 6 + 4 + 3 = 13 [s] + 1(default) = 14[s]

        jointNames = ["HeadYaw", "HeadPitch"]
        angles = [-0.2, 0.2]
        times  = [1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # safety move to avoid collision with handle
        jointNames = ["RShoulderRoll", "RHand", "RShoulderPitch"]   
        angles = [-1,1,0.2]  #0.8
        times  = [1,1,2]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # to handle
        jointNames = ["RShoulderPitch","RShoulderRoll", "RElbowRoll", "RElbowYaw","RWristYaw"]   
        angles = [0.3, -0.2,  0.2, 0.8, -0.8]  #0.8
        times  = [1,1, 1, 1, 1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # close hand
        jointNames = ["RHand"]   
        angles = [0]
        times  = [1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # rotate wrist and elbow
        jointNames = ["RWristYaw", "RElbowYaw", "RShoulderPitch", "RShoulderRoll"]   
        angles = [1.2, 0, 0.25, -0.15]
        times  = [1,1,1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # wait virtual motion
        time.sleep(time_wheel_motion)


        # rotate wrist back and open hand, rest position of the handle 
        jointNames = ["RWristYaw", "RElbowYaw", "RShoulderPitch", "RShoulderRoll","RHand"]   
        angles = [-0.8, 0.8, 0.3,-0.2,1]
        times  = [1,1,1,1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        


        # jointNames = ["RShoulderRoll", "RShoulderPitch", "RElbowRoll","HeadYaw", "HeadPitch"] 
        # angles = [-0.8, 1.6, 0.5, self.angles_start['HeadYaw'][0],self.angles_start['HeadPitch'][0]]
        # times  = [1,2,1,1,1]
        # isAbsolute = True
        # self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # arm move to go back at default pose with safety motion

        jointNames = ["RShoulderRoll", "RShoulderPitch", "RElbowRoll","HeadYaw", "HeadPitch"] 
        angles = [-0.9,0.4, self.angles_start['RElbowRoll'][0], self.angles_start['HeadYaw'][0],self.angles_start['HeadPitch'][0]]
        times  = [0.5,1,1,1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        jointNames = ["RShoulderRoll", "RShoulderPitch"] 
        angles = [self.angles_start['RShoulderRoll'][0], self.angles_start['RShoulderPitch'][0]]
        times  = [1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        self.default()


    def interactWin(self, time_wheel_motion = 4):  # time: 6 + 4  + 3 [s] = 13 + 1 (default) = 14[s]

        jointNames = ["HeadYaw", "HeadPitch"]
        angles = [-0.2, -0.2]
        times  = [1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # safety move to avoid collision with handle
        jointNames = ["RShoulderRoll", "RHand", "RShoulderPitch"]   
        angles = [-1,1,- 0.5]  #0.8
        times  = [1,1,2]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        # to handle
        jointNames = ["RShoulderPitch","RShoulderRoll", "RElbowRoll", "RElbowYaw","RWristYaw"]   
        angles = [-0.4, -0.2,  0.2, 0.8, -0.8]  #0.8
        times  = [1,1, 1, 1, 1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # close hand
        jointNames = ["RHand"]   
        angles = [0]
        times  = [1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # rotate wrist and elbow
        jointNames = ["RWristYaw", "RElbowYaw", "RShoulderPitch", "RShoulderRoll"]   
        angles = [1.2, 0, -0.45, -0.15]
        times  = [1,1,1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        # wait virtual motion
        time.sleep(time_wheel_motion)


        # rotate wrist back and open hand, rest position of the handle 
        jointNames = ["RWristYaw", "RElbowYaw", "RShoulderPitch", "RShoulderRoll","RHand"]   
        angles = [-0.8, 0.8, -0.45,-0.2,1]
        times  = [1,1,1,1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

    
        # arm move to go back at default pose with safety motion

        jointNames = ["RShoulderRoll", "RShoulderPitch", "RElbowRoll","HeadYaw", "HeadPitch"] 
        angles = [-0.9,-0.3, self.angles_start['RElbowRoll'][0], self.angles_start['HeadYaw'][0],self.angles_start['HeadPitch'][0]]
        times  = [0.5,1,1,1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


        jointNames = ["RShoulderRoll", "RShoulderPitch"] 
        angles = [self.angles_start['RShoulderRoll'][0], self.angles_start['RShoulderPitch'][0]]
        times  = [1,1]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        self.default()


    def dance(self):

        jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll"]
        angles = [0.64, 1.55, 0.64, -1.55]
        times = [0.5, 0.5, 0.5, 0.5]
        isAbsolute = True
        self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        self.continue_dance = True

        while self.continue_dance:
            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            angles = [0.34, 1.25, 1, -1.25, 0.15]
            times = [0.5, 0.5, 0.5, 0.5, 0.5]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            angles = [1, 1.85, 0.34, -1.85, 0.15]
            times = [0.5, 0.5, 0.5, 0.5, 0.5]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)


            angles = [0.34, 1.25, 1, -1.25, -0.15]
            times = [0.5, 0.5, 0.5, 0.5, 0.5]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            angles = [1, 1.85, 0.34, -1.85, -0.15]
            times = [0.5, 0.5, 0.5, 0.5, 0.5]
            isAbsolute = True
            self.motion.angleInterpolation(jointNames, angles, times, isAbsolute)

        self.default()

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
