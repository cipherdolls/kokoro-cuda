# Kokoro TTS Benchmark Results

**Date:** 2026-03-20 09:56 UTC

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
| wav | 77ms | 735.4KB | 98.58% |
| mp3 | 120ms | 308.1KB | 98.58% |
| opus | 126ms | 380.2KB | 98.58% |
| flac | 63ms | 370.4KB | 98.58% |
| pcm | 61ms | 735.4KB | n/a |

## Results: WAV

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 107ms | 22ms | 277ms | 93.8KB |
| medium | 105 chars | 37ms | 34ms | 44ms | 331.7KB |
| long | 323 chars | 71ms | 67ms | 78ms | 972.7KB |
| numbers | 74 chars | 36ms | 32ms | 43ms | 294.2KB |
| punctuation | 69 chars | 33ms | 30ms | 38ms | 199.3KB |
| very_long | 910 chars | 180ms | 174ms | 193ms | 2520.7KB |

Avg latency: **77ms** | Throughput: **3234 chars/sec**

## Results: MP3

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 53ms | 49ms | 60ms | 40.8KB |
| medium | 105 chars | 74ms | 72ms | 79ms | 139.7KB |
| long | 323 chars | 145ms | 144ms | 147ms | 406.9KB |
| numbers | 74 chars | 71ms | 68ms | 77ms | 124.3KB |
| punctuation | 69 chars | 64ms | 60ms | 70ms | 84.9KB |
| very_long | 910 chars | 315ms | 313ms | 316ms | 1051.9KB |

Avg latency: **120ms** | Throughput: **2080 chars/sec**

## Results: OPUS

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 50ms | 49ms | 52ms | 37.9KB |
| medium | 105 chars | 79ms | 76ms | 84ms | 168.1KB |
| long | 323 chars | 150ms | 148ms | 154ms | 509.0KB |
| numbers | 74 chars | 74ms | 69ms | 80ms | 147.3KB |
| punctuation | 69 chars | 65ms | 61ms | 70ms | 98.4KB |
| very_long | 910 chars | 338ms | 333ms | 342ms | 1320.3KB |

Avg latency: **126ms** | Throughput: **1990 chars/sec**

## Results: FLAC

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 23ms | 22ms | 25ms | 38.1KB |
| medium | 105 chars | 35ms | 34ms | 36ms | 163.7KB |
| long | 323 chars | 75ms | 72ms | 81ms | 502.2KB |
| numbers | 74 chars | 34ms | 34ms | 35ms | 141.7KB |
| punctuation | 69 chars | 30ms | 30ms | 30ms | 92.4KB |
| very_long | 910 chars | 183ms | 181ms | 187ms | 1284.0KB |

Avg latency: **63ms** | Throughput: **3949 chars/sec**

## Results: PCM

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 20ms | 19ms | 21ms | 93.8KB |
| medium | 105 chars | 32ms | 32ms | 33ms | 331.6KB |
| long | 323 chars | 69ms | 68ms | 70ms | 972.7KB |
| numbers | 74 chars | 33ms | 32ms | 34ms | 294.1KB |
| punctuation | 69 chars | 29ms | 28ms | 29ms | 199.2KB |
| very_long | 910 chars | 182ms | 169ms | 189ms | 2520.7KB |

Avg latency: **61ms** | Throughput: **4119 chars/sec**

## Whisper Validation Details

| Test | Similarity | Expected | Transcribed |
|------|-----------|----------|-------------|
| short | 100% | Hello, this is a test. | Hello, this is a test. |
| medium | 100% | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. |
| long | 98% | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text to speech synthesis is one of the most exciting applications, enabling natural sounding voice generation from written text. | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text-to-speech synthesis is one of the most exciting applications, enabling natural-sounding voice generation from written text. |
| numbers | 96% | There are 7 continents, 195 countries, and over 8 billion people on Earth. | There are seven continents, 195 countries, and over 8 billion people on Earth. |
| punctuation | 97% | Wait, what? Are you serious! That's incredible... I can't believe it. | Wait, what? Are you serious? That's incredible. I can't believe it. |
| very_long | 100% | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries-old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. |
