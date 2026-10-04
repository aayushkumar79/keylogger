from pynput.keyboard import Key,Listener,KeyCode
import time
from datetime import datetime

ct=time.localtime()

f=open("keystrokes.log","a+",encoding="utf-8")
f.write("====================================\nSESSION SUMMARY {}/{}/{} {}:{}:{}\n------------------------------------\n".format(ct.tm_mday,ct.tm_mon,ct.tm_year,ct.tm_hour,ct.tm_min,ct.tm_sec))

count={}
current=set()
c=0
b=0
start=time.time()

d={Key.esc:"[ESC]",Key.backspace:"[BACKSPACE]",Key.enter:"[ENTER]",Key.tab:"[TAB]",Key.num_lock:"[NUMLOCK]",
   Key.alt_l:"[ALT]",Key.alt_gr:"[ALT]",Key.alt_r:"[ALT]",Key.alt:"[ALT]",
   Key.ctrl:"[CTRL]",Key.ctrl_l:"[CTRL]",Key.ctrl_r:"[CTRL]",
   Key.shift:"[SHIFT]",Key.shift_r:"[SHIFT]",Key.cmd:"[CMD]",Key.cmd_r:"[CMD]",
   Key.space:"[SPACE]",Key.caps_lock:"[CAPSLOCK]",Key.delete:"[DELETE]",Key.scroll_lock:"[SCRLOCK]",
   Key.up:"[UP]",Key.down:"[DOWN]",Key.right:"[RIGHT]",Key.left:"[LEFT]",
   Key.page_up:"[PAGEUP]",Key.page_down:"[PAGEDOWN]",Key.home:"[HOME]",Key.end:"[END]",Key.insert:"[INSERT]",Key.print_screen:"[PRTSCR]",
   Key.f1:"[F1]",Key.f2:"[F2]",Key.f3:"[F3]",Key.f4:"[F4]",Key.f5:"[F5]",Key.f6:"[F6]",Key.f7:"[F7]",Key.f8:"[F8]",Key.f9:"[F9]",Key.f10:"[F10]",
   Key.f11:"[F11]",Key.f12:"[F12]",Key.f13:"[F13]",Key.f14:"[F14]",Key.f15:"[F15]",Key.f16:"[F16]",Key.f17:"[F17]",Key.f18:"[F18]",Key.f19:"[F19]",Key.f20:"[F20]",
   Key.f21:"[F21]",Key.f22:"[F22]",Key.f23:"[F23]",Key.f24:"[F24]",Key.menu:"[MENU]",
   Key.media_volume_mute:"[VOLMUTE]",Key.media_volume_down:"[VOLDOWN]",Key.media_volume_up:"[VOLUP]",
   Key.media_previous:"[PREVIOUS]",Key.media_next:"[NEXT]",Key.media_play_pause:"[PLAY/PAUSE]",Key.media_stop:"[STOP]",
   74:"'j'",96:"'0'",97:"'1'",98:"'2'",99:"'3'",100:"'4'",101:"'5'",102:"'6'",103:"'7'",104:"'8'",105:"'9'",255:"[BRIGHTNESSCTRL]"}
l=[]

def convert(sec):
    hours=int(sec//3600)
    mins=int((sec%3600)//60)
    sec=round(sec%60,2)
    return hours,mins,sec

def show(key):
    global c
    c=c+1
    current.add(listener.canonical(key))
    if Key.ctrl in current and Key.alt in current and KeyCode.from_char("j") in current:
        if "'j'" in count:
            count["'j'"]+=1
        else:
            count["'j'"]=1
        l.append("{:02d}:{:02d}:{:02d}.{}; 'j'\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2]))
        return False
    if key in d:
        if key==Key.backspace:
            if d[key] in count:
                count[d[key]]+=1
            else:
                count[d[key]]=1
            global b
            b=b+1
            l.append("{:02d}:{:02d}:{:02d}.{}; {}\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],d[key]))
        else:
            if d[key] in count:
                count[d[key]]+=1
            else:
                count[d[key]]=1
            l.append("{:02d}:{:02d}:{:02d}.{}; {}\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],d[key]))
    elif hasattr(key,"vk") and key.vk in d:
        if d[key.vk] in count:
            count[d[key.vk]]+=1
        else:
            count[d[key.vk]]=1
        l.append("{:02d}:{:02d}:{:02d}.{}; {}\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],d[key.vk]))
    else:
        if key in count:
            count[key]+=1
        else:
            count[key]=1
        l.append("{:02d}:{:02d}:{:02d}.{}; {}\n".format(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec,str(datetime.now().microsecond)[:2],key))

def releasing(key):
    current.discard(listener.canonical(key))
    
with Listener(on_press=show,on_release=releasing) as listener:
    listener.join()

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
