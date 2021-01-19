from numpy import sin, pi, mean

class Analyser:

    def __init__(self, sample_rate, chunk_length=2.0, window_length=0.5, hop_length=0.05, dominant_threshold=2.5e6, analyser_config=None):
        self.sample_rate = sample_rate
        
        if analyser_config != None:
            self.chunk_length = analyser_config['chunk_length']
            self.window_length = analyser_config['window_length']
            self.hop_length = analyser_config['hop_length']
            self.dominant_threshold = analyser_config['dominant_threshold']
        else:
            self.chunk_length = chunk_length
            self.window_length = window_length
            self.hop_length = hop_length
            self.dominant_threshold = dominant_threshold

        self.chunk_size = int(self.sample_rate * self.chunk_length)
        self.window_size = int(self.sample_rate * self.window_length)
        self.hop_size = int(self.sample_rate * self.hop_length)   

    def smooth_window(self, window):
        if len(window) > 0:
            smoothed = [0.0] * len(window)
            for i in range(len(window)):
                smoothed[i] = window[i]**2 * sin(pi*i/len(window))**2
            return mean(smoothed)
        else:
            return 0.0

    def smooth(self, signal):
        smoothed_signal = [0.0] * (len(signal) // self.hop_size)

        for i in range(self.hop_size, len(signal), self.hop_size):
            if i-(self.window_size//2) > len(signal) or i+(self.window_size//2) > len(signal):
                continue
            smoothed_signal[(i//self.hop_size)-1] = self.smooth_window(signal[i-(self.window_size//2) : i+(self.window_size//2)-1])

        return smoothed_signal

    def detect(self, smoothed_signal):
        detection_signal = [0.0] * len(smoothed_signal)
        for i in range(1, len(smoothed_signal)):
            detection_signal[i] = smoothed_signal[i] - smoothed_signal[i-1]
        return detection_signal

    def peak_pick(self, detection_signal):
        peak_signal = [0] * len(detection_signal)
        for i in range(1, len(detection_signal) - 1):
            l = detection_signal[i-1]
            m = detection_signal[i]
            r = detection_signal[i+1]
            peak_signal[i] = m if m > self.dominant_threshold and l < m and m >= r else 0
        return peak_signal

    def peaks_to_timestamps(self, peak_signal):
        timestamps = []

        for i in range(len(peak_signal)):
            if peak_signal[i] != 0.0:
                timestamp = i * self.hop_length
                amplitude = peak_signal[i]
                timestamps.append((timestamp, amplitude))
        
        return timestamps[1:] # drop first peak because it caused by signal smoothing

    def analyse(self, signal):
        h = self.hop_size
        w = self.window_size

        l  = self.smooth_window(signal[h-(w//2) : h+self.hop_size+(w//2)-1])
        h += self.hop_size
        ml = self.smooth_window(signal[h-(w//2) : h+self.hop_size+(w//2)-1])
        h += self.hop_size
        mr = self.smooth_window(signal[h-(w//2) : h+self.hop_size+(w//2)-1])
        h += self.hop_size
        r  = self.smooth_window(signal[h-(w//2) : h+self.hop_size+(w//2)-1])

        dl = ml - l
        dm = mr - ml
        dr = r - mr

        dominants = []

        while h < len(signal) - w//2:

            if dm > self.dominant_threshold and dl < dm and dm >= dr:
                t = (h//self.hop_size - 1) * self.hop_length
                dominants.append((t, dm))

            h += self.hop_size

            mr = r
            r  = self.smooth_window(signal[h-(w//2) : h+self.hop_size+(w//2)-1])

            dl = dm
            dm = dr
            dr = r - mr

        return dominants[1:] if len(dominants) > 1 else []