#!/usr/bin/env python3
"""
Download Phi-3-mini model
"""
import os
from gpt4all import GPT4All

print("=" * 70)
print("Downloading Phi-3-mini Model")
print("=" * 70)
print("\nModel Details:")
print("  Name:  Phi-3-mini-4k-instruct.Q4_0.gguf")
print("  Size:  ~2.1 GB")  
print("  Speed: Very Fast (5-10 seconds per response)")
print("  Quality: Excellent for study/career tasks")
print("\nDownload Location:")
print(f"  {os.path.expanduser('~')}/.cache/gpt4all/")
print("\nThis may take 5-10 minutes depending on internet speed...")
print("=" * 70)

try:
    print("\n⏳ Starting download...")
    model = GPT4All("Phi-3-mini-4k-instruct.Q4_0.gguf")
    print("\n✅ SUCCESS! Phi-3-mini downloaded and ready!")
    print("\nYou can now:")
    print("  1. Run your StudyWiseAI app")
    print("  2. Use Career Counseling feature")
    print("  3. Generate action plans")
    print("  4. All responses will be fast (~5-10 seconds)")
    
except KeyboardInterrupt:
    print("\n⚠️  Download interrupted by user")
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    print("\nTroubleshooting:")
    print("  - Check your internet connection")
    print("  - Ensure you have ~5GB free disk space")
    print("  - Try again in a moment")
