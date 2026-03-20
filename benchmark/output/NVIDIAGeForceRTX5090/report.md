# Kokoro TTS Benchmark Results

**Date:** 2026-03-20 09:41 UTC

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
| wav | 80ms | 735.4KB | 98.58% |
| mp3 | 120ms | 308.1KB | 98.58% |
| opus | 126ms | 380.0KB | 98.58% |
| flac | 63ms | 370.4KB | 98.58% |
| pcm | 60ms | 735.4KB | n/a |

## Results: WAV

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 117ms | 23ms | 306ms | 93.8KB |
| medium | 105 chars | 38ms | 33ms | 46ms | 331.7KB |
| long | 323 chars | 70ms | 65ms | 77ms | 972.7KB |
| numbers | 74 chars | 36ms | 32ms | 43ms | 294.2KB |
| punctuation | 69 chars | 34ms | 28ms | 47ms | 199.3KB |
| very_long | 910 chars | 186ms | 178ms | 199ms | 2520.7KB |

Avg latency: **80ms** | Throughput: **3121 chars/sec**

## Results: MP3

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 52ms | 48ms | 59ms | 40.8KB |
| medium | 105 chars | 75ms | 73ms | 79ms | 139.7KB |
| long | 323 chars | 143ms | 139ms | 145ms | 406.9KB |
| numbers | 74 chars | 72ms | 69ms | 77ms | 124.3KB |
| punctuation | 69 chars | 64ms | 61ms | 69ms | 84.9KB |
| very_long | 910 chars | 316ms | 312ms | 321ms | 1051.9KB |

Avg latency: **120ms** | Throughput: **2080 chars/sec**

## Results: OPUS

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 52ms | 48ms | 58ms | 37.9KB |
| medium | 105 chars | 77ms | 74ms | 82ms | 167.7KB |
| long | 323 chars | 149ms | 145ms | 154ms | 508.8KB |
| numbers | 74 chars | 75ms | 72ms | 81ms | 147.1KB |
| punctuation | 69 chars | 65ms | 61ms | 71ms | 98.1KB |
| very_long | 910 chars | 338ms | 335ms | 340ms | 1320.2KB |

Avg latency: **126ms** | Throughput: **1988 chars/sec**

## Results: FLAC

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 23ms | 22ms | 24ms | 38.2KB |
| medium | 105 chars | 34ms | 33ms | 35ms | 163.8KB |
| long | 323 chars | 73ms | 72ms | 73ms | 502.2KB |
| numbers | 74 chars | 34ms | 33ms | 35ms | 141.7KB |
| punctuation | 69 chars | 29ms | 29ms | 30ms | 92.4KB |
| very_long | 910 chars | 183ms | 177ms | 188ms | 1284.1KB |

Avg latency: **63ms** | Throughput: **3993 chars/sec**

## Results: PCM

| Test | Input Length | Avg Latency | Min | Max | File Size |
|------|-------------|-------------|-----|-----|-----------|
| short | 22 chars | 21ms | 20ms | 23ms | 93.8KB |
| medium | 105 chars | 32ms | 31ms | 33ms | 331.6KB |
| long | 323 chars | 70ms | 70ms | 70ms | 972.7KB |
| numbers | 74 chars | 32ms | 32ms | 33ms | 294.1KB |
| punctuation | 69 chars | 28ms | 27ms | 28ms | 199.2KB |
| very_long | 910 chars | 174ms | 168ms | 179ms | 2520.7KB |

Avg latency: **60ms** | Throughput: **4207 chars/sec**

## Whisper Validation Details

| Test | Similarity | Expected | Transcribed |
|------|-----------|----------|-------------|
| short | 100% | Hello, this is a test. | Hello, this is a test. |
| medium | 100% | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the English alphabet. |
| long | 98% | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text to speech synthesis is one of the most exciting applications, enabling natural sounding voice generation from written text. | Artificial intelligence has transformed the way we interact with technology. From voice assistants to self-driving cars, machine learning models are becoming an integral part of our daily lives. Text-to-speech synthesis is one of the most exciting applications, enabling natural-sounding voice generation from written text. |
| numbers | 96% | There are 7 continents, 195 countries, and over 8 billion people on Earth. | There are seven continents, 195 countries, and over 8 billion people on Earth. |
| punctuation | 97% | Wait, what? Are you serious! That's incredible... I can't believe it. | Wait, what? Are you serious? That's incredible. I can't believe it. |
| very_long | 100% | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. | In the early morning hours, the city slowly comes to life. Street vendors set up their carts along the busy avenues, while commuters rush to catch the first trains of the day. The smell of fresh coffee drifts through the air, mixing with the sound of distant traffic. Somewhere in a quiet neighborhood, a baker pulls the first loaves of bread from a centuries-old oven, continuing a tradition passed down through generations. Meanwhile, across town, a young engineer sits at her desk, reviewing lines of code that will power a new artificial intelligence system designed to help doctors diagnose rare diseases. She takes a sip of tea and smiles, knowing that her work could save thousands of lives in the years to come. Outside her window, the sun begins to rise over the skyline, casting long shadows across the rooftops and painting the clouds in shades of orange and gold. It is going to be a beautiful day. |
