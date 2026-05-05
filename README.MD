# ⚡ MYTHOS — The Epic of Olympus

> *A great storm broke over Olympus. The gods were summoned to the arena.*
> *Who shall rule? Who shall fall? The epic is being written now...*

```
  ╔══════════════════════════════════════════════════╗
  ║     ⚡  MYTHOS — THE EPIC OF OLYMPUS  ⚡          ║
  ║   A multiplayer terminal battle game in Python   ║
  ╚══════════════════════════════════════════════════╝
```

Mythos, **2–6 oyuncunun** TCP soketleri üzerinden bağlanıp Yunan tanrılarını seçerek **sıra tabanlı bir ölüm dövüşüne** girdiği, terminalde çalışan çok oyunculu bir Python oyunudur. Her tanrının kendine özgü pasif yetenekleri, özel güçleri ve hikâye anlatı şablonları vardır. Her hamle, Olimpos'un destanına işlenmektedir.

---

## 🗂️ İçindekiler

- [Özellikler](#-özellikler)
- [Tanrılar](#-tanrılar)
- [Durum Etkileri](#-durum-etkileri)
- [Olimpos Olayları](#%EF%B8%8F-olimpos-olayları)
- [Kurulum](#-kurulum)
- [Nasıl Oynanır](#-nasıl-oynanır)
- [Teknik Mimari](#%EF%B8%8F-teknik-mimari)
- [Dosya Yapısı](#-dosya-yapısı)

---

## ✨ Özellikler

- 🧵 **Çok oyunculu** — 2 ile 6 oyuncu arasında, TCP soketleri üzerinden gerçek zamanlı
- ⚡ **12 benzersiz tanrı** — Her birinin kendine özgü HP/ATK/DEF değerleri, özel gücü ve pasif yeteneği
- 🔥 **6 durum etkisi** — Burn, Frozen, Blessed, Cursed, Poisoned, Enraged
- 🌩️ **Olimpos Olayları** — Her turda %15 ihtimalle devreye giren rastgele ilahi müdahaleler
- 📜 **Destanlar ve Mezar Yazıtları** — Her oyunun sonunda tüm savaş olaylarından otomatik oluşturulan "Olimpos Destanı" ve her oyuncuya özel unvan + istatistik ekranı
- 🎨 **Renkli terminal arayüzü** — `colorama` ile ANSI renkler, semboller ve emoji'lerle bezenmiş tam renkli bir terminal deneyimi
- ⏱️ **30 saniyelik hamle süresi** — Süre aşımında otomatik olarak "Savun" hamlesi seçilir

---

## ⚔️ Tanrılar

| # | Tanrı | Sembol | HP | ATK | DEF | Özel Güç | Pasif |
|---|-------|--------|-----|-----|-----|-----------|-------|
| 1 | Zeus | ⚡ | 100 | 30 | 15 | Lightning Storm | Storm Aura — %20 ihtimalle hasarı geri yansıtır |
| 2 | Poseidon | 🌊 | 110 | 25 | 20 | Tsunami | Tide Pull — Her tur başında +5 HP |
| 3 | Athena | 🦉 | 90 | 20 | 35 | Shield of Wisdom | Tactical Mind — Savunma hamlesi +5 ek HP |
| 4 | Ares | ⚔️ | 120 | 38 | 8 | Blood Frenzy | Bloodlust — Her öldürme sonrası kalıcı +3 ATK |
| 5 | Hermes | 🪶 | 85 | 28 | 15 | Divine Speed | Quicksilver — %30 dodge şansı |
| 6 | Hades | 💀 | 130 | 28 | 22 | Soul Drain | Undying — Oyun başına bir kez ölümden 1 HP ile döner |
| 7 | Apollo | 🌞 | 95 | 26 | 18 | Solar Flare | Healer's Touch — İttifak hamlesi 20 HP iyileştirir |
| 8 | Artemis | 🌙 | 88 | 32 | 14 | Moonshot | Hunter's Focus — Her turda ilk saldırı maksimum hasarla çarpar |
| 9 | Aphrodite | 💖 | 80 | 18 | 20 | Enthrall | Charm Aura — %25 ihtimalle saldırganı büyüleyip saldırıyı iptal eder |
| 10 | Hephaestus | 🔨 | 115 | 24 | 28 | Forge Blast | Iron Skin — Tüm gelen hasarları 5 azaltır |
| 11 | Dionysus | 🍇 | 92 | 22 | 16 | Divine Madness | Chaos Brew — Her tur ±15 HP/ATK rastgele değişir |
| 12 | Persephone | 🌸 | 98 | 24 | 22 | Bloom & Wither | Seasonal Shift — Çift turlarda +ATK, tek turlarda +DEF |

---

## 🔥 Durum Etkileri

| Etki | Emoji | Açıklama |
|------|-------|----------|
| `burn` | 🔥 | Her tur -8 HP |
| `frozen` | ❄️ | Bir sonraki turu kaybettirir |
| `blessed` | ✨ | Bu turda +10 ATK |
| `cursed` | 🌑 | -10 DEF |
| `poisoned` | ☠️ | Her tur -5 HP |
| `enraged` | 😡 | +15 ATK, -15 DEF |

Aynı etki birden fazla kez uygulanamaz; yalnızca süresi uzar.

---

## ⛈️ Olimpos Olayları

Her tur başında **%15 ihtimalle** ilahi bir olay tetiklenir:

| Olay | Etki |
|------|------|
| ⚡ Zeus'un yıldırımı | Tüm tanrılar 10 hasar alır |
| 💚 Hera'nın lütfu | Tüm tanrılar 15 HP kazanır |
| 🔀 Kader'in müdahalesi | Tur sırası karıştırılır |
| 🔥 Prometheus'un hediyesi | Aktif oyuncu `blessed` kazanır |
| ☠️ Pandora'nın kutusu | Rastgele bir oyuncu `poisoned` olur |
| 🌬️ İlahi rüzgar | Tüm durum etkileri temizlenir |
| 🌟 Kahin'in sözü | En düşük HP'li tanrı 20 HP kazanır |
| 😡 Ares'in arenası | Tüm tanrılar 1 tur `enraged` olur |

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- `colorama` kütüphanesi

### Adımlar

```bash
# Repoyu klonla
git clone https://github.com/ozgemelteminan/olympus-arena.git
cd olympus-arena

# Bağımlılıkları yükle
pip install colorama

# Sunucuyu başlat
python server.py
```

Ayrı terminal pencerelerinde her oyuncu için:

```bash
python client.py
```

> Varsayılan olarak sunucu `127.0.0.1:5555` adresinde çalışır.  
> Ağ üzerinden oynamak için `server.py` ve `client.py` içindeki `HOST` değerini sunucu IP'siyle değiştirin.

---

## 🕹️ Nasıl Oynanır

### Bağlantı ve Tanrı Seçimi

1. `python client.py` ile sunucuya bağlan
2. Kullanıcı adını gir
3. Listeden bir tanrı seç (1-12)
4. İkinci oyuncu bağlandığında oyun otomatik başlar

### Hamle Sistemi

Her tur, sırayla her oyuncudan hamle beklenir:

```
  [1] Attack      — Hedef seç, normal saldırı yap
  [2] Defend      — Savun ve 10-20 HP iyileştir
  [3] Alliance    — Bir müttefik seç, ikiniz de 10 HP kazan
  [4] Special     — Özel gücünü kullan (tüm düşmanlara 18-28 hasar)
  [5] Steal HP    — Hedeften 10-20 HP çal
```

**Hamle formatı:** `<hamle> <hedef>` — örneğin `1 2` (2. oyuncuya saldır), `2` (savun)

### Oyun Sonu

Son hayatta kalan tanrı Olimpos'un hâkimi olur. Oyun bitiminde:

- 🏆 **Kazanan ilanı**
- 📜 **The Epic of Olympus** — tüm savaş olaylarının destanı
- 🪦 **Kişisel Mezar Yazıtları** — her oyuncunun istatistikleri ve kazandığı unvan

Örnek unvanlar: `"The Godslayer"`, `"Herald of Peace"`, `"The Untouchable"`, `"Ruler of Olympus"`

---

## 🏛️ Teknik Mimari

```
┌─────────────┐        TCP/5555        ┌──────────────────────┐
│  client.py  │ ◄──────────────────── │     server.py        │
│             │                        │                      │
│  - Gönder   │ ──────────────────────►│  handle_client()     │
│  - Al/Göster│                        │  game_loop()         │
└─────────────┘                        │  process_move()      │
                                        │  tick_status()       │
┌─────────────┐        TCP/5555        │  trigger_olympus_    │
│  client.py  │ ◄──────────────────── │    event()           │
│  (oyuncu 2) │ ──────────────────────►│                      │
└─────────────┘                        │  GameState (paylaşımlı│
                                        │  threading.Lock ile) │
     ...                                └──────────────────────┘
```

- **Sunucu** her client bağlantısı için ayrı bir thread açar (`threading.Thread`)
- **Oyun durumu** tek bir `GameState` nesnesiyle yönetilir ve `threading.Lock` ile thread-safe tutulur
- **Hamle sırası** `turn_order` listesiyle takip edilir; elenen oyuncular listeden çıkarılır
- **Yayın** tüm mesajlar `broadcast_all()` ile tüm bağlı oyunculara aynı anda gönderilir
- **Input timeout** — 30 saniye içinde hamle gönderilmezse sunucu otomatik `"2"` (savun) seçer

### Kullanılan Modüller

| Modül | Amaç |
|-------|-------|
| `socket` | TCP bağlantı yönetimi |
| `threading` | Her client için ayrı thread, `Lock` ile senkronizasyon |
| `random` | Hasar hesaplama, olay seçimi, şablon seçimi |
| `time` | Tur arası bekleme (`sleep`) |
| `colorama` | ANSI renk kodları (Windows uyumlu) |

---

## 📁 Dosya Yapısı

```
olympus-arena/
├── server.py      # Oyun mantığı, sunucu, tüm sistem burada
└── client.py      # Basit terminal istemcisi — gönder/al
```

---


Bu proje **CMPE322 — Computer Networks** dersi kapsamında geliştirilmiştir.  
Temel ağ kavramlarını (TCP soketleri, istemci-sunucu mimarisi, thread yönetimi) oyun tasarımıyla birleştiren bir dönem projesidir.

---

<div align="center">

*⚡ Olympus will remember you all forever. 🏛️*

</div>