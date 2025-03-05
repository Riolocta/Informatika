#2.1 tulis kode untuk fungsi yang mengembalikan nilai minimum dalam array dan petunjuk indeksnya: dapatkah Anda mengadaptasi fungsi max_in_array?
def min_in_array(arr):
    if not arr:  # Memeriksa apakah array kosong
        return None, None  # Mengembalikan None jika array kosong
    min_value = arr[0]  # Menginisialisasi nilai minimum dengan elemen pertama
    min_index = 0  # Menginisialisasi indeks minimum dengan 0
    for index in range(1, len(arr)):
        if arr[index] < min_value:  # Jika elemen saat ini lebih kecil dari min_value
            min_value = arr[index]  # Memperbarui nilai minimum
            min_index = index  # Memperbarui indeks minimum
    return min_value, min_index  # Mengembalikan nilai minimum dan indeksnya
#contoh penggunaan
array = [10,20,5,7]
min_value, min_index = min_in_array(array)
print(f"Nilai minimum adalah {min_value} pada indeks {min_index}.")

#2.2bisakah Anda menulis metode yang mengembalikan nilai maks dan min sekaligus?
def min_max_in_array(arr):
    if not arr:  # Memeriksa apakah array kosong
        return None, None, None, None  # Mengembalikan None jika array kosong
    min_value = arr[0]  # Menginisialisasi nilai minimum dengan elemen pertama
    max_value = arr[0]  # Menginisialisasi nilai maksimum dengan elemen pertama
    min_index = 0  # Menginisialisasi indeks minimum dengan 0
    max_index = 0  # Menginisialisasi indeks maksimum dengan 0
    for index in range(1, len(arr)):
        if arr[index] < min_value:  # Jika elemen saat ini lebih kecil dari min_value
            min_value = arr[index]  # Memperbarui nilai minimum
            min_index = index  # Memperbarui indeks minimum
        elif arr[index] > max_value:  # Jika elemen saat ini lebih besar dari max_value
            max_value = arr[index]  # Memperbarui nilai maksimum
            max_index = index  # Memperbarui indeks maksimum
    return min_value, min_index, max_value, max_index  # Mengembalikan nilai minimum, indeks minimum, nilai maksimum, dan indeks maksimum
#contoh penggunaan 
array = [10,20,5,7]
min_value, min_index, max_value, max_index = min_max_in_array(array)
print(f"Nilai minimum adalah {min_value} pada indeks {min_index}.")
print(f"Nilai maksimum adalah {max_value} pada indeks {max_index}.")

print("apa keuntungan menghitung keduanya dalam metode yang sama?")
print("Penggunaan Memori : Dengan menghitung keduanya dalam satu fungsi, Anda dapat menghindari penggunaan memori tambahan yang mungkin diperlukan untuk menyimpan hasil dari dua fungsi terpisah")
print("Bacaan kode : Menggabungkan logika untuk mendapatkan nilai maksimum dan minimum dalam satu fungsi dapat membuat kode lebih ringkas dan lebih mudah dipahami, karena semua logika terkait berada dalam satu tempat")