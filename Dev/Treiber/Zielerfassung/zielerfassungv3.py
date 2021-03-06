__author__ = 'Andri'

import math

import Dev.Treiber.Zielerfassung.config as CFG

import time
import subprocess
# import collections
# import threading
import os
import signal

proc = None
pid = -1


def read_output(process, append):
    for line in iter(process.stdout.readline, ""):
        print line
        if line.startswith("detect: "):
            str_pos = line.replace("detect: ", "")
            append(str_pos)
    print "zf3 t end"


class Zielerfassung:
    def __init__(self):
        try:
            self.config = CFG.ZFConfig()
            self.work_path = "/home/pi/PREN/hslu_pren_grp19_2014/Dev/Kommunikation/static/images"
            self.dir_path = os.path.dirname(os.path.abspath(__file__))
            # self.start_subproc()
        except Exception as ex:
            print ex.message

    def stop_subproc(self):
        global proc
        global pid
        try:
            print "zf3 proc stopping"
            if proc is not None:
                print "killing pid: " + str(proc.pid)
                os.killpg(proc.pid, signal.SIGTERM)
                #proc.kill()
                #os.kill(proc.pid)
                proc = None
                print "zf3 proc killed pid: " + str(pid)
                pid = -1
        except:
            pass

    def start_subproc(self):
        global proc
        global pid
        try:
            with open(self.work_path + "/detect.txt", 'w') as detect_file:
                detect_file.write("loading")
                detect_file.close()
            print "zf3 proc open"
            cmd = "sudo python /home/pi/PREN/hslu_pren_grp19_2014/Dev/Treiber/Zielerfassung/zf_subproc.py " + self.work_path
            proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
            pid = proc.pid
            print "zf3 proc started"
            time.sleep(5)

        except Exception as ex:
            print ex.message


    def read_file(self):
        str_pos = "loading"
        with open(self.work_path + "/detect.txt", 'r') as detect_file:
            str_pos = detect_file.readline()
            detect_file.close()
        return str_pos

    def detect(self):
        t = time.time()
        print 'zf3 detect'
        str_pos = self.read_file()
        counter = 0;
        while str_pos == "loading" and counter < 10:
            counter += 1
            time.sleep(0.3)
        position = int(float(str_pos))
        angle = math.atan(self.config.pixelToCMFactor * position)
        dt = time.time() - t
        print "position: pixel: " + str(position) + "  |  angle: " + str(angle) + "  |  time: " + str(dt * 1000)
        return angle

    def get_threshold(self):
        return self.config.threshold

    def set_threshold(self, threshold):
        self.stop_subproc()
        self.config.set_threshold(threshold)
        self.start_subproc()

    def get_image(self):
        self.detect()

    def save_config(self):
        global proc
        self.stop_subproc()
        self.config.save_config()
        time.sleep(2)
        proc = None
        self.start_subproc()

    def close(self):
        self.stop_subproc()

    def __del__(self):
        global proc
        global pid
        try:
            proc.kill()
            proc = None
            pid = -1
        except Exception as ex:
            print ex.message
