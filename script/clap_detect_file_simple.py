import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt


def check_channel(data):
    if data.shape[0] == 1:
        return 1
    else:
        return 2


if __name__ == "__main__":
    audio_path = "../audio/two_clap.wav"
    data, fs = sf.read(audio_path)
    ch1 = data

    total_duration = len(data) / fs  # second
    thres = 0.5
    time_interval = 0.5  # seconds between two clap
    high_amp_thres = 30  # count in discrete domain
    high_amp_len = 0
    trigger = False
    idx_start = 0
    idx_stop = 0
    trigger_window_len = time_interval * fs  # window to count the high amplitude sound
    trigger_window_count = 0
    clap_count = 0
    for i, s in enumerate(ch1):
        if trigger:
            if trigger_window_count < trigger_window_len:
                if s > thres:
                    idx_stop = i
                    # print("{}: {:.2f}".format(i, s))
                trigger_window_count += 1
            else:
                trigger = False
                trigger_window_count = 0

                # check clap sound
                # print(idx_start, idx_stop)
                high_amp_len = idx_stop - idx_start  # count in discrete domain
                if high_amp_len > high_amp_thres:
                    print("clap detected !!!")
                    clap_count += 1
                else:
                    print("nothing detected")
        else:
            if s > thres:
                trigger = True
                idx_start = i
                # print("{}: {:.2f}".format(i, s))

    print("detect {} clap(s)".format(clap_count))

    # plt.plot(ch1)
    # plt.show()

    # sd.play(data, fs)
    # sd.wait()
