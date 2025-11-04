# phone-phone-goose
# Phone Entropy Chain 🌀📱🔊

A deranged circle of doom: Line up 20+ smartphones in a ring. One starts with a crisp audio clip (your voice? A banger beat? Cthulhu whispers?). Each phone records the incoming sound from the previous one's speaker, mangles it with digital decay (filters, noise, pitch wobbles), and passes the abomination to the next. By the end? Pure auditory apocalypse—like telephone game on bath salts.

Inspired by analog horror and signal entropy. Built for viral TikToks, art installs, or just watching tech weep.

## 🎯 Quick Demo
1. Arrange phones in a circle (mic → speaker, 6-12" apart).
2. Run the app on all—scan QR for IDs (0 = originator).
3. Phone 0: Record/play starter clip.
4. Watch the chain: Entropy builds. Last phone? Uploads the final mutant for playback showdown.

## 🚀 Getting Started

### Hardware Setup
- 5-20 Android/iOS phones (older = more grit).
- Quiet room, consistent volume. Test mic/speaker pairs.
- Optional: Tripods for stability.

### Run the Sim First (Python)
No phones? Prototype the decay!
```bash
cd sim
pip install -r requirements.txt
python degrade.py  # Spits out stats & WAVs in outputs/
Tweak degrade_audio() for your flavor of ruin.







