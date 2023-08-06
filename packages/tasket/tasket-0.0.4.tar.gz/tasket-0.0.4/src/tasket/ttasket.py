#!/usr/bin/env python

import argparse
#import cmd2
import os
import sys

#Premable - grab the args

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Maintain a list of needful things to do.")
    group = parser.add_mutually_exclusive_group()

    parser.add_argument("-t","--task", type=str, help="Add a new task to the list - use single or double quotes")
    group.add_argument("-d", "--done", type=int, help="Complete a task")
    group.add_argument("-x", "--skip", type= int, help="Skip a task")
    group.add_argument("-s", "--show", type= int, help="Show a (specific) task")

    args = parser.parse_args()
    task = args.task

    #print(17,repr(task))

    #Build and maintain the list

    tasklist = []
    
    tasklist.append(task)

    #print(25,repr(tasklist)) 


    #Show the current tasks

    print('\n')
    os.system('date')
    print('\n')
    os.system('cal')
    print('\n')
    

    #for i in tasklist:
	#    print(f'{i}' + ': ' + tasklist[i])
	
    [print(i) for i in tasklist] 

    #print(task)	
    print('\n')


