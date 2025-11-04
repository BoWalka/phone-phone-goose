import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import glob
import os

# Grab all phone WAVs (assumes outputs/ exists)
phone_files = sorted(glob.glob('outputs/phone_*.wav'))
n_phones = len(phone_files)

rms_levels = []
dom_freqs = []

sample_rate = 44100
duration = 2.0
t = np.linspace(0, duration, int(sample_rate * duration), False)

def analyze_wav(filename):
    sr, data = wavfile.read(filename)
    data = data.astype(np.float32) / 32767.0  # Normalize
    rms = np.sqrt(np.mean(data**2))
    fft = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1/sr)
    dom_freq = freqs[np.argmax(np.abs(fft[:len(fft)//2]))]
    return rms, dom_freq

# Load & analyze
for i, file in enumerate(phone_files, 1):
    rms, freq = analyze_wav(file)
    rms_levels.append(rms)
    dom_freqs.append(freq)
    print(f"Phone {i}: RMS {rms:.4f}, Freq {freq:.1f}Hz")

# Plot the madness
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(range(1, n_phones+1), rms_levels, 'r-', marker='o', label='RMS Energy')
ax1.set_ylabel('RMS Level')
ax1.set_title('Audio Entropy Chain: The RMS Rampage')
ax1.grid(True)
ax1.legend()

ax2.plot(range(1, n_phones+1), dom_freqs, 'b-', marker='s', label='Dominant Freq')
ax2.set_ylabel('Freq (Hz)')
ax2.set_xlabel('Phone #')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig('outputs/degradation_plot.png')  # Save for repo glory
plt.show()  # Or just save if headless

print("Plot saved as outputs/degradation_plot.png – Frame your descent!")
