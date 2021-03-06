import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import EnergyUtils as eu
import Yin as YIN
import ScaleMatcher as sm
import MidiConvert as mc


def most_common(lst):
    return max(set(lst), key=lst.count)


run_scripts = [1, 2, 3]

####################################################################################
if 1 in run_scripts:
    fs = 48000
    duration = 5
    rec_load = True
    hear = False
    if rec_load:
        raw_rec = sd.rec(fs*duration, fs, channels=1)
        print('Start')
        sd.wait()
        print('End')
        rec = np.array(raw_rec).reshape(-1)
        np.save('./Audios/LastAudio.npy', rec)
    else:
        rec = np.load('./Audios/LastAudio.npy')
    if hear:
        sd.play(rec, fs)
        sd.wait()
##################################################################################

if 2 in run_scripts:
    energy_est = eu.binary_voice_detector(rec, th=0.00)
    plt.plot(np.abs((rec**2)))
    plt.show()
    silenced_rec = energy_est*rec


##################################################################################

if 3 in run_scripts:
    p = YIN.Yin()
    slen = 2048
    lst = p.yin(silenced_rec, 48000, slen, slen, 100, 2000, .2)[0]
    a = sm.caster(lst)
    lst = list(a[0]/a[1]*440)
    time_vect = np.linspace(0, len(silenced_rec)/48, len(lst))
    mc.yin_2_midi(lst)
    plt.title('YIN Pitch Estimation'), plt.plot(
        time_vect, lst, label='T')
    plt.xlabel('Time [ms]'), plt.ylabel('Frequency [Hz]')
    plt.grid(), plt.legend()
    plt.show()
    '''
    lst = p.yin(silenced_rec, 48000, int(2048/4),
                int(1024/4), 100, 2000, .4)[0]
    time_vect = np.linspace(0, len(silenced_rec)/48, len(lst))
    plt.title('YIN Pitch Estimation'), plt.plot(
        time_vect, lst, 'o', label='Frames Size : Original/4')
    plt.xlabel('Time [ms]'), plt.ylabel('Frequency [Hz]')
    plt.grid(), plt.legend()

    lst = p.yin(silenced_rec, 48000, 2048*8, 1024*8, 100, 2000, .4)[0]
    time_vect = np.linspace(0, len(silenced_rec)/48, len(lst))
    plt.title('YIN Pitch Estimation'), plt.plot(
        time_vect, lst, 'o', label='Frames Size : Original*8')
    plt.xlabel('Time [ms]'), plt.ylabel('Frequency [Hz]')
    plt.grid(), plt.legend()
    '''
    # plt.show()

#################################################################################
if 4 in run_scripts:
    a = sm.caster(lst)
    lst = a[0]/a[1]*880

##################################################################################

if 5 in run_scripts:
    tones = []
    for lsti in lst:
        tones.append(int(round(12*np.log2(lsti/440) + 69))
                     ) if lsti > 0 else tones.append(0)
    # plt.plot(tones)
    mc.to_midi(tones)

##################################################################################
