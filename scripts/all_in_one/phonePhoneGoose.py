#"""
#Phone Entropy Chain: One-Stop Chaos Generator & Viz Beast 🌀📱🔊
#================================================================

#The ultimate script-kiddie-friendly mashup: Gen a chain of 20 degraded audio clips (sine wave to sonic apocalypse),
#then analyze & plot the RMS energy + dominant freq descent. 

#WHY ONE SCRIPT? Easy peasy—run it all, or comment out sections you don't grok yet.
#- Section 1: Config (tweak params here, noob-proof).
#- Section 2: Degrade chain (gen WAVs—comment # to skip if you just want plots).
#- Section 3: Analyze & plot (viz the madness—comment # to skip if audio-only).

#RUN ME:
#1. pip install numpy scipy matplotlib  # If not already (one-time).
#2. python this_script.py  # From your GOOSE dir
#3. Outputs: WAVs & PNG in C:\Users\Administrator\Desktop\PHONEphoneGOOSE\outputs\
 #  - Chain 'em in Audacity for the full ear-bleed symphony.
 #  - PNG: RMS ramp + freq wobble graph. Embed in README.md like ![Doom Plot](outputs/degradation_plot.png)

#TIPS FOR KIDDIES:
#- Comment out = Add # at line start. Boom, skipped.
#$- Randomness? Each run varies (noise/drift). Seed np.random.seed(42) for same-same.
#- Upgrade? Tweak degrade_audio()—add reverb? Reverse? Go wild.
#- Scale? Change n_phones=5 for quick tests.

#Built for the PHONEphoneGOOSE repo. Commit as "v0.2: United the scripts—now one chaotic monolith." 🚀 """"

import numpy as np
from scipy import signal
from scipy.io import wavfile
import os
import glob
import matplotlib.pyplot as plt  # For plots—comment below if no viz

# =============================================================================
# SECTION 1: CONFIG – TWEAK YOUR CHAOS HERE (Safe zone for params)
# =============================================================================
# Output dir – Change this path if your GOOSE nest moved
output_dir = r'C:\Users\Administrator\Desktop\PHONEphoneGOOSE\outputs'
os.makedirs(output_dir, exist_ok=True)

# Audio params – Start simple, crank for more doom
sample_rate = 44100  # CD quality Hz
duration = 2.0       # Seconds per clip – Short for tests
n_phones = 20        # How many phones in the circle? 5=quick, 50=eternal suffering
original_freq = 440  # Starting note (A4) – Change to 261.6 for middle C vibes

# Degradation knobs – Dial up/down for flavor
noise_scale = 0.03   # Noise ramp per phone (0.01=whisper, 0.05=screech)
pitch_drift_amp = 0.03  # Freq wobble % (0.01=subtle, 0.05=drunk)

print("Config locked: {n_phones} phones, {duration}s clips @ {original_freq}Hz. Entropy incoming...".format(**locals()))

# =============================================================================
# SECTION 2: AUDIO DEGRADATION CHAIN – GEN THE WAV APOCALYPSE
# =============================================================================
# Comment out the whole block below (add # to def & for-loop) if you just want plots from existing WAVs
print("\n--- SECTION 2: Forging the Chain (Comment me out to skip gen) ---")

t = np.linspace(0, duration, int(sample_rate * duration), False)
original = 0.5 * np.sin(2 * np.pi * original_freq * t)  # Clean sine start – 50% volume

def degrade_audio(audio, phone_id):
    """
    The mangler: Low-pass filter (muffles highs), add noise (grit), pitch drift (wobble).
    Tweak inside for custom hell—e.g., add echo: audio + np.roll(audio, 1000)
    """
    # Low-pass: Cutoff drops per phone (cheap mic/speaker sim)
    cutoff = max(1000, 8000 - (phone_id * 300))  # Hz – Early: crisp, late: muffled
    b, a = signal.butter(4, cutoff / (sample_rate / 2), btype='low')
    filtered = signal.filtfilt(b, a, audio)
    
    # Noise injection: Ramps up – Early quiet, late static storm
    noise_level = phone_id * noise_scale
    noise = np.random.normal(0, noise_level, len(audio))
    noisy = filtered + noise
    
    # Pitch drift: Sine-based wobble + new drifted sine blend
    drift = 1 + np.sin(phone_id * 0.3) * pitch_drift_amp
    drifted = np.sin(2 * np.pi * original_freq * drift * t)
    return np.clip(noisy * 0.7 + drifted * 0.3, -1, 1)  # Blend & cap to -1/+1

