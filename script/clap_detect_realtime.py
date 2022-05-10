import sounddevice as sd
import matplotlib.pyplot as plt
import sys
import queue
import numpy as np
from matplotlib.animation import FuncAnimation
import threading


def callback(indata, frames, time, status):
    global q
    if status:
        print(status, file=sys.stderr)
    q.put(indata[:, 0])


def update_data(frame):
    global buffer_data, q, plotdata
    while True:
        # get data immediately until no more data
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:] = data

        # put data to buffer_data for processing
        for d in data:
            buffer_data.put(d)
    # for debug purpose
    for line in lines:
        line.set_ydata(plotdata)
    return lines


def detect_clap():
    global buffer_data

    print("running clap detection in background...")
    fs = 44100
    thres = 0.5
    time_interval = 0.5  # seconds between two clap
    high_amp_thres = 30  # count in discrete domain
    trigger = False
    idx_start = 0
    idx_stop = 0
    idx_count = 0
    trigger_window_len = time_interval * fs  # window to count the high amplitude sound
    trigger_window_count = 0
    clap_count = 0

    while True:
        # get buffer_data from queue
        s = buffer_data.get()
        if trigger:
            if trigger_window_count < trigger_window_len:
                if s > thres:
                    idx_stop = idx_count
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
                    print("not a clap")
        else:
            if s > thres:
                trigger = True
                idx_start = idx_count
                # print("{}: {:.2f}".format(i, s))

        idx_count += 1

    print("detect {} clap(s)".format(clap_count))

    return 0


if __name__ == "__main__":
    device = 1  # check from $ python -m sounddevice
    q = queue.Queue()
    sf = 44100

    buffer_data = queue.Queue()  # store array of [index, data]
    plot_len = int(sf * 1)  # plot audio data only last 1 seconds
    plotdata = np.zeros(plot_len)
    last_index = 0

    # display realtime plot
    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    # detect clap in thread
    # mutex = threading.Lock()
    t1 = threading.Thread(name="thread1", target=detect_clap)
    t1.start()
    # t1.join()

    stream = sd.InputStream(device=device, channels=1, samplerate=sf, callback=callback)
    ani = FuncAnimation(fig, update_data, interval=30, blit=True)
    with stream:
        plt.show()
