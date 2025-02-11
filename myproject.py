
'''
APM: 

injaro ezafe kardam agar soal dashtid inja benevisid, moafagh bashid


Alan prozhe nahaei hamine?
bale faghat shoma bayad 1--> tamame print haro neevshte bashid
2--> task1 ro kamel ezafe krde bashid (k anjam dadid)
3--> va takmil konid tamame function haro + 2 ta function ham az rooye khalaghiat ekhdoeton
**commente akahr ham bebinid va bebinid aya nokteye estefadeye class ha ro gereftid ? va b in fekr konid chegone dar real world azin fucntion ha estefade mishe, 
yani user interfacemon chie? (k dar jalaseye akhar sohabt mishe rajebesh

'''


import numpy as np
class Sensor:
    def __init__(self,topic,pin=100):
        self.topic=topic
        self.topic_list=self.topic.split('/')
        self.group=self.topic_list[1]
        self.device_type=self.topic_list[2]
        self.name=self.topic_list[3]
        self.pin=pin

    def read_sensor(self):
        if self.device_type=='thermo':
            a=np.random.uniform(22,27)
            self.curren_value=a
            return self.curren_value
        elif self.device_type=='light':
            a=np.random.uniform(0,100)
            self.curren_value=a
            return self.curren_value

a=Sensor('home/living_room/thermo/t10')
a.name
a.group
a.device_type
a.read_sensor()


'''

APM:

neveshtin ke pycharm kar mikone inja na
inja manzooretoon github hast? github jaee baraye run nadare

na manzoram dakhel pychram ke ba super motagheyrhay klass ghabli ke moshtarak hast farkhani mikonim
ama dakhel spyder kar nemikonad


****
ba super() shoam mitonid clas ghabli ro farakhani konid
ama be harhal rabti b spdyer, pycharm nadare, compilere hamashon pythone
emkan nadare yek code bznid va spyder yek javab bede va pycharm javabe dg ee
faghat GUI frgh darad

Sepas


'''
#import paho.mqtt.client as mqtt
#import RPi.GPIO as GPIO        
class Device(Sensor):
    def __init__(self,topic,mqtt_broker='localhost',port=1883):
        super().__init__(topic)    #داخل پای چارم کار میکند اما اینجا نه
        # self.topic=topic
        # self.topic_list=self.topic.split('/')        
        # self.group=self.topic_list[1]
        # self.device_type=self.topic_list[2]
        # self.name=self.topic_list[3]
        self.port=port
        self.mqtt_broker=mqtt_broker 
        self.status='off'
        self.speed=0
        self.temperatur=24
        #self.connect_mqtt()
        self.setup_gpio()

    def connect_mqtt(self):
        self.mqtt_client.connect(self.mqtt_broker,self.port)
        print(f'{self.name} connected to mqtt')
        
    def setup_gpio(self):
        if self.device_type=='lights':
            GPIO.setup(17,GPIO.OUT)
            print(f'{self.name} connected to gpio')

        elif self.device_type=='doors': 
            GPIO.setup(27,GPIO.OUT)
            print(f'{self.name} connected to gpio')
            
        elif self.device_type=='fans':
            GPIO.setup(22,GPIO.OUT)
            if self.speed>0:
                GPIO.setup(18, GPIO.OUT)  # For fan speed, if using PWM
                #self.pwm = GPIO.PWM(18, 100)  # PWM frequency 100Hz
                #self.pwm.start(0)
                print(f'{self.name} connected to gpio')
        elif self.device_type=='water':
            if self.temperatur>40:
                GPIO.setup(29,GPIO.OUT)
                print(f'{self.name} connected to gpio')
                
    def turn_on(self):
        self.status='on'
        print(f'{self.name} is turned on')
        #self.send_command('TURN_ON') #ramzie k toye MQTT
        if self.device_type=='lights':
            pass
            #GPIO.output(17, GPIO.HIGH)
            
        elif self.device_type=='doors':
            pass
            #GPIO.output(27, GPIO.HIGH)
            
        elif self.device_type=='fans':
            pass
            #GPIO.output(22, GPIO.HIGH)
        elif self.device_type=='water':
            #GPIO.output(29,GPIO.HIGH)
            pass
                     
    def set_speed(self,speed):
        if self.status=='off':
            print(f'{self.name} currently is off')
            return None      
        else:
            self.speed=speed
            #self.send_command(f'SET_SPEED:{speed}')
    
    def turn_off(self):
        self.status='off'
        print(f'{self.name} is turned off')
        #self.send_command('TURN_OFF')
        if self.device_type=='lights':
            #GPIO.output(17, GPIO.LOW)
            pass
        elif self.device_type=='doors':
            #GPIO.output(27, GPIO.LOW)
            pass
        elif self.device_type=='fans':
            #GPIO.output(22, GPIO.LOW)
            pass
        elif self.device_type=='water':
            #GPIO.output(29,GPIO.LOW)
            pass
            
    def get_status(self):
        return (f'{self.name} is {self.status}')
        
    def send_command(self,command):
        '''send a command via MQTT'''
        self.mqtt_client.publish(self.topic,command)
        print(f'command {command} send to topic {self.topic}')
        
a1=Device('home/living_room/water/water2')
a1.name
a1.device_type
a1.group
a1.turn_on()
a1.get_status()
a1.turn_off()
a1.get_status()




