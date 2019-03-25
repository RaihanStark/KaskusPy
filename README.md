# Auto Post Kaskus Bot
> Sebuah bot yang otomatis post ke thread kaskus

Ini adalah sebuah bot yang otomatis mempos ke thread di Kaskus!

![](example.gif)

## Instalasi

```
python -m pip install -r requirements.txt
```

## Cara Penggunaan

1. edit kata.txt
  Kata/kalimat yang nantinya akan digunakan untuk pos (1 kalimat/kata perbaris)
2. jalankan app.py (python app.py)

Ikuti Instruksinya

## Algoritma
- Login kedalam website menggunakan Request POST langsung ke server\n
- Setelah login berhasil, bot ini langsung mengarah ke link kategori dan mengambil semua id thread selain pinned thread menggunakan Beautiful Soup dan menyimpannya kedalam sebuah variable
- pagenumber + 1. Untuk pindah ke page selanjutnya
- Setelah selesai _Scraping_, Bot ini akan mengambil securitytoken form menggunakan Beautiful Soup sebelum request POST ke server!
- Delay 30 detik dan kembali ke poin 4 sampai akhirnya tidak ada link lagi yang harus di pos

## TODO
- Iterate to ALL Thread on each category

## Authors
* **Raihan Yudo Saputra** - *Initial Work*

### **HANYA UNTUK PEMBELAJARAN !!!**
