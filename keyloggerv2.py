from pynput.keyboard import Key,Listener,KeyCode
import time
from datetime import datetime

ct=time.localtime()

f=open("keystrokes.log","a+",encoding="utf-8")
f.write("====================================\nSESSION SUMMARY {}/{}/{} {}:{}:{}\n------------------------------------\n".format(ct.tm_mday,ct.tm_mon,ct.tm_year,ct.tm_hour,ct.tm_min,ct.tm_sec))

count={}
c=0
b=0
start=time.time()

d={Key.media_volume_mute:"[VOLMUTE]",Key.media_volume_down:"[VOLDOWN]",Key.media_volume_up:"[VOLUP]",
   Key.media_previous:"[PREVIOUS]",Key.media_next:"[NEXT]",Key.media_play_pause:"[PLAY/PAUSE]",Key.media_stop:"[STOP]",12:"[USELESSFIVE]",
   KeyCode.from_char("a"):"a",74:"j",96:"0",97:"1",98:"2",99:"3",100:"4",101:"5",102:"6",103:"7",104:"8",105:"9",255:"[BRIGHTNESSCTRL]"}
current=set()
l=[]

def convert(sec):
    hours=int(sec//3600)
    mins=int((sec%3600)//60)
    sec=round(sec%60,2)
    return hours,mins,sec

def show(key):
    global c,b
    c=c+1
    current.add(listener.canonical(key))
    if Key.ctrl in current and Key.alt in current and KeyCode.from_char("j") in current:
        if "j" in count:
            count["j"]+=1
        else:
            count["j"]=1
        l.append("{:02d}:{:02d}:{:02d}.{}; j\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2]))
        return False
    if hasattr(key,"char") and key.char is not None:
        if key.char in count:
            count[key.char]+=1
        else:
            count[key.char]=1
        l.append("{:02d}:{:02d}:{:02d}.{}; {}\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],key.char))
##        print("{:02d}:{:02d}:{:02d}.{}; {}".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],key.char))
    elif key in d:
            if d[key]in count:
                count[d[key]]+=1
            else:
                count[d[key]]=1
            l.append("{:02d}:{:02d}:{:02d}.{}; {}\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],d[key]))
##            print("{:02d}:{:02d}:{:02d}.{}; {}".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],d[key]))
    elif hasattr(key,"vk") and key.vk in d:
        if d[key.vk] in count:
            count[d[key.vk]]+=1
        else:
            count[d[key.vk]]=1
        l.append("{:02d}:{:02d}:{:02d}.{}; {}\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],d[key.vk]))
##        print("{:02d}:{:02d}:{:02d}.{}; {}".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],d[key.vk]))
    else:
        if key==Key.backspace:
            if "[BACKSPACE]" in count:
                count["[BACKSPACE]"]+=1
            else:
                count["[BACKSPACE]"]=1
            b=b+1
            l.append("{:02d}:{:02d}:{:02d}.{}; [BACKSPACE]\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2]))
##            print("{:02d}:{:02d}:{:02d}.{}; [BACKSPACE]".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2]))
        if "[{}]".format(str(key).split(".")[1].split("_")[0].upper()) in count:
            count["[{}]".format(str(key).split(".")[1].split("_")[0].upper())]+=1
        else:
            count["[{}]".format(str(key).split(".")[1].split("_")[0].upper())]=1
        l.append("{:02d}:{:02d}:{:02d}.{}; [{}]\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],str(key).split(".")[1].split("_")[0].upper()))
##        print("{:02d}:{:02d}:{:02d}.{}; [{}]".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],str(key).split(".")[1].split("_")[0].upper()))
    
def release(key):
    current.discard(listener.canonical(key))
    if key==Key.esc:
        print("Key released: [ESC]")
        return False

with Listener(on_press=show,on_release=release) as listener:
    listener.join()

##print("No of keystrokes:",c)
##print("Backspace Rate; {:.2f}\n".format(b*100/c))
##print(dict(sorted(count.items(),key=lambda item:item[1],reverse=True)[:5]))
sortl=dict(sorted(count.items(),key=lambda item:item[1],reverse=True)[:5])
lines=[f"| {str(key):<17} | {value:<6} |\n" for key,value in sortl.items()]
f.write("Total Runtime; {:02d}:{:02d}:{:.2f}\n".format(*convert(time.time()-start)))
f.write("Total Keystrokes; {}\n".format(c))
f.write("Backspace Rate; {:.2f}\n".format(b*100/c))
f.write("+----------------------------+\n| Top 5 Most Pressed Keys;   |\n+-------------------+--------+\n")
f.writelines(lines)
f.write("+-------------------+--------+\n")
f.write("------------------------------------\n")
f.writelines(l)
f.write("====================================\n")
f.close()