# Chain it: Original → Phone 1 → ... → Phone 20
current = original.copy()
wavfile.write(os.path.join(output_dir, 'original.wav'), sample_rate, (current * 32767).astype(np.int16))

for i in range(1, n_phones + 1):
    current = degrade_audio(current, i)
    filename = os.path.join(output_dir, f'phone_{i}.wav')
    wavfile.write(filename, sample_rate, (current * 32767).astype(np.int16))
    rms = np.sqrt(np.mean(current**2))
    print(f"Phone {i}: Saved {os.path.basename(filename)} – RMS beast: {rms:.4f}")

print("Chain forged! {n_phones} mutants ready in {output_dir}".format(**locals()))

# =============================================================================
# SECTION 3: ANALYZE & PLOT – VIZ THE DESCENT (OR ASCENT TO NOISE HELL)
# =============================================================================
# Comment out the whole block below (add # to def & for-loop & fig) if you just want audio, no graphs
print("\n--- SECTION 3: Dissecting the Doom (Comment me out to skip plots) ---")

# Numeric sort key – Fixes "phone_10" before "phone_2" sorting stupidity
def natural_sort_key(filename):
    return int(os.path.basename(filename).split('_')[1].split('.')[0])

# Load phone WAVs, sorted numeric
phone_files = sorted(glob.glob(os.path.join(output_dir, 'phone_*.wav')), key=natural_sort_key)
n_phones_loaded = len(phone_files)

if n_phones_loaded == 0:
    print("No WAVs in outputs/ – Run Section 2 first, or point output_dir elsewhere!")
    exit(1)  # Bail if no files (don't crash the party)

rms_levels = []
dom_freqs = []

def analyze_wav(filename):
    """Crunch a WAV: RMS energy + dominant freq via FFT. Quick & dirty."""
    sr, data = wavfile.read(filename)
    data = data.astype(np.float32) / 32767.0  # Normalize to -1/+1
    rms = np.sqrt(np.mean(data**2))
    
    # FFT for freq peak (positive half only)
    fft = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), 1/sr)
    pos_len = len(fft) // 2
    pos_freqs = freqs[:pos_len]
    pos_fft = np.abs(fft[:pos_len])
    dom_freq = pos_freqs[np.argmax(pos_fft)]
    
    return rms, dom_freq

# Analyze each
for i, file in enumerate(phone_files, 1):
    rms, freq = analyze_wav(file)
    rms_levels.append(rms)
    dom_freqs.append(freq)
    print(f"Phone {i}: RMS {rms:.4f}, Dom Freq {freq:.1f}Hz")

# Plot: Two subplots – RMS climb + Freq wobble
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(range(1, n_phones_loaded+1), rms_levels, 'r-', marker='o', label='RMS Energy')
ax1.set_ylabel('RMS Level')
ax1.set_title('Audio Entropy Chain: The RMS Rampage')
ax1.grid(True)
ax1.legend()

ax2.plot(range(1, n_phones_loaded+1), dom_freqs, 'b-', marker='s', label='Dominant Freq')
ax2.set_ylabel('Freq (Hz)')
ax2.set_xlabel('Phone #')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
png_path = os.path.join(output_dir, 'degradation_plot.png')
plt.savefig(png_path)
plt.show()  # Pops window if GUI; else just saves

print(f"Plot etched in eternity: {png_path}")
print("All done! Tweak configs, rerun, remix. What's next—ML voices? BLE sync? Spill.")

# EOF – Your chaos awaits. Fork on GitHub, tag the madness. 🌀
