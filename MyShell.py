
"""psh: a simple Shell written in Python"""

import os , signal
from colorama import Fore, Back, Style
import psutil

bg_processes = []



def execute_command(command):
    
    pid = os.fork()
    split_string = []
    start_index = 0
    end_index = 0
    while True :
        if( end_index >= len(command) ) :
            if( command[end_index-1] == '"' ) :
                split_string.append(command[start_index:end_index-1])
                break
            else :
                split_string.append(command[start_index:])
                break    
            
        if( command[end_index] == '\\' ) :
            end_index +=2
        elif( command[end_index] == ' ' ) :
            split_string.append(command[start_index:end_index])
            start_index = end_index + 1
            end_index += 1
        elif( command[end_index] == '"' ) :
            end_index += 1
            start_index += 1
            while True :
                if( command[end_index] == '"' ) :
                    end_index += 1
                    break
                else :
                    end_index += 1
        else :
            end_index += 1
            
    
    
    if pid == 0:
        os.execvp(split_string[0], split_string)
    else:
        os.waitpid(0, 0)
        #os.wait()
        


    

def psh_cd(path):
    """convert to absolute path and change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))
        


def psh_bg(command):
    
    pid = os.fork()
    split_string = []
    start_index = 0
    end_index = 0
    while True :
        if( end_index >= len(command) ) :
            if( command[end_index-1] == '"' ) :
                split_string.append(command[start_index:end_index-1])
                break
            else :
                split_string.append(command[start_index:])
                break    
            
        if( command[end_index] == '\\' ) :
            end_index +=2
        elif( command[end_index] == ' ' ) :
            split_string.append(command[start_index:end_index])
            start_index = end_index + 1
            end_index += 1
        elif( command[end_index] == '"' ) :
            end_index += 1
            start_index += 1
            while True :
                if( command[end_index] == '"' ) :
                    end_index += 1
                    break
                else :
                    end_index += 1
        else :
            end_index += 1
            
            
    
    if pid == 0:
        os.execvp(split_string[0], split_string)
    else:
        my_tuple = (len(bg_processes)+1,pid,True)
        bg_processes.append(my_tuple)
        return
        
    
    
    
    
def psh_bgList():
    
    number_of_processes = 0
    
    for t in bg_processes :
        if( t[2] == True ) :
            print("(" + str(t[0]) + ")" + " " + str(psutil.Process(t[1]).cwd()) + "/" + str(psutil.Process(t[1]).name()) )
            number_of_processes += 1
    print("total background processes : " + str(number_of_processes) )
    
    
    
def psh_bgKill(n):
    
    try:
        os.kill(bg_processes[int(n)-1][1], signal.SIGTERM)
        del bg_processes[int(n)-1]
        return
    except:
        print('Unable to kill the process ' + n)
        
        
        
def psh_bgStop(n):
    
    try:
        os.kill(bg_processes[int(n)-1][1], signal.SIGSTOP)
        bg_processes[int(n)-1][2] = False
        return
    except:
        print('Unable to stop the process ' + n)
        
        
        
def psh_bgStart(n):
    
    try:
        os.kill(bg_processes[int(n)-1][1], signal.SIGCONT)
        bg_processes[int(n)-1][2] = True
        return
    except:
        print('Unable to start the process ' + n)
        

        
def psh_pwd():
    """print working directory"""
    try:
        print(os.getcwd())
    except Exception:
        print("pwd: no files here")


    
    
def main():
    
    while True:
        
        if(len(bg_processes) == 0) :
            print("All background jobs have been finished")
        
        inp = input("\n" + Fore.CYAN + os.getcwd() + "/shell> " + Fore.LIGHTYELLOW_EX)
        
        if inp == "exit":
            break
        elif inp[:3] == "cd ":
            psh_cd(inp[3:])
        elif inp[:3] == "pwd":
            psh_pwd()
        elif inp[:3] == "bg ":
            psh_bg(inp[3:])
        elif inp[:6] == "bglist":
            psh_bgList()
        elif inp[:7] == "bgkill ":
            psh_bgKill(inp[7:])
        elif inp[:7] == "bgstop ":
            psh_bgStop(inp[7:])
        elif inp[:8] == "bgstart ":
            psh_bgStart(inp[8:])
        elif inp == '' :
            pass
        else:
            execute_command(inp)


if '__main__' == __name__:
    main()



            
            
            