import datetime, os, shutil, json, time

def print_center(teks, prt=True):
    if prt == True:
        [print(str(tek).center(shutil.get_terminal_size().columns)) for tek in teks.split("\n")]
    elif prt == False:
        return str(teks).center(shutil.get_terminal_size().columns)


def tambah():
    global menus
    global harga_menus
    global daftar_pesanan
    while True:
        menu_pesanan = int(input("masukan menu pesanan (nomor menu) : "))
        if menu_pesanan > len(menus):
            print_center("=====Menu tidak tersedia, silahkan pilih menu lainnya!!=====")
            continue
        else:
            nama_makanan = menus[menu_pesanan-1]
            harga = harga_menus[menu_pesanan-1]
            if nama_makanan not in daftar_pesanan.keys():
                daftar_pesanan[nama_makanan] = 1
            else:
                daftar_pesanan[nama_makanan] += 1
            return nama_makanan, int(harga)

def kurang(jumlah_harga):
    global daftar_pesanan
    global menus
    global harga_menus
    [print(f"{makanan} jumlah ({jumlah})") for makanan, jumlah in daftar_pesanan.items()]
    while True:
        jenis = int(input(f'Makanan apa yang ingin dikurangi? (1-{len(daftar_pesanan)})\t:'))
        if jenis > len(daftar_pesanan.values()) and jenis <= 0 : print_center('Masukkan sesuai daftar makanan mu!!')
        else:
            pesanan = list(daftar_pesanan.keys())[jenis-1]
            if daftar_pesanan[pesanan] <= 1:
                del daftar_pesanan[pesanan]
            else:
                daftar_pesanan[pesanan] -= 1
            return jumlah_harga - int(harga_menus[menus.index(pesanan)])


def cetak(nama, jumlah_harga: int):
    global date
        # import file pesanan.json
    if not os.path.exists('pesanan.json'):
        data = {}
    else:
        file = open('pesanan.json').read()
        try: data = json.loads(file)
        except json.JSONDecodeError: data = {}
    if not os.path.exists('result'): os.mkdir("result")
    ts = int(date.timestamp())
    tanggal = date.date()
    namafile = str(ts)+'_'+str(nama)+'.json'
    try:
        info = data[f'{tanggal.year}-{tanggal.month}-{tanggal.day}']
        info.append({'nama': nama, 'time': ts, 'path': namafile})
    except:
        info = [{'nama': nama, 'time': ts, 'path': namafile}]
    data[f'{tanggal.year}-{tanggal.month}-{tanggal.day}'] = info
    js = (json.dumps(data, indent = 4))
    open('pesanan.json', 'w+').write(js)
    return data, cetakPesanan(nama, namafile, jumlah_harga)


def cetakPesanan(nama, namafile, jumlah_harga):
    global menus
    global harga_menus
    global daftar_pesanan
    pesanan = []
    data = {}
    for k in list(daftar_pesanan.keys()):
        pesanan.append({'makanan': k, "harga": harga_menus[menus.index(k)], "jumlah pembelian": daftar_pesanan[k]})
    data['nama'] = nama
    data['pesanan'] = pesanan
    data['total'] = jumlah_harga
    file = open('result/'+namafile, 'w+').write(json.dumps(data, indent=4))
    return data



def hapus(nama: str):
    if not os.path.exists("pesanan.json"):
        print("you don't have file (pesanan.json), please input user first")
        return
    nama = nama.lower()
    datas = json.loads(open('pesanan.json').read())
        # delete file
    for k,v in datas.items():
        catch = []
        for value in v:
            if nama == list(value.values())[0].strip():
                print("ada "+str(value))
                try:
                    os.remove(f"result/{list(value.values())[2]}")
                except: pass
            else: catch.append(v[v.index(value)])
        datas[k] = catch
    open("pesanan.json", "w+").write(json.dumps(datas, indent=4))



def main():
    global date
    kurangs = False
    while True:
        if kurangs != True:
            nama_makanan, harga = tambah()
            jumlah_pembelian = int(input("masukan jumlah pembelian : "))
            daftar_pesanan[nama_makanan] += jumlah_pembelian-1
            try: jumlah_harga = jumlah_harga+(harga*jumlah_pembelian)
            except: jumlah_harga = harga*jumlah_pembelian
        jawab = input("apakah ada yang ingin di tambah/dikurangi? tambah/kurang/tidak? ")
        if jawab == 'tidak':
            break
        elif jawab == 'tambah':
            kurangs = False
            continue
        elif jawab == 'kurang':
            kurangs = True
            jumlah_harga = kurang(jumlah_harga)
    data1, data2 = cetak(nama, jumlah_harga)
    os.system('cls' if os.name=='nt' else 'clear')
    print_center(f'Informasi Pembelian Milik {nama}')
    for no, pesan in enumerate(data2['pesanan']):
        print(f'{no}.\tmakanan ({pesan["makanan"]})\n\tharga ({pesan["harga"]})\n\tjumlah pembelian ({pesan["jumlah pembelian"]})\n')
    print_center(f"Total Pembayaran : {jumlah_harga}")
    print_center(f'Struk untuk {nama} berhasil dicetak\n\npress any to continue!\n')
    input("")







while True:
    os.system('cls' if os.name=='nt' else 'clear')
    print_center("Main Menu\n\n1. Delete file user\n2. Input data user\n3. Exit")
    try: choose = int(input("choose one >> "))
    except:
        print_center("enter the correct choice!")
        time.sleep(2)
        continue
    if choose == 1:
        nama = input("input user name to delete (all files) > ")
        hapus(nama)
        input(f"delete files from user ({nama}) success\n\npress any to continue!\n")
    elif choose == 2:
        print_center("         WARUNG GERI                \n"+"="*52)
        nama = input(f"\tNama Pelanggan : ").strip()
        nama = 'noname' if nama == '' else nama.lower()
        date = datetime.datetime.now()
        no = 0
        menus = ['nasi ayam', 'nasi bebek', 'nasi babat', 'nasi campur', 'nasi kikil']
        harga_menus = ['10000', '15000', '20000', '15000', "25000"]
        daftar_pesanan = {}
        print_center("="*52+"\n"+"__________MENU__________")
        for menu in menus:
            no += 1
            print(f'\t{no}. {menu}\t\t Rp.{harga_menus[no-1]}')
        print_center("__________MENU__________")
        main()
    elif choose == 3:
        exit("goodbye :)")
    else:
        print_center("enter the correct choice!")
        time.sleep(2)
        continue

exit()
print_center("         WARUNG GERI                \n"+"="*52)
nama = input(f"\tNama Pelanggan : ").strip()
nama = 'noname' if nama == '' else nama
nama = nama.lower()
date = datetime.datetime.now()
no = 0
menus = ['nasi ayam', 'nasi bebek', 'nasi babat', 'nasi campur', 'nasi kikil']
harga_menus = ['10000', '15000', '20000', '15000', "25000"]
daftar_pesanan = {}
print_center("="*52+"\n"+"__________MENU__________")
for menu in menus:
    no += 1
    print(f'\t{no}. {menu}\t\t Rp.{harga_menus[no-1]}')
print_center("__________MENU__________")

