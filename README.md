# Automation Scripts

This repository contains my random automation scripts for various tasks and utilities.

## Scripts

### Text to Voice

A simple ElevenLabs CLI script that converts text to speech and plays it. By default, it says "Task finished successfully" but you can provide a custom message.

**How to run:**
```bash
# Default message
uv run uv-scripts/text-to-voice.py

# Custom message
uv run uv-scripts/text-to-voice.py "Your custom text here"
```

**Requirements:**
- ElevenLabs API key set as environment variable: `ELEVENLABS_API_KEY`
- ffplay (comes with ffmpeg) for audio playback

### Weekly Coding Stats

This script tracks the number of lines of code written per week, showing weekly average and totals.

**How to run:**
```bash
uv run uv-scripts/weekly-coding-stats.py
```

**Sample Output:**
```
+------------+-----------------+
| Week       |           Lines |
+------------+-----------------+
| 2025 W00   |               3 |
| 2025 W02   |             850 |
| 2025 W03   |             160 |
| 2025 W04   |             252 |
| 2025 W05   |             160 |
| 2025 W06   |           1.553 |
| 2025 W09   |           7.354 |
| 2025 W10   |             517 |
| 2025 W11   |             177 |
| 2025 W12   |              87 |
| 2025 W13   |              64 |
| 2025 W14   |             104 |
| 2025 W15   |              53 |
| 2025 W16   |             142 |
| 2025 W17   |             195 |
| 2025 W18   |               3 |
| 2025 W19   |               2 |
| 2025 W20   |             453 |
| 2025 W21   |               7 |
| 2025 W22   |              87 |
| 2025 W23   |               2 |
| 2025 W25   |             139 |
| 2025 W26   |              53 |
| 2025 W27   |          13.343 |
| 2025 W28   |           2.661 |
| 2025 W29   |           8.019 |
| 2025 W30   |           6.434 |
| 2025 W31   |           7.807 |
| 2025 W32   |           2.788 |
| 2025 W33   |           2.277 |
| ────────── | ─────────────── |
| TOTAL      |          55.746 |
| AVG        |           1.858 |
+------------+-----------------+
```