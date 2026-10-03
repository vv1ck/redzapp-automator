<div align="center">
  <img src="https://raw.githubusercontent.com/vv1ck/redzapp-automator/main/cat.jpg" alt="RedzApp Automator Logo" width="250" style="border-radius: 15px;">
  <br><br>
  
  <h1>🚀 RedzApp Automator</h1>
  <p><b>Advanced Account Provisioning & Engagement Automation Tool for Redz</b></p>
  
  <a href="https://github.com/vv1ck">
    <img src="https://img.shields.io/badge/Author-vv1ck-blue.svg?style=flat-square" alt="Author">
  </a>
  <a href="https://t.me/vv0ck">
    <img src="https://img.shields.io/badge/Telegram-Channel-2CA5E0.svg?style=flat-square&logo=telegram" alt="Telegram">
  </a>
  <img src="https://img.shields.io/badge/Python-3.8+-green.svg?style=flat-square&logo=python" alt="Python">
</div>

## 📌 Overview

**RedzApp Automator** is a high-performance, multi-threaded Python utility designed to automate account creation and manage engagement metrics on the Redz platform. 

The script dynamically provisions new accounts (verifying them via temporary emails), bypasses basic restrictions, and coordinates these accounts to artificially boost engagement on targeted profiles and posts. This includes driving up follower counts, post views, likes, comments, shares, and bookmarks.

## ✨ Core Features

- **Automated Account Creation:** Seamlessly generates new Redz accounts with automated email verification and session handling.
- **Dynamic Profile Customization:** Automatically assigns authentic-looking Arabic names and randomly selects elegant Islamic supplications (Adhkar/Duas) for the account bio to ensure profiles look legitimate.
- **Customizable Username Lengths:** Generate highly sought-after usernames (3-letter, 4-letter, or random 5-6 letter combinations).
- **Engagement Manipulation:** Directs the generated fleet of accounts to interact with a specific target:
  - Auto-Follow the target user.
  - Auto-Like, View, Share, Bookmark, and Comment on targeted posts or series.
- **Proxy Rotation Support:** Built-in proxy parsing and rotation to distribute requests and avoid IP-based rate limiting or blocks.
- **Multi-threading Architecture:** Utilizes Python's `threading` module to run dozens of creation and engagement instances concurrently for rapid execution.
- **Interactive CLI:** An easy-to-use command-line interface to configure targeting and settings on the fly.

## ⚙️ Prerequisites

Ensure you have Python 3.8 or higher installed. You will also need to install the required dependencies:

```bash
pip install requests user_agent httpx
```

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vv1ck/redzapp-automator.git
   cd redzapp-automator
   ```

2. **Configure Proxies:**
   The tool requires proxies to function effectively without getting flagged. 
   Create a file named `proxy.txt` in the root directory and add your proxies (one per line). The tool supports various proxy formats (e.g., `IP:Port`, `User:Pass@IP:Port`, etc.).
   ```bash
   nano proxy.txt
   ```

## 🛠️ Usage & Configuration

Upon running the tool for the first time, you **must** configure your target parameters via the built-in settings menu.

1. **Launch the script:**
   ```bash
   python redzapp.py
   ```

2. **Access Settings:** 
   From the main menu, type `2` and hit Enter to access the configuration module. 
   Here you need to define:
   - **Activate System:** Ensure this is set to `on` to enable the engagement payload.
   - **Target Username:** Enter your Redz username (the account that will receive the followers).
   - **Post URL:** Paste the exact URL of the Redz post or series you want to boost with likes, views, and comments.
   - **Username Length:** Choose the format for the generated bot accounts (Option `1` for 3 letters, `2` for 4 letters, or `3` for random 5-6 letters).

3. **Start the Engine:**
   Once configured, return to the main menu and select `1`. The script will initiate the multi-threaded sequence, create accounts, and automatically execute the engagement tasks against your configured targets.

## 📁 Output

The tool will automatically create a `redzapp_accounts` directory. It securely logs all successfully created accounts, session tokens, and device IDs into organized `.txt` files (e.g., `new_random_accounts.txt`), alongside operational logs and a `Settings.json` file for state persistence.

## 📞 Contact & Support

For updates, custom scripts, or support, join the Telegram channel:

**👉 [Telegram Channel: @vv0ck](https://t.me/vv0ck)**

---
*Disclaimer: This tool is provided for educational and research purposes only. The author is not responsible for any misuse, account bans, or violations of platform Terms of Service.*
