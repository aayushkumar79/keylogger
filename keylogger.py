from pynput.keyboard import Key,Listener,KeyCode
import time

ct=time.localtime()

f=open("keylog.txt","a+")
f.write("====================================\nSESSION SUMMARY {}:{}:{} {}/{}/{}\n------------------------------------\n".format(ct.tm_hour,ct.tm_min,ct.tm_sec,ct.tm_mday,ct.tm_mon,ct.tm_year))

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
        l.append("{:02d}:{:02d}:{:.2f}; 'j'\n".format(*convert(time.time()-start)))
        return False
    if key in d:
        if key==Key.backspace:
            global b
            b=b+1
            l.append("{:02d}:{:02d}:{:.2f}; {}\n".format(*convert(time.time()-start),d[key]))
            print("{:02d}:{:02d}:{:.2f}; {}".format(*convert(time.time()-start),d[key]))
        else:
            l.append("{:02d}:{:02d}:{:.2f}; {}\n".format(*convert(time.time()-start),d[key]))
            print("{:02d}:{:02d}:{:.2f}; {}".format(*convert(time.time()-start),d[key]))
    elif hasattr(key,"vk") and key.vk in d:
        l.append("{:02d}:{:02d}:{:.2f}; {}\n".format(*convert(time.time()-start),d[key.vk]))
        print("{:02d}:{:02d}:{:.2f}; {}".format(*convert(time.time()-start),d[key.vk]))
    else:
        l.append("{:02d}:{:02d}:{:.2f}; {}\n".format(*convert(time.time()-start),key))
        print("{:02d}:{:02d}:{:.2f}; {}".format(*convert(time.time()-start),key))

def releasing(key):
    current.discard(listener.canonical(key))
    
with Listener(on_press=show,on_release=releasing) as listener:
    listener.join()

print("No of keystrokes:",c)
print("Backspace Rate; {:.2f}\n".format(b*100/c))
f.write("Total Runtime; {:02d}:{:02d}:{:.2f}\n".format(*convert(time.time()-start)))
f.write("Total Keystrokes; {}\n".format(c))
f.write("Backspace Rate; {:.2f}\n".format(b*100/c))
f.write("------------------------------------\n")
f.writelines(l)
f.write("====================================\n")
f.close()
