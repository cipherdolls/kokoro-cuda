# Kokoro TTS Benchmark Results

**Date:** 2026-03-19 09:35 UTC

## Hardware

| Property | Value |
|----------|-------|
| GPU | NVIDIA GeForce RTX 5090 |
| VRAM | 32607 MiB |
| Driver | 580.126.09 |
| Compute Capability | 12.0 |

## Configuration

| Setting | Value |
|---------|-------|
| Model | Kokoro v1.0 (82M params) |
| Voice | af_heart |
| Formats Tested | wav, mp3, opus, flac, pcm |
| Bitrate (lossy) | 192k |
| Sample Rate | 24000 Hz |
| Runs per test | 3 |
| Whisper Model | large-v3-turbo |

## Format Comparison

| Format | Avg Latency | Avg File Size | Whisper Similarity |
|--------|-------------|---------------|-------------------|
| wav | 101ms | 735.4KB | 98.58% |
| mp3 | 120ms | 308.1KB | 98.58% |
| opus | 124ms | 380.0KB | 98.58% |
| flac | 62ms | 370.4KB | 98.58% |
| pcm | 57ms | 735.4KB | n/a |

## Results: WAV

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 223ms | 20ms | 627ms | 93.8KB |
| medium | 105 chars | 36ms | 32ms | 45ms | 331.7KB |
| long | 323 chars | 111ms | 70ms | 187ms | 972.7KB |
| numbers | 74 chars | 33ms | 29ms | 41ms | 294.2KB |
| punctuation | 69 chars | 30ms | 26ms | 37ms | 199.3KB |
| very_long | 910 chars | 176ms | 170ms | 181ms | 2520.7KB |

Avg latency: **101ms** | Throughput: **2468 chars/sec**

## Results: MP3

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 67ms | 49ms | 102ms | 40.8KB |
| medium | 105 chars | 74ms | 69ms | 82ms | 139.7KB |
| long | 323 chars | 140ms | 139ms | 141ms | 406.9KB |
| numbers | 74 chars | 71ms | 68ms | 77ms | 124.3KB |
| punctuation | 69 chars | 63ms | 58ms | 69ms | 84.9KB |
| very_long | 910 chars | 306ms | 305ms | 307ms | 1051.9KB |

Avg latency: **120ms** | Throughput: **2086 chars/sec**

## Results: OPUS

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 54ms | 49ms | 63ms | 37.8KB |
| medium | 105 chars | 76ms | 72ms | 83ms | 167.7KB |
| long | 323 chars | 149ms | 149ms | 149ms | 509.0KB |
| numbers | 74 chars | 72ms | 69ms | 79ms | 147.3KB |
| punctuation | 69 chars | 64ms | 61ms | 70ms | 98.0KB |
| very_long | 910 chars | 327ms | 324ms | 329ms | 1320.1KB |

Avg latency: **124ms** | Throughput: **2024 chars/sec**

## Results: FLAC

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 24ms | 20ms | 32ms | 38.1KB |
| medium | 105 chars | 34ms | 32ms | 35ms | 163.8KB |
| long | 323 chars | 69ms | 68ms | 69ms | 502.1KB |
| numbers | 74 chars | 31ms | 31ms | 32ms | 141.7KB |
| punctuation | 69 chars | 28ms | 27ms | 29ms | 92.3KB |
| very_long | 910 chars | 184ms | 183ms | 187ms | 1284.5KB |

Avg latency: **62ms** | Throughput: **4069 chars/sec**

## Results: PCM

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 20ms | 20ms | 22ms | 93.8KB |
| medium | 105 chars | 32ms | 31ms | 33ms | 331.6KB |
| long | 323 chars | 65ms | 65ms | 66ms | 972.7KB |
| numbers | 74 chars | 29ms | 29ms | 30ms | 294.1KB |
| punctuation | 69 chars | 26ms | 26ms | 26ms | 199.2KB |
| very_long | 910 chars | 168ms | 166ms | 169ms | 2520.7KB |

Avg latency: **57ms** | Throughput: **4404 chars/sec**

## Whisper Validation Details

| Test | Similarity | Expected | Transcribed |
|------|-----------|----------|-------------|
| short | 100% | Hello, this is a test. | Hello, this is a test. |
| medium | 100% | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. |
| long | 98% | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text to speech synthesis is one of the most exciting applications, enabling natural sounding voice generation from written text. | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text-to-speech synthesis is one of the most exciting applications, enabling natural-sounding voice generation from written text. |
| numbers | 96% | There are 7 continents, 195 countries, and over 8 billion people on Earth. | There are seven continents, 195 countries, and over 8 billion people on Earth. |
| punctuation | 97% | Wait, what? Are you serious! That's incredible... I can't believe it. | Wait, what? Are you serious? That's incredible. I can't believe it. |
| very_long | 100% | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries-old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. |