class AdminPanel(Device):

    def __init__(self):
        self.groups={}
        
    def creat_group(self,group_name):
        if group_name not in self.groups:
            self.groups[group_name]=[]
            print(f'groups {group_name} created')
        else:
            print('your group name is duplicated name')
            
    def add_device_to_group(self,group_name,device_type):
        if group_name in self.groups:
            self.groups[group_name].append(device_type)
            print(f'{device_type} add to {group_name}')
        else:
            print(f'Group {group_name} does not exist')
            
    def creat_device(self,group_name,device_type,name):
        if group_name in self.groups:
            topic=f'home/{group_name}/{device_type}/{name}'
            new_device=Device(topic)
            self.add_device_to_group(group_name, new_device)
            print(f'{new_device} created!')
        else:
            print(f'Group {group_name} does not exist')
            
    def create_multiple_devices(self,group_name,device_type,number_of_devices):
        if group_name in self.groups:
            for i in range(1,number_of_devices+1):
                device_name=f"{device_type}{i}"
                topic=f'home/{group_name}/{device_type}/{device_name.lower()}'
                new_device=Device(topic)
                self.add_device_to_group(group_name, new_device)
        else:
            print(f'Group {group_name} does not exist')
            
    def get_devices_in_groups(self,group_name):
        if group_name in self.groups:
            return self.groups[group_name]
        else:
            print(f'Group {group_name} does not exist')
            return []

    def turn_on_all_in_group(self,group_name):
        devices=self.devices_ingroups(group_name)
        for device in devices:
            device.turn_one()
            print(f'{device} is turned on')
          
    def turn_off_all_in_group(self,group_name):
        devices=self.devices_ingroups(group_name)
        for device in devices:
            device.turn_off()
            print(f'{device} is turned off')
        
    def trun_on_all(self):
        devices_all=self.group
        for device in devices_all:
            device.turn_one()
            print(f'{device} are turned on')
        pass
        
    def turn_off_all(self):
        devices_all=self.group
        for device in devices_all:
            device.turn_off()
            print(f'{device} are turned off')
        
    def get_status_in_group(self,group_name):
        devices=self.devices_ingroups(group_name)
        for device in devices:
            return self.status
    
    def get_status_in_device_type(self,device_type):
        devices_type=self.devices_ingroups(device_type)
        for device in devices_type:
            return self.status
    
    def creat_sensor(self,group_name,device_type,name) :
        if group_name in self.groups:
            topic=f'home/{group_name}/{device_type}/{name}'
            new_sensor=Sensor(topic)
            self.add_device_to_group(group_name, new_sensor)
            print(f'{new_sensor} created!')
        else:
            print(f'Group {group_name} does not exist')

    def get_status_sensor_in_group(self,group_name):
        devices=self.devices_ingroups(group_name)
        for sensor in devices:
            return self.status
    
    import time
    from datetime import datetime    
    def alarm_sleep(self,group_name):
        if groups[group_name]=='speaker':     #میخوام چک کنم ببینم داخل گروهام(لیوینگ روم یا آشپزخانه) بلندگو هست یا نه؟
            time='23:00:00'
            while True:
                now=datetime.now().strftime("%H:%M:%S")
                if now==time:
                    print(f'time sleep')
                else:
                    pass
                
    def test_healthy_device(self,group_name,device_type,name):
        pass
    
a1=AdminPanel()               
a1.groups        
a1.creat_group('living_room')
a1.groups
a1.creat_group('parking')
a1.groups
a1.add_device_to_group('parking', 'lamps')
a1.add_device_to_group('living_room', 'lamps')
a1.add_device_to_group('parking', 'door')
a1.groups
a1.creat_device('living_room','lamps','lamp1')  #<__main__.Device object at 0x00000126460729F0> created! چکار کنیم که بخشی ار حافظه نشان ندهد
#motasefane nemishnase classi k ma sakhtim ro 


a1.groups
a1.create_multiple_devices('living_room','lamps',40)
mygroups=a1.groups['living_room']
mygroups[1].name #lamps2'
mygroups[3].name

#----------
'''
bebinid shoma yek class darid bename a1 , tamam tabe ha mesle turn_off_all and ... hame ina motealegh b a1 hast
masalan bayad benevsiid a1.create .. and ...

bad tooo dele khode adminpanel (a1) ma yek groups darim k yek dictionarie
bad shoma ag bezanid a1.groups['living_room'] in yek list hast bad ag benevisid [0] in dg admin_panel nsiot balke yek variable
yek class dg bename (Device) hast k tabe haye khodesho dare
shoma yekja neveshtid mygroups[1] --> in device e 2 vom tooye living room hast k yek class hast bename Device ke tabe haye (turn_off , turn_on va .. dare)
ama dose khat paeen tar shoma neveshtid mygroup[1].turn_off_all() --> in tabe ye turn_off_all az adminpanel hast na device
mitonid benevisid a1.turn_off_all()
'''

'''
yekam baram pichide shode vaghiat 
az a1.turn_off_all() estefade kardam vali baz error dad
fekr konam kola moshkel az tabei ke tarif kardam hast

saiti nist ke tamrin karbordi az classha va tavabe dade bashe ke botonim bishtar tamrin konim
'''
#-------
mygroups[1].turn_on()   
mygroups[1].turn_off()    #چرا از توابع کلاس دیوایس استفاده شده وقتی که تابع آن داخل خود کلاس تعربف شده چون این مثال برای خاموشی دیوایس داخل گروه خودش یوده

mygroups[1].turn_off_all()    #AttributeError : 'Device' object has no attribute 'turn_off_all'


mygroups[2].get_status()
mygroups[2].get_status_in_group()     #AttributeError: 'Device' object has no attribute 'get_status_in_group'
s1=AdminPanel()
s1.creat_sensor('living_room','harigh','harigh1')
a1.alarm_sleep('living_room')
