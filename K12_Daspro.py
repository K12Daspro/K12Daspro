import os
import datetime
import csv
from prettytable import PrettyTable
import pwinput

fileData = 'data.csv'
keranjang = []
editFile = 1

def hapusLayar():
    os.system('cls' if os.name == 'nt' else 'clear')

def kembaliKeMenu():
    global editFile
    editFile = 1
    print("")
    input("Tekan Enter Untuk Kembali Ke Menu Utama")
    main_menu()

def login(username, password): # Fungsi untuk memeriksa apakah username dan password sesuai
    with open('users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return row['saldo_epay']
    return None

def register(username, password, saldo_epay): #Fungsi untuk membuat akun 
    with open('users.csv', mode='a', newline='') as file:
        fieldnames = ['username', 'password', 'saldo_epay']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({'username': username, 'password': password, 'saldo_epay': saldo_epay})
        hapusLayar()
        print("="*60)
        print("Terima Kasih Akun Anda Telah Terdaftar")
        print("Data Anda:")
        print({"username": username})
        print({"password": password})
        print("="*60)
        kembaliKeMenu()

def bacaSaldo(username): #Untuk membaca saldo dari file CSV
    with open('users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                saldo = float(row['saldo_epay'])
                print(f"Saldo e-pay Anda: Rp. {saldo}")
                return saldo
    print("Pengguna tidak ditemukan.")
    return None

def menu(): #dfatr menu dan menu transaksi
    global keranjang
    keranjang = []
    hargaSementara = 0
    beli = 1

    hapusLayar()
    print("=" * 32)
    print("""
    Selamat Datang di Twelve Resto
        Silahkan Pilih Menu""", "\n")
    print("=" * 32)
    menu_jualan = PrettyTable(["No Menu","Nama Menu", "Harga Menu"])
    menu_jualan.add_row(["1","Burger","Rp. 15000"])
    menu_jualan.add_row(["2","Ayam Goreng","Rp. 13000"])
    menu_jualan.add_row(["3","Cream Soup","Rp. 20000"])
    menu_jualan.add_row(["4","French Fries","Rp. 6000"])
    menu_jualan.add_row(["5","Nasi","Rp. 5000"])
    menu_jualan.add_row(["6","Air Mineral","Rp. 5000"])
    menu_jualan.add_row(["7","Ice Tea","Rp. 7000"])
    menu_jualan.add_row(["8","Orang Juice","Rp. 8000"])
    menu_jualan.add_row(["9","Milo","Rp. 10000"])
    menu_jualan.add_row(["10","Coca Cola/Sprite/Fanta","Rp. 13000"])
    print(menu_jualan)

    while beli == 1:
        current = datetime.datetime.now()
        hari = current.day
        bulan = current.month
        tahun = current.year
        tanggal = f"{hari}-{bulan}-{tahun}"

        print("")
        try:
            pilihBarang = int(input("Masukkan Nomor Menu    : "))
        except ValueError:
            print("Input Harus Berupa Angka")
            continue
        else:
            try:
                jumlahBarang = int(input("Masukkan Jumlah        : "))
            except ValueError:
                print("Input Harus Berupa Angka")
                continue
            else:
                if pilihBarang == 1:
                    namaBarang = "Burger"
                    hargaBarang = 15000
                elif pilihBarang == 2:
                    namaBarang = "Ayam Goreng"
                    hargaBarang = 13000
                elif pilihBarang == 3:
                    namaBarang = "Cream Soup"
                    hargaBarang = 20000
                elif pilihBarang == 4:
                    namaBarang = "French Fries"
                    hargaBarang = 6000
                elif pilihBarang == 5:
                    namaBarang = "Nasi"
                    hargaBarang = 5000
                elif pilihBarang == 6:
                    namaBarang = "Air Mineral"
                    hargaBarang = 5000
                elif pilihBarang == 7:
                    namaBarang = "Ice Tea"
                    hargaBarang = 7000
                elif pilihBarang == 8:
                    namaBarang = "Orange Juice"
                    hargaBarang = 8000
                elif pilihBarang == 9:
                    namaBarang = "Milo"
                    hargaBarang = 10000
                elif pilihBarang == 10:
                    namaBarang = "Coca Cola/Sprite/Fanta"
                    hargaBarang = 13000
                elif pilihBarang >= 11:
                    print("Menu Anda Tidak Ada")
                    continue
        hargaSementara = hargaBarang * jumlahBarang
        dataCSV = {'Tanggal':tanggal, 'Nama Barang':namaBarang, 'Jumlah Barang':jumlahBarang, 'Harga Satuan':hargaBarang, 'Total Harga':hargaSementara}
        keranjang.append(dataCSV)
        print(keranjang)
        print("")

        while True:
            ulang = str(input("Ada Lagi? [y/t] : "))

            if ulang == 'y':
                break
            elif ulang == 't':
                beli += 2
                if editFile == 1:
                    tulisData()
                elif editFile == 2:
                    tambahData()               
                dataSementara()
                break
            else:
                continue

def update_saldo(username, saldo): #untuk memperbaharui saldo e-pay
    with open('users.csv', mode='r') as file:
        users = list(csv.DictReader(file))

    for user in users:
        if user['username'] == username:
            user['saldo_epay'] = str(saldo)
            with open('users.csv', mode='w', newline='') as file:
                fieldnames = ['username', 'password', 'saldo_epay']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users)

def tambahKembalian(username, kembalian): #untuk mengupdate data saldo setelah melakukan transaksi
    fileData = 'users.csv'  
    dataBaru = []

    with open(fileData, 'r', newline='') as fileBaca:
        baca = csv.DictReader(fileBaca, delimiter=',')
        for data in baca:
            if data['username'] == username:
                data['saldo_epay'] = kembalian
            dataBaru.append(data)

    with open(fileData, 'w', newline='') as fileTulis:
        fieldnames = dataBaru[0].keys()
        writer = csv.DictWriter(fileTulis, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataBaru)

def cek_saldo(username): #untuk melihast saldo (user)
    with open('users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                saldo = float(row['saldo_epay'])
                print(f"Saldo e-pay {username}: Rp.{saldo}")
                return saldo
    print("Pengguna tidak ditemukan.")
    return None

def topup_saldo(username, jumlah): #untuk menambahkan saldo (admin)
    with open('users.csv', mode='r') as file:
        users = list(csv.DictReader(file))
    
    for user in users:
        if user['username'] == username:
            user['saldo_epay'] = str(float(user['saldo_epay']) + jumlah)
            with open('users.csv', mode='w', newline='') as file:
                fieldnames = ['username', 'password', 'saldo_epay']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(users)
            print(f"Saldo e-pay {username} berhasil ditambahkan sebesar {jumlah}")
            hasil = cek_saldo(username) + jumlah
            print(f"Saldo {username} sekarang adalah: {hasil}") 
            return
    print("Pengguna tidak ditemukan.")

def tulisData(): #fungsi ini untuk menulis data, dengan menghapus data sebelumnya jika ada
    try:
        listData = ['Tanggal', 'Nama Barang', 'Jumlah Barang', 'Harga Satuan', 'Total Harga']

        with open(fileData, 'w', newline='') as fileTulis:
            tulis = csv.DictWriter(fileTulis, fieldnames=listData)
            tulis.writeheader()
            tulis.writerows(keranjang)
    except IOError as e:
        print(e)

def tambahData(): #fungsi ini diågunakan untuk menulis data, dengan menambahkan data ke data yang sudah ada
    try:
        listData = ['Tanggal', 'Nama Barang', 'Jumlah Barang', 'Harga Satuan', 'Total Harga']

        with open(fileData, 'a', newline='') as fileTambah:
            tulis = csv.DictWriter(fileTambah, fieldnames=listData)
            tulis.writerows(keranjang)
    except IOError as e:
        print(e)

def hapusData(): #fungsi ini digunakan untuk menghapus salah satu data yang diinginkan pengguna
    listData = ['Tanggal', 'Nama Barang', 'Jumlah Barang', 'Harga Satuan', 'Total Harga']
    print("")
    hapus = input("Masukkan Nama Menu : ")
    daftarHapus = []
    daftarBaru = []

    try:
        with open(fileData, 'r') as fileBaca:
            baca = csv.DictReader(fileBaca, delimiter=',')
            for isi in baca:
                if isi['Nama Barang'] == hapus:
                    daftarHapus.append(hapus)
                    continue
                else:
                    daftarBaru.append(isi)
    except IOError as e:
        print(e)

    if len(daftarHapus) == 0:
        print("Menu Belum Dipesan")
    else:
        try:
            with open(fileData, 'w', newline='') as fileTulis:
                tulis = csv.DictWriter(fileTulis, fieldnames=listData)
                tulis.writeheader()
                tulis.writerows(daftarBaru)
                print("")
                print("Menu Berhasil di Hapus")
        except IOError as e:
            print(e)
        dataBaru()

def dataBaru(): #fungsi ini digunakan untuk menampilkan data sementara yang sudah diinput
    hapusLayar()

    try:
        with open(fileData, 'r') as fileBaca:
            baca = csv.DictReader(fileBaca, delimiter=',')
            
            print('-'*89)
            print(f"|\tTanggal \t Nama Barang \t Jumlah Barang \t Harga Satuan \t Total Harga \t|")
            print("-"*89) 

            for data in baca:
                print(f"|\t{data['Tanggal']} \t {data['Nama Barang']} \t {data['Jumlah Barang']} \t\t {data['Harga Satuan']} \t\t {data['Total Harga']} \t\t|")
    except IOError as e:
        print(e)
    
    admin_menu()

def editTest():
    barang = []
    with open(fileData, 'r') as fileEdit:
        baca_data = csv.DictReader(fileEdit)
        for data in baca_data:
            barang.append(data)
    
    for indeks, data in enumerate(barang, 1):
        print(f"{indeks}. Tanggal: {data['Tanggal']}, Nama Barang: {data['Nama Barang']}, Jumlah Barang: {data['Jumlah Barang']}, Harga Satuan: {data['Harga Satuan']}, Total Harga: {data['Total Harga']}")

    pilihan = int(input("Pilih nomor data yang ingin diedit: "))
    
    if 1 <= pilihan <= len(barang):
        data_ketemu = barang[pilihan - 1]
        
        # Di sini Anda dapat menambahkan logika untuk mengedit data sesuai kebutuhan Anda
        print("Data yang dipilih:", data_ketemu)
        # Misalnya, Anda dapat memungkinkan pengguna untuk mengedit jumlah, harga satuan, atau yang lainnya
        # Setelah pengeditan, Anda dapat menulis kembali data ke file CSV
        data_ketemu['Jumlah Barang'] = int(input("Masukkan jumlah yang baru: "))
        data_ketemu['Harga Satuan'] = int(input("Masukkan harga satuan yang baru: "))
        
        # Kemudian Anda bisa menulis kembali data ke file CSV
        with open(fileData, 'w', newline='') as fileTulis:
            listData = ['Tanggal', 'Nama Barang', 'Jumlah Barang', 'Harga Satuan', 'Total Harga']
            tulis = csv.DictWriter(fileTulis, fieldnames=listData)
            tulis.writeheader()
            tulis.writerows(barang)
        
        print("Data berhasil diubah!")
    else:
        print("Nomor data tidak valid.")

def editData(): #fungsi ini digunakan untuk memilih perintah untuk mengedit data
    global editFile

    print("")
    print("Ada Perubahan?")

    while True:
        edit = str(input("Tambah [t], Hapus [h], Selesai [s] : "))

        if edit == 't':
            editFile = 2
            menu()
        elif edit == 'h':
            hapusData()
        elif edit == 's':
            strukData()
            break
        else:
            continue

def dataTransaksi(): #fungsi ini digunakan untuk menampilkan data sementara yang sudah diinput
    hapusLayar()

    try:
        with open(fileData, 'r') as fileBaca:
            baca = csv.DictReader(fileBaca, delimiter=',')
            
            print('-'*89)
            print(f"|\tTanggal \t Nama Barang \t Jumlah Barang \t Harga Satuan \t Total Harga \t|")
            print("-"*89) 

            for data in baca:
                print(f"|\t{data['Tanggal']} \t {data['Nama Barang']} \t {data['Jumlah Barang']} \t\t {data['Harga Satuan']} \t\t {data['Total Harga']} \t\t|")
    except IOError as e:
        print(e)

def dataSementara(): #fungsi ini digunakan untuk menampilkan data sementara yang sudah diinput
    hapusLayar()

    try:
        with open(fileData, 'r') as fileBaca:
            baca = csv.DictReader(fileBaca, delimiter=',')
            
            print('-'*89)
            print(f"|\tTanggal \t Nama Barang \t Jumlah Barang \t Harga Satuan \t Total Harga \t|")
            print("-"*89) 

            for data in baca:
                print(f"|\t{data['Tanggal']} \t {data['Nama Barang']} \t {data['Jumlah Barang']} \t\t {data['Harga Satuan']} \t\t {data['Total Harga']} \t\t|")
    except IOError as e:
        print(e)

    editData()

def strukData(): #fungsi ini digunakan untuk menampilkan data akhir dan memproses pembayaran
    hapusLayar()
    JmlhBrg = []
    NmaBarang = []
    listTotalHarga = []
    totalHarga = 0
    try:
        with open(fileData, 'r') as fileBaca:
            baca = csv.DictReader(fileBaca, delimiter=',')
            for data in baca:
                listTotalHarga.append(int(data['Total Harga']))
                NmaBarang.append(data['Nama Barang'])
                JmlhBrg.append(data['Jumlah Barang'])
                totalHarga = sum(listTotalHarga)
            
    except IOError as e:
        print(e)

    current = datetime.datetime.now()
    hari = current.day
    bulan = current.month
    tahun = current.year
    tanggal = f"{hari}-{bulan}-{tahun}"
    
    print("------------------- Struk Pembayaran ---------------------")
    username = input("Username Pelanggan : ")
    print("Methode : Self Service")
    print("="*50)
    print(f"Tanggal Pemesanan            : {tanggal}")
    saldo = bacaSaldo(username)
    print(f"List menu yang anda pesan    : {NmaBarang}")
    print(f"List Jumlah menu             : {JmlhBrg}")
    print(f"Total Pembayaran Anda Adalah : Rp. {totalHarga}")
    kembalian = saldo - totalHarga
    update_saldo(username, saldo)
    print(f"Sisa Saldo Anda              : Rp. {kembalian}")
    tambahKembalian(username, kembalian)
    print("--------------------- Terima kasih -----------------------")
    print("Ada pertanyaan? Silahkan hubungi Customer Service (012-345-6789)")
    user_menu()

def main_menu():
    while True:
        hapusLayar()
        print("=" * 32)
        print("Selamat Datang di Twelve Resto")
        print("1. Log In Sebagai Admin")
        print("2. Log In Sebagai Customer")
        print("3. Register")
        print("4. Exit")
        print("=" * 32)

        choice = input("Pilih opsi: ")

        if choice == '1':
            username = input("Masukkan username: ")
            password = pwinput.pwinput("Masukkan password: ", mask='X')
            if login(username, password):
                admin_menu()
            else:
                print("Login as admin failed.")
        elif choice == '2':
            username = input("Masukkan username: ")
            password = pwinput.pwinput("Masukkan password: ", mask='X')
            if login(username, password):
                user_menu()
            else:
                print("Login as customer failed.")
        elif choice == '3':
            username = input("Masukkan Username Baru: ")
            password = pwinput.pwinput("Masukkan password: ", mask='X')
            try:
                saldo_epay = int(input("Masukkan jumlah uang anda: "))
            except ValueError:
                print("Anda Tidak Boleh Bukan Angka")
            else:
                if saldo_epay == "":
                    print("Anda Tidak Boleh Kosong")
                elif saldo_epay < 0:
                    print("Saldo Tidak Boleh Mines")
                else:
                    register(username, password, saldo_epay)
        elif choice == '4':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def user_menu():
    while True:
            print("=" * 32)
            print("Selamat Datang, User")
            print("1. Cek Saldo")
            print("2. Pesan Menu Makanan dan Minuman")
            print("3. Kembali ke Menu Utama")
            print("=" * 32)

            choice = input("Pilih opsi: ")

            if choice == '1':
                username = input("Masukkan Nama Pengguna: ")
                cek_saldo(username)
            elif choice == '2':
                menu()
            elif choice == '3':
                break
            else:
                print("Pilihan yang anda masukkan tidak valid")

def admin_menu():
    hapusLayar()
    while True:
        print("=" * 32)
        print("Selamat Datang, Admin")
        print("1. Lihat Data Transaksi")
        print("2. Hapus Data Transaksi")
        print("3. Edit Data Transaksi")
        print("4. Top Up Saldo Pengguna")
        print("5. Kembali ke Main Menu")
        print("=" * 32)

        choice = input("Pilih opsi: ")

        if choice == '1':
            dataTransaksi()
        elif choice == '2':
            hapusData()
        elif choice == '3':
            editTest()
        elif choice == '4':
                username = input("Masukkan nama pengguna: ")
                try:
                    jumlah = int(input("Masukkan jumlah top-up: "))
                except ValueError:
                    print("Harus Berupa Angka")
                    continue
                else:
                    topup_saldo(username, jumlah)
        elif choice == '5':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

main_menu()
