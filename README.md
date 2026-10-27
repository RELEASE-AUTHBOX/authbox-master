[![authbox-logo-small-3.png](https://i.postimg.cc/t4WwwZxf/authbox-logo-small-3.png)](https://postimg.cc/Yv2dmS8f) 
![Static Badge](https://img.shields.io/badge/python-3.8-blue) 
![Static Badge](https://img.shields.io/badge/django-4.0-green) 

# Selamat Datang 

Ini merupakan repository master project AUTHBOX. Berisi proses CRUD, manajemen user, template, menu, permission, dll.
Perubahan di repository ini akan berdampak pada keseluruhan project. 


# Cara menjadi kontributor
## Di github
1. Fork repository : `https://github.com/PROJECT-AUTHBOX/authbox-master` 
    - misal bernama NAMA-REPO
    - maka akan menjadi `https://github.com/NAMA-REPO/authbox-master`

2. Fork repository : `https://github.com/PROJECT-AUTHBOX/authbox-contribute`
    - misal bernama NAMA-REPO
    - maka akan menjadi `https://github.com/NAMA-REPO/authbox-contribute`

## Di komputer
1. Buat folder : `mkdir project-authbox && cd project-authbox`
2. Git clone/pull : `git@github.com:NAMA-REPO/authbox-master.git`
3. Git clone/pull : `git@github.com:NAMA-REPO/authbox-contribute.git`
4. Masuk ke folder utama : `cd authbox-master/engine`
5. Jalankan : `pip install -r requirements.txt` 
6. Jalankan : `python manage.py runserver` 
    - jika error `File Not Found` : `/file/to/environment/folder/.env-komputer-name`
    - copy file environment default : `cp /file/to/environment/folder/.env-default /file/to/environment/folder/.env-komputer-name`
    - kemudian modifikasi file `.env-komputer-name` sesuai setting di komputer Anda.

7. Ulangi step `6`, jika tidak ada error maka lanjutkan ke step `8`
8. Jalankan : `python manage.py migrate`
9. Jalankan : `python manage.py createsuperuser`
10. Jalankan : `python manage.py updatecoredata`
11. Jalankan : `python manage.py runserver` 
12. Masuk ke folder : `cd project-authbox/origin` untuk copy template asli yang digunakan
13. masuk ke folder : `cd project-authbox/clothes` untuk versi template yang digunakan oleh project **django**
14. Cek frontend di : `http://127.0.0.1:8000`
15. Cek backend di : `http://127.0.0.1:8000/id/dashboard` gunakan username yg dibuat diproses `9` 
16. Update database khusus untuk developer di : `http://127.0.0.1:8000/secret-admin` gunakan username yg dibuat diproses `9` 


# Kunjungi website resmi kami 
[AUTHBOX.web.id](https://authbox.web.id)

