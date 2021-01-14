from configparser import ConfigParser

from numpy import sin, pi, mean, median, argmax

class Analyser:

    def __init__(self, sample_rate=44100, chunk_length=5.0, window_length=0.25, hop_length=0.05, dominant_window_length=0.5, dominant_hop_length=0.25, dominant_scale=1.0, analyser_config=None):
        self.sample_rate = sample_rate
        
        if analyser_config != None:
            self.chunk_length = analyser_config['chunk_length']
            self.window_length = analyser_config['window_length']
            self.hop_length = analyser_config['hop_length']
            self.dominant_window_length = analyser_config['dominant_window_length']
            self.dominant_hop_length = analyser_config['dominant_hop_length']
            self.dominant_scale = analyser_config['dominant_scale']
        else:
            self.chunk_length = chunk_length
            self.window_length = window_length
            self.hop_length = hop_length
            self.dominant_window_length = dominant_window_length
            self.dominant_hop_length = dominant_hop_length
            self.dominant_scale = dominant_scale

        self.chunk_size = int(self.sample_rate * self.chunk_length)
        self.window_size = int(self.sample_rate * self.window_length)
        self.hop_size = int(self.sample_rate * self.hop_length)
        self.dominant_window_size = int(self.sample_rate * self.dominant_window_length) // self.hop_size
        self.dominant_hop_size = int(self.sample_rate * self.dominant_hop_length) // self.hop_size    

    def detect(self, signal):
        def detect_window(window):
            detected = [0.0] * len(window)
            for i in range(len(window)):
                detected[i] = window[i]**2 * sin(pi*i/len(window))**2
            return mean(detected)

        detection_signal = [0.0] * (len(signal) // self.hop_size)

        for i in range(self.hop_size, len(signal), self.hop_size):
            if i-(self.window_size//2) > len(signal) or i+(self.window_size//2) > len(signal):
                continue
            detection_signal[(i//self.hop_size)-1] = detect_window(signal[i-(self.window_size//2) : i+(self.window_size//2)-1])

        return detection_signal

    def peak_pick(self, detection_signal):
        peak_signal = []
        for i in range(self.dominant_hop_size, len(detection_signal), self.dominant_hop_size):
            window = detection_signal[i-(self.dominant_hop_size) : i]
            window_median = median(window)
            peak_signal += list(map(lambda x: x if x > self.dominant_scale*window_median else 0.0, window))

        cleared_peak_signal = peak_signal.copy()
        for i in range(self.dominant_hop_size, len(peak_signal), self.dominant_hop_size):
            if i-(self.dominant_window_size//2) > len(peak_signal) or i+(self.dominant_window_size//2) > len(peak_signal):
                continue
            window = peak_signal[i-(self.dominant_window_size//2) : i+(self.dominant_window_size//2)]
            if len(window) != 0:
                i_max = argmax(window)
                cleared_peak_window = [0.0] * len(window)
                cleared_peak_window[i_max] = window[i_max]
                cleared_peak_signal[i-(self.dominant_window_size//2) : i+(self.dominant_window_size//2)] = cleared_peak_window
        
        return cleared_peak_signal

    def peaks_to_timestamps(self, signal):
        timestamps = []

        for i in range(len(signal)):
            if signal[i] != 0.0:
                timestamp = i * self.hop_length
                amplitude = signal[i]
                timestamps.append((timestamp, amplitude))
        
        return timestamps

    def analyse(self, signal):
        detection_signal = self.detect(signal)
        peak_signal = self.peak_pick(detection_signal)
        return self.peaks_to_timestamps(peak_signal)