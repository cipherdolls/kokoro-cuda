# Kokoro TTS Benchmark Results

**Date:** 2026-03-19 09:19 UTC

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
| wav | 100ms | 735.4KB | 98.58% |
| mp3 | 119ms | 308.1KB | 98.58% |
| opus | 125ms | 380.2KB | 98.58% |
| flac | 63ms | 370.4KB | 98.58% |
| pcm | 60ms | 735.4KB | n/a |

## Results: WAV

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 220ms | 19ms | 621ms | 93.8KB |
| medium | 105 chars | 36ms | 31ms | 45ms | 331.7KB |
| long | 323 chars | 109ms | 67ms | 186ms | 972.7KB |
| numbers | 74 chars | 33ms | 30ms | 40ms | 294.2KB |
| punctuation | 69 chars | 30ms | 26ms | 37ms | 199.3KB |
| very_long | 910 chars | 173ms | 169ms | 180ms | 2520.7KB |

Avg latency: **100ms** | Throughput: **2498 chars/sec**

## Results: MP3

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 55ms | 50ms | 64ms | 40.8KB |
| medium | 105 chars | 73ms | 69ms | 80ms | 139.7KB |
| long | 323 chars | 144ms | 141ms | 148ms | 406.9KB |
| numbers | 74 chars | 75ms | 72ms | 79ms | 124.3KB |
| punctuation | 69 chars | 62ms | 58ms | 69ms | 84.9KB |
| very_long | 910 chars | 305ms | 301ms | 307ms | 1051.9KB |

Avg latency: **119ms** | Throughput: **2107 chars/sec**

## Results: OPUS

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 52ms | 49ms | 59ms | 38.0KB |
| medium | 105 chars | 77ms | 72ms | 84ms | 168.0KB |
| long | 323 chars | 152ms | 150ms | 155ms | 508.7KB |
| numbers | 74 chars | 75ms | 72ms | 82ms | 147.4KB |
| punctuation | 69 chars | 63ms | 58ms | 70ms | 98.2KB |
| very_long | 910 chars | 328ms | 325ms | 331ms | 1321.0KB |

Avg latency: **125ms** | Throughput: **2011 chars/sec**

## Results: FLAC

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 21ms | 20ms | 23ms | 38.1KB |
| medium | 105 chars | 34ms | 33ms | 36ms | 163.7KB |
| long | 323 chars | 68ms | 68ms | 69ms | 502.2KB |
| numbers | 74 chars | 36ms | 34ms | 37ms | 141.7KB |
| punctuation | 69 chars | 30ms | 29ms | 31ms | 92.4KB |
| very_long | 910 chars | 187ms | 185ms | 189ms | 1284.1KB |

Avg latency: **63ms** | Throughput: **3992 chars/sec**

## Results: PCM

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 25ms | 23ms | 28ms | 93.8KB |
| medium | 105 chars | 35ms | 34ms | 36ms | 331.6KB |
| long | 323 chars | 70ms | 69ms | 71ms | 972.7KB |
| numbers | 74 chars | 31ms | 31ms | 32ms | 294.1KB |
| punctuation | 69 chars | 29ms | 29ms | 31ms | 199.2KB |
| very_long | 910 chars | 171ms | 167ms | 178ms | 2520.7KB |

Avg latency: **60ms** | Throughput: **4154 chars/sec**

## Whisper Validation Details

| Test | Similarity | Expected | Transcribed |
|------|-----------|----------|-------------|
| short | 100% | Hello, this is a test. | Hello, this is a test. |
| medium | 100% | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. |
| long | 98% | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text to speech synthesis is one of the most exciting applications, enabling natural sounding voice generation from written text. | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text-to-speech synthesis is one of the most exciting applications, enabling natural-sounding voice generation from written text. |
| numbers | 96% | There are 7 continents, 195 countries, and over 8 billion people on Earth. | There are seven continents, 195 countries, and over 8 billion people on Earth. |
| punctuation | 97% | Wait, what? Are you serious! That's incredible... I can't believe it. | Wait, what? Are you serious? That's incredible. I can't believe it. |
| very_long | 100% | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries-old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. |
