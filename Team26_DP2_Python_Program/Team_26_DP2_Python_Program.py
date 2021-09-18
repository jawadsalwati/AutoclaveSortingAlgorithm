## ----------------------------------------------------------------------------------------------------------
## DP-2 TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeat_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = q_arm()

update_thread = repeating_timer(2, update_sim)


'''
IBEHS 1P10 - DP-2 Computer Program

Team Number: 26

Student 1 Details (Name, macID, Student Number): Muhammad Jawad, Jawadm1, 400330872

Student 2 Details (Name, macID, Student Number): Bela Davidson, Davidb11, 400307288

Date: 2020-12-08

'''
import time
import random

## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------

'''
Controls:
- Q-arm moves when both arms are flexed together past the threshold value,0.3, AND when they have the same value
- Gripper is controlled by right arm being flexed past the threshold value of 0.3 and the left arm is extended to have a value of zero
- Drawer is controlled by left arm being flexed past the threshold value of 0.3 and the right arm is extended to have a value of zero

General work flow steps:
1) Move to pick up location by flexing both arms together past the threshold value, 0.3, and ensuring both right and left emulators have the same value
2) Close the gripper to pick up container, by flexing the right arm above the 0.3 value and extending the left arm, so it has a value of zero
3) Keeping both left and right arm values the same (by flexing them together), flex both arms past the threshold value, in order to go to the dropp off location
4) If wanting to open a drawer, extend right arm so it has a value of zero and flex left arm past threshold value
5) Open the gripper, to drop off container, by flexing the right arm above the 0.3 value and extending the left arm to a value of zero
6) If wanting to close a drawer,extend right arm so it has a value of zero and flex left arm past threshold value
7) Arm will move home. Repeat instructions for the remaining five containers. 
'''
##Muhammad Jawad
##Function outputs autobin location based on the container ID
def bin_loc(container_id):
    if container_id==1: ##small red
        dropoff =[-0.5931, 0.2396, 0.374]
    elif container_id==2: ##small green
        dropoff =[0.0001,-0.6392,0.374]
    elif container_id==3: ##small blue
        dropoff =[-0.0001,0.6392,0.374]
    elif container_id==4: ##large red
        dropoff = [-0.3782,0.1489,0.34]
    elif container_id==5: ##large green
        dropoff =[0.0,-0.4064,0.34]
    elif container_id==6: ##large blue
        dropoff =[0.0,0.4064,0.34]
    return dropoff

##Bela Davidson
#Function moves q arm to the desired location passed through the argument, once both arms are flexed past a threshold value and both arms have the same value
def move_end_effector (location):
    global threshold
    threshold = 0.3 ##threshold value globally defined to be 0.3
    while True: 
        if arm.emg_left() > threshold and arm.emg_right() > threshold and arm.emg_left()==arm.emg_right():
            #When both arms are flexed and exceeding the threshold, whilst having the same value, move to the appropriate location
             time.sleep(2) ##sleep functions added in order to prevent Q arm from knocking things over
             arm.move_arm(location [0],location[1],location[2])
             time.sleep(2)
             break
##Muhammad Jawad & Bela Davidson
##Function randomizes the order in which the containers will be distributed to their autoclave locations
def random_list_generator():
    unrandomized_list=[1,2,3,4,5,6] 
    randomized_list=[] #Placeholder list, will contain the used random values and ensure no repitition 
    for i in range (6): ##Loop chooses a random value from the unrandomized list, removes it and adds it to the randomized list and cycles six times 
        index=5-i  
        random_index=random.randint(0,index) 
        number=unrandomized_list[random_index] 
        randomized_list.append(number)
        unrandomized_list.remove(number)
    return randomized_list ##Function outputs a list of numbers from 1 to 6 in a randomized order

##Muhammad Jawad
##Makes gripper close if at pickup location and open if at autoclave location, once the right arm exceeds a threshold value of 0.3 and the left arm is fully extended
##Extent of which gripper closes is passed through the argument and determined in the main function
def control_gripper(autoclave_location,pick_up_location,gripper_value):
    while True:
        if arm.emg_right() > threshold and arm.emg_left()==0 and arm.effector_position()==(pick_up_location[0], pick_up_location[1], pick_up_location[2]):
            #If the right arm is flexed above threshold, the left arm is fully extended to have a value of zero and the effector position is at pick up location:
            arm.control_gripper(gripper_value) #close gripper
            break
        elif arm.emg_right() > threshold and arm.emg_left()==0 and arm.effector_position()==(autoclave_location [0], autoclave_location[1], autoclave_location[2]):
            #If the right arm is flexed above threshold, the left arm is fully extended to have a value of zero and the effector position is at the corresponding autoclave bin:
            arm.control_gripper((gripper_value)*(-1)) #open gripper 
            break

##Bela Davidson
#Controls the correct autoclave drawer based on the command (True or False) and the container ID   
def control_drawer(command, container_id):
    while True:
        if arm.emg_left() > threshold and arm.emg_right() == 0: ##Drawer is controlled once the left arm exceeds the threshold value and the right arm is fully extended to have a value of zero
            if container_id == 4:
                arm.open_red_autoclave(command)
                time.sleep(2)
            elif container_id == 5:
                arm.open_green_autoclave(command)
                time.sleep(2)
            elif container_id == 6:
                arm.open_blue_autoclave(command)
                time.sleep(2)
            break

##Muhammad Jawad & Bela Davidson
def general_pathway(autoclave_location,pick_up_location,gripper_value,home): ##Function allows Q arm to undergo a general pathway that is independent of container size
    move_end_effector(pick_up_location) #moves to pickup location
    time.sleep(2)
    control_gripper(autoclave_location,pick_up_location,gripper_value) #gripper function is called when the effector is at the pick up location
    move_end_effector(home)
    time.sleep(0.5)
    move_end_effector(autoclave_location)#moves to the autoclave bin location
    
##Muhammad Jawad & Bela Davidson    
def main_cont_or_term(): ## Continue/terminate function acts as a main function and repeats the process for every type of container organised in a random order
    ID_list=random_list_generator() #Order of container ID's assigned from the random list generator function
    home=[0.4064, 0.0, 0.4826]
    pick_up_location=[0.5056, 0.0, 0.0226]
    for container_id in ID_list: #cycles through the main function for each container ID in the list 
        autoclave_location=bin_loc(container_id) #autoclave location determined from respective container ID 
        arm.spawn_cages(container_id) 
        if container_id==4 or container_id==5 or container_id==6: ##Large container-specific pathway, allowing user to control the autoclave drawer
            gripper_value=23 ##How much gripper opens/closes for large container
            general_pathway(autoclave_location,pick_up_location,gripper_value,home)
            time.sleep(1)
            control_drawer(True, container_id) 
            time.sleep(3)
            control_gripper(autoclave_location,pick_up_location,gripper_value) #gripper function is called when the effector is at the autoclave location
            time.sleep(2)
            control_drawer(False, container_id)
            time.sleep(2)
        else: ##Small container-specific pathway
            gripper_value=30 ##How much gripper opens/closes for small container
            general_pathway(autoclave_location,pick_up_location,gripper_value,home)
            time.sleep(3) 
            control_gripper(autoclave_location,pick_up_location,gripper_value) #gripper function is called when the effector is at the autoclave location
            time.sleep(2)
        arm.home() ## Q arm returns to the home position for the cycle to repeat until all containers have been sorted
        time.sleep(2)

#Calling main function
time.sleep(3)
main_cont_or_term()

