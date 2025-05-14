# Discord-Token-Extractor

> **⚠ EDUCATIONAL USE ONLY**
> This script is intended for **educational, testing, and awareness purposes only.
> Misuse of this code for unauthorized access or malicious activity is illegal. The author is not responsible for any misuse or damages caused by this code.
> Always use in controlled environments and with explicit permission.**

---

## 🎯 Description

`token-grab.py` is a **Discord token extractor and validator** for educational purposes.

It demonstrates how Discord tokens are stored locally, how attackers may attempt to extract them, and how tokens can be verified by querying Discord's API.

The script also formats the information into Discord webhook embeds for reporting purposes.

---

## 🚀 Features

* Extracts tokens from:

  * Discord Stable
  * Discord PTB
  * Discord Canary
* Supports:

  * **Plaintext token format**
  * **Encrypted tokens using AES-GCM with local state key**
* Checks token validity via the Discord API.
* Retrieves user info (username, email, phone, Nitro status, etc.).
* Sends clean embeds to your Discord webhook.

  * Green embed for valid tokens.
  * Red embed for invalid/expired tokens.
* Labels which app the token was found in.

---

## 🛡 Educational Purpose

This project helps to:

* Understand Discord token storage.
* Learn about token encryption on Windows.
* Explore how malicious actors might abuse local data.
* Encourage better endpoint and browser security practices.

---

## ⚙ Requirements

```bash
pip install pycryptodome pypiwin32
```

---

## 🔧 Usage

1. **Replace the webhook URL** in the script:

```python
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_HERE"
```

2. **Run the script**:

```bash
python token-grab.py
```

3. **Results** will appear both in the console and as embeds in your Discord channel.

---

## 📜 Legal & Ethical Reminder

This code is shared for awareness and research ONLY.
Unauthorized token harvesting and account access are **illegal under computer misuse laws**.

Use responsibly:

* On your own machine.
* For your own accounts.
* With explicit permission.

---

## 🖼 Example Output

| Status    | Description                         |
| --------- | ----------------------------------- |
| ✅ Valid   | Full user info in a green embed     |
| ❌ Invalid | Token shown in red with source path |

---

## 📝 License

MIT License
