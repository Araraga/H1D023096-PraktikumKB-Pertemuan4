% Fakta dinamis
:- dynamic fakta/1.

% Aturan Diagnosis
rule('Koneksi internet terputus dari ISP atau router mati.',
     [tidak_ada_akses, terhubung_wifi, semua_terpengaruh]).

rule('IP conflict atau DNS salah.',
     [tidak_ada_akses, hanya_perangkat_ini, ada_tanda_seru]).

rule('Perangkat tidak terhubung Wi-Fi.',
     [tidak_terhubung_wifi]).

rule('Interferensi Wi-Fi atau penggunaan bandwidth tinggi.',
     [ping_tinggi, terhubung_wifi]).

rule('Switch bermasalah atau kabel rusak.',
     [ping_tinggi, menggunakan_ethernet]).

rule('DNS server bermasalah.',
     [dns_tidak_merespon]).

% Diagnosis berhasil jika semua syarat dalam rule terpenuhi
diagnosa(Diagnosis) :-
    rule(Diagnosis, Syarat),
    forall(member(F, Syarat), fakta(F)).

% Solusi untuk setiap diagnosis
solusi('Koneksi internet terputus dari ISP atau router mati.',
       'Restart router, cek koneksi ISP, atau hubungi teknisi.').

solusi('IP conflict atau DNS salah.',
       'Periksa IP dan DNS di pengaturan jaringan, aktifkan DHCP.').

solusi('Perangkat tidak terhubung Wi-Fi.',
       'Pastikan Wi-Fi aktif dan password benar.').

solusi('Interferensi Wi-Fi atau penggunaan bandwidth tinggi.',
       'Minimalkan jumlah perangkat dan ubah channel Wi-Fi.').

solusi('Switch bermasalah atau kabel rusak.',
       'Coba ganti kabel LAN atau pindahkan ke port lain.').

solusi('DNS server bermasalah.',
       'Gunakan DNS publik seperti 8.8.8.8 atau 1.1.1.1.').
