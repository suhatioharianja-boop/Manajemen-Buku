"""
SISTEM MANAJEMEN DATA BUKU - VERSI TERMINAL
Cara menjalankan: python main.py

Program ini menggunakan:
- Class Buku dan Perpustakaan
- Linear Search untuk pencarian
- Bubble Sort untuk pengurutan
- JSON untuk penyimpanan permanen
- *args, **kwargs, lambda, try-except, raise, dan assert
"""

import json
from pathlib import Path

FILE_DATA = Path(__file__).parent / "data.json"


class Buku:
    """Menyimpan informasi satu buku."""

    def __init__(self, id_buku, judul, kategori, harga):
        if not id_buku.strip() or not judul.strip() or not kategori.strip():
            raise ValueError("ID, judul, dan kategori wajib diisi.")

        harga = float(harga)
        assert harga >= 0, "Harga tidak boleh negatif."

        self.id = id_buku.strip()
        self.judul = judul.strip()
        self.kategori = kategori.strip()
        self.harga = harga

    def ke_dictionary(self):
        """Mengubah objek buku menjadi dictionary untuk disimpan ke JSON."""
        return {
            "id": self.id,
            "judul": self.judul,
            "kategori": self.kategori,
            "harga": self.harga
        }


class Perpustakaan:
    """Mengelola data, pencarian, pengurutan, dan penyimpanan buku."""

    def __init__(self):
        self.data = self.muat_data()

    def muat_data(self):
        """Membaca data dari JSON. File hilang/rusak ditangani tanpa crash."""
        try:
            with open(FILE_DATA, "r", encoding="utf-8") as file:
                hasil = json.load(file)
                if not isinstance(hasil, list):
                    raise ValueError("Format data harus berupa list.")
                return hasil
        except FileNotFoundError:
            print("File data.json belum ditemukan. Data dimulai dari kosong.")
            return []
        except (json.JSONDecodeError, ValueError) as error:
            print(f"Data tidak dapat dibaca ({error}). Data dimulai dari kosong.")
            return []

    def simpan_data(self):
        """Menyimpan data terbaru ke file JSON secara permanen."""
        with open(FILE_DATA, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def tambah_buku(self, buku):
        """Menambahkan buku dan memastikan ID tidak duplikat."""
        if any(item["id"].lower() == buku.id.lower() for item in self.data):
            raise ValueError("ID buku sudah digunakan.")
        self.data.append(buku.ke_dictionary())
        self.simpan_data()
        print("Buku berhasil ditambahkan.")

    def tampilkan_buku(self, daftar=None):
        """Menampilkan data dalam bentuk tabel teks."""
        daftar = self.data if daftar is None else daftar

        if not daftar:
            print("\nBelum ada data buku.")
            return

        print("\n" + "-" * 83)
        print(f"{'ID':<10} {'JUDUL':<28} {'KATEGORI':<20} {'HARGA':>15}")
        print("-" * 83)
        for buku in daftar:
            print(
                f"{buku['id']:<10} "
                f"{buku['judul'][:27]:<28} "
                f"{buku['kategori'][:19]:<20} "
                f"Rp{buku['harga']:>12,.0f}"
            )
        print("-" * 83)
        print(f"Jumlah buku: {len(daftar)}")

    def cari_buku(self, kata_kunci):
        """Linear Search: mencari kata kunci pada ID, judul, atau kategori."""
        hasil = []
        kata_kunci = kata_kunci.lower()

        for buku in self.data:
            teks = buku["id"] + buku["judul"] + buku["kategori"]
            if kata_kunci in teks.lower():
                hasil.append(buku)

        return hasil

    def urutkan_buku(self, kolom="judul"):
        """Bubble Sort: mengurutkan data berdasarkan judul atau harga."""
        if kolom not in ("judul", "harga"):
            raise ValueError("Pilihan pengurutan tidak tersedia.")

        hasil = self.data.copy()
        jumlah = len(hasil)

        for i in range(jumlah):
            for j in range(0, jumlah - i - 1):
                kiri = hasil[j][kolom]
                kanan = hasil[j + 1][kolom]

                # Lambda digunakan untuk menentukan kunci perbandingan teks.
                if kolom == "judul":
                    tukar = (lambda a, b: a.lower() > b.lower())(kiri, kanan)
                else:
                    tukar = kiri > kanan

                if tukar:
                    hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]

        return hasil

    def hapus_buku(self, id_buku):
        """Menghapus buku berdasarkan ID."""
        jumlah_awal = len(self.data)
        self.data = [
            buku for buku in self.data
            if buku["id"].lower() != id_buku.lower()
        ]

        if len(self.data) == jumlah_awal:
            print("Buku dengan ID tersebut tidak ditemukan.")
        else:
            self.simpan_data()
            print("Buku berhasil dihapus.")

    def hitung_total_harga(self, *daftar_harga):
        """Contoh penggunaan *args untuk menghitung total harga."""
        return sum(daftar_harga)

    def filter_buku(self, **kriteria):
        """Contoh penggunaan **kwargs untuk filter berdasarkan kolom."""
        hasil = self.data
        for kolom, nilai in kriteria.items():
            hasil = list(filter(
                lambda buku: str(buku.get(kolom, "")).lower() == str(nilai).lower(),
                hasil
            ))
        return hasil


def tampilkan_menu():
    """Menampilkan pilihan menu aplikasi."""
    print("\n========== SISTEM MANAJEMEN BUKU ==========")
    print("1. Tampilkan semua buku")
    print("2. Tambah buku")
    print("3. Cari buku")
    print("4. Urutkan buku")
    print("5. Hapus buku")
    print("6. Hitung total harga semua buku")
    print("0. Keluar")
    print("===========================================")


def main():
    """Fungsi utama untuk menjalankan menu terminal."""
    aplikasi = Perpustakaan()

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                aplikasi.tampilkan_buku()

            elif pilihan == "2":
                print("\n--- Tambah Buku ---")
                id_buku = input("ID buku     : ")
                judul = input("Judul       : ")
                kategori = input("Kategori    : ")
                harga = input("Harga       : Rp")

                buku = Buku(id_buku, judul, kategori, harga)
                aplikasi.tambah_buku(buku)

            elif pilihan == "3":
                keyword = input("Masukkan ID/judul/kategori yang dicari: ")
                hasil = aplikasi.cari_buku(keyword)
                aplikasi.tampilkan_buku(hasil)

            elif pilihan == "4":
                print("1. Urutkan berdasarkan judul")
                print("2. Urutkan berdasarkan harga")
                urutan = input("Pilih: ").strip()

                if urutan == "1":
                    kolom = "judul"
                elif urutan == "2":
                    kolom = "harga"
                else:
                    print("Pilihan tidak valid.")
                    continue

                aplikasi.tampilkan_buku(aplikasi.urutkan_buku(kolom))

            elif pilihan == "5":
                id_buku = input("Masukkan ID buku yang ingin dihapus: ")
                aplikasi.hapus_buku(id_buku)

            elif pilihan == "6":
                total = aplikasi.hitung_total_harga(
                    *(buku["harga"] for buku in aplikasi.data)
                )
                print(f"Total harga seluruh buku: Rp{total:,.0f}")

            elif pilihan == "0":
                print("Terima kasih. Data sudah tersimpan.")
                break

            else:
                print("Menu tidak tersedia. Silakan pilih kembali.")

        except (ValueError, AssertionError) as error:
            print(f"Terjadi kesalahan: {error}")
        except (OSError, TypeError) as error:
            print(f"Terjadi kesalahan saat memproses file/data: {error}")


if __name__ == "__main__":
    main()
