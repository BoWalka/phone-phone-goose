import numpy as np
from scipy import signal
from scipy.io import wavfile
import os

# Your output dir—tweak if needed
output_dir = r'C:\Users\Administrator\Desktop\PHONEphoneGOOSE\outputs'
os.makedirs(output_dir, exist_ok=True)

# Params (tweak here)
sample_rate = 44100
duration = 2.0  # Longer for fun
n_phones = 20
original_freq = 440

t = np.linspace(0, duration, int(sample_rate * duration), False)
original = 0.5 * np.sin(2 * np.pi * original_freq * t)  # Quiet start

def degrade_audio(audio, phone_id):
    cutoff = max(1000, 8000 - (phone_id * 300))  # Deeper drop
    b, a = signal.butter(4, cutoff / (sample_rate / 2), btype='low')
    filtered = signal.filtfilt(b, a, audio)
    
    noise_level = phone_id * 0.03
    noise = np.random.normal(0, noise_level, len(audio))
    noisy = filtered + noise
    
    # Pitch drift + harmonic distortion
    drift = 1 + np.sin(phone_id * 0.3) * 0.03
    drifted = np.sin(2 * np.pi * original_freq * drift * t)
    return np.clip(noisy * 0.7 + drifted * 0.3, -1, 1)

# Chain & save
current = original.copy()
wavfile.write(os.path.join(output_dir, 'original.wav'), sample_rate, (current * 32767).astype(np.int16))

for i in range(1, n_phones + 1):
    current = degrade_audio(current, i)
    filename = os.path.join(output_dir, f'phone_{i}.wav')
    wavfile.write(filename, sample_rate, (current * 32767).astype(np.int16))
    print(f"Phone {i}: Saved {filename} – Now a {np.sqrt(np.mean(current**2)):.4f} RMS beast.")

print("Chain complete! Play 'em in seq for the full descent.")
