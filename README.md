# 🎮 SOLID PENUH RATMAN.STORE BOT

Bot Discord All-in-One untuk toko Robux & Gamepass dengan fitur lengkap!

## ✨ FITUR LENGKAP

### 🛒 Store System
- Shop Robux/Gamepass/Items
- Auto order channel dengan button
- Stock management otomatis
- Order tracking lengkap
- Revenue counter

### 🛡️ Auto Moderation
- ✅ Delete bad words → Auto DM warning
- ✅ Delete links → Auto DM warning
- ✅ **Allow GIF links** (tenor, giphy, imgur)
- ✅ **Allow Discord Gift links** (discord.gift/)
- Warning system lengkap
- Auto log semua pelanggaran

### 👑 Moderator Commands
- `/kick` - Kick member
- `/ban` - Ban member
- `/timeout` - Timeout member
- `/warn` - Warn member
- `/clear` - Clear messages
- `/warnings` - Check warnings

### 🎁 Giveaway System
- `/giveaway` - Create giveaway
- Auto pick winners
- `/reroll` - Reroll winner
- DM notification ke pemenang

### 🎮 Fun Commands
- `/ping` - Check latency
- `/roll` - Roll dice
- `/coinflip` - Flip coin
- `/8ball` - Magic 8ball
- `/serverinfo` - Server info
- `/userinfo` - User info

### 🎵 Music Bot
- `/play` - Play music (Coming soon!)
- `/stop` - Stop music (Coming soon!)
- Full queue system (Coming soon!)

## 🚀 SETUP LEWAT GITHUB

### 1. Fork Repository Ini

Klik tombol **"Fork"** di kanan atas!

### 2. Deploy ke Leonodes

Di Leonodes panel:
1. Tab **"Startup"**
2. Cari **"Github Repository"**
3. Paste: `https://github.com/YOUR_USERNAME/solid-ratman-bot`
4. **Start** bot!

### 3. Setup di Discord

```
/setup order_channel:#pesanan admin_role:@Admin
```

### 4. Tambah Produk

```
/addproduct 
name: 100 Robux
category: robux
price: 15000
stock: 50
description: Instant delivery!
```

### 5. Test!

```
/shop
```

## 📋 COMMANDS LENGKAP

### Everyone
- `/shop` - Lihat & beli produk
- `/myorders` - Cek status order
- `/ping` - Check bot
- `/roll` `/coinflip` `/8ball` - Fun commands
- `/serverinfo` `/userinfo` - Info commands
- `/help` - Show all commands

### Moderator
- `/kick` `/ban` `/timeout` - Member management
- `/warn` `/warnings` - Warning system
- `/clear` - Clear messages

### Admin
- `/setup` - Setup bot
- `/addproduct` - Add product
- `/updatestock` - Update stock
- `/giveaway` - Create giveaway
- `/reroll` - Reroll winner

## 🛡️ AUTO MOD RULES

### ❌ Yang Dihapus & DM Warning:
- Bad words (anjing, kontol, dll)
- Semua link (http://, discord.gg/, dll)

### ✅ Yang Dibolehkan:
- GIF links (tenor.com, giphy.com, gfycat.com, imgur.com)
- Discord gift links (discord.gift/, discord.com/gifts/)
- Pesan normal

### 💬 DM Warning:
Bot otomatis kirim DM ke user yang melanggar dengan pesan ramah:
- **Bad word:** "Jangan berkata kasar ya! 😊"
- **Link:** "Jangan kirim link ya! Hubungi admin jika perlu."

## 🎁 GIVEAWAY TUTORIAL

### Create Giveaway:
```
/giveaway duration:60 winners:3 prize:100 Robux
```

- Duration = menit
- Winners = jumlah pemenang
- Prize = hadiah

### Auto Features:
- Bot add reaction 🎉
- Members react untuk join
- Auto pick winners pas waktu habis
- DM winners otomatis

### Reroll:
```
/reroll message_id:123456789
```

## 📊 DATA FILES

Bot otomatis create files ini:
- `products.json` - Produk & stock
- `orders.json` - Semua pesanan
- `warnings.json` - Warning history
- `giveaways.json` - Giveaway data
- `config.json` - Bot settings

## 🔧 TROUBLESHOOTING

### Bot offline?
```bash
cd /home/container
python main.py
```

### Commands gak muncul?
Tunggu 5-10 menit, Discord sync lama.

### Auto mod gak jalan?
```
/modtoggle
```
Pastikan enabled!

## 💡 TIPS

### Bad Words Custom:
```
/addbadword word:kata_baru
```

### Disable Mod Sementara:
```
/modtoggle
```

### Backup Data:
```bash
cp *.json backup/
```

## 📝 TODO / Coming Soon

- [ ] Full music bot integration
- [ ] Leveling system
- [ ] Custom roles
- [ ] Ticket system
- [ ] Economy system

## 🎉 SELESAI!

Bot siap pakai! Tinggal:
1. Fork repo
2. Deploy ke Leonodes
3. Setup di Discord
4. Mulai jualan! 💰

---

**Dibuat untuk:** Solid Penuh Ratman.Store
**Bot Type:** All-in-One
**Version:** 1.0.0

💬 **Support:** Contact owner
🌐 **Website:** Coming soon!
