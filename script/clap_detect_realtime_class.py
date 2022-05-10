import sounddevice as sd
import matplotlib.pyplot as plt
import sys
import queue
import numpy as np
from matplotlib.animation import FuncAnimation
import threading


class ClapDetector:
    def __init__(self, device, sf, plot_interval, downsample):
        # input stream
        self.stream = sd.InputStream(device=device, channels=1, samplerate=sf, callback=self.callback)
        self.input_queue = queue.Queue()
        self.capacity = 10000
        self.size = 0
        self.buffer_data = np.zeros((self.capacity, 1), dtype=float)
        # visualize
        plot_len = int(sf * plot_interval / downsample)  # plot audio data only last 1 seconds
        self.plotdata = np.zeros(plot_len)
        self.lines = None
        self.downsample = downsample

        # for detection
        self.trigger = False

    def plot_data(self):
        # display realtime plot
        fig, ax = plt.subplots()
        self.lines = ax.plot(self.plotdata)
        ax.axis((0, len(self.plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(bottom=False, top=False, labelbottom=False,
                       right=False, left=False, labelleft=False)
        fig.tight_layout(pad=0)

        ani = FuncAnimation(fig, self.update_plot, interval=30, blit=True)
        with self.stream:
            plt.show()

    def get_size(self):
        return self.size

    def detect_clap(self):

        print("running clap detection in background...")
        fs = 44100
        thres = 0.5
        time_interval = 0.5  # seconds between two clap
        high_amp_thres = 30  # count in discrete domain
        self.trigger = False
        idx_start = 0
        idx_stop = 0
        idx_count = 0
        trigger_window_len = int(time_interval * fs)  # window to count the high amplitude sound
        clap_count = 0
        with self.stream:
            while True:
                # get buffer_data from queue
                if self.get_size() - idx_count < trigger_window_len:
                    continue
                else:
                    for i in range(trigger_window_len):
                        s = self.buffer_data[idx_count + i]
                        if self.trigger:
                            if s > thres:
                                idx_stop = idx_count + i
                                # print("{}: {:.2f}".format(i, s))

                        else:
                            if s > thres:
                                self.trigger = True
                                idx_start = idx_count
                                # print("{}: {:.2f}".format(i, s))

                    # check clap sound
                    # print(idx_start, idx_stop)
                    high_amp_len = idx_stop - idx_start  # count in discrete domain
                    if high_amp_len > high_amp_thres:
                        print("clap detected !!!")
                        clap_count += 1
                    else:
                        print(".")

                    # update variable
                    self.trigger = False
                    idx_count += trigger_window_len
                    idx_start = 0
                    idx_stop = 0

    def update_plot(self, frame):
        while True:
            # get data immediately until no more data
            try:
                new_data = self.input_queue.get_nowait()
            except queue.Empty:
                break

            # visualize
            new_data_len = len(new_data)
            self.plotdata = np.roll(self.plotdata, -new_data_len, axis=0)
            self.plotdata[-new_data_len:] = new_data
            for line in self.lines:
                line.set_ydata(self.plotdata)
        return self.lines

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.input_queue.put(indata[::self.downsample, 0])

        # data for processing
        new_data_len = len(indata[:, 0])
        self.size += new_data_len
        if self.size > self.capacity:
            self.capacity *= 4
            print("add buffer size to {}".format(self.capacity))
            expanded_buffer_data = np.zeros((self.capacity, 1))
            expanded_buffer_data[:len(self.buffer_data)] = self.buffer_data
            self.buffer_data = expanded_buffer_data

        self.buffer_data[self.size - new_data_len:self.size] = indata[:, 0].reshape(-1, 1)


if __name__ == "__main__":
    device = 1  # check from $ python -m sounddevice
    sf = 44100
    downsample = 10
    cd = ClapDetector(device=device, sf=sf, plot_interval=0.2, downsample=downsample)
    cd.detect_clap()

    # TODO fix threading with plot
    # t1 = threading.Thread(name="thread1", target=cd.plot_data)
    # t2 = threading.Thread(name="thread2", target=cd.detect_clap)
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    # cd.plot_data()

