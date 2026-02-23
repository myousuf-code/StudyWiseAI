#!/usr/bin/env python3
"""
Download Orca-Mini model
"""
import os
from gpt4all import GPT4All

print("=" * 70)
print("Downloading Orca-Mini Model")
print("=" * 70)
print("\nModel Details:")
print("  Name:  orca-mini-3b-gguf2-q4_0.gguf")
print("  Size:  ~2.0 GB")  
print("  Speed: Fast (more stable than Phi-3)")
print("  Quality: Good for study/career tasks")
print("\nDownload Location:")
print(f"  {os.path.expanduser('~')}/.cache/gpt4all/")
print("\nThis may take 5-10 minutes depending on internet speed...")
print("=" * 70)

try:
    print("\n⏳ Starting download...")
    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
    print("\n✅ SUCCESS! Orca-Mini downloaded and ready!")
    print("\nYou can now:")
    print("  1. Run your StudyWiseAI app")
    print("  2. Use Career Counseling feature")
    print("  3. Generate action plans")
    print("  4. All responses will be fast and stable")
    
except KeyboardInterrupt:
    print("\n⚠️  Download interrupted by user")
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    print("\nTroubleshooting:")
    print("  - Check your internet connection")
    print("  - Ensure you have ~3GB free disk space")
    print("  - Try again in a moment")
