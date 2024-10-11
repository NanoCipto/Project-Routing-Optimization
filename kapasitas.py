import pulp as lp

demand_mitra = {
    'Mitra 1' : 10,
    'Mitra 2' : 20,
    'Mitra 3' : 30,
    'Mitra 4' : 10,
}

jarak = {
    'Depot' : {
        'Depot' : 0,
        'Mitra 1' : 10,
        'Mitra 2' : 20,
        'Mitra 3' : 30,
        'Mitra 4' : 40,
    },
    'Mitra 1' : {
        'Depot' : 10,
        'Mitra 1' : 0,
        'Mitra 2' : 25,
        'Mitra 3' : 35,
        'Mitra 4' : 45,
    },
    'Mitra 2' : {
        'Depot' : 20,
        'Mitra 1' : 25,
        'Mitra 2' : 0,
        'Mitra 3' : 15,
        'Mitra 4' : 30,
    },
    'Mitra 3' : {
        'Depot' : 30,
        'Mitra 1' : 35,
        'Mitra 2' : 15,
        'Mitra 3' : 0,
        'Mitra 4' : 20,
    },
    'Mitra 4' : {
        'Depot' : 40,
        'Mitra 1' : 45,
        'Mitra 2' : 30,
        'Mitra 3' : 20,
        'Mitra 4' : 0,
    },
}

kapasitas_kendaraan = {
    'Kendaraan A' : 20,
    'Kendaraan B' : 30,
    'Kendaraan C' : 40,
}

lokasi_awal = jarak.keys()
lokasi_tujuan = jarak.keys()
kendaraan = kapasitas_kendaraan.keys()
demand = demand_mitra.keys()

problem = lp.LpProblem("Capacitated VRP", lp.LpMinimize)
rute = lp.LpVariable.dicts('Rute', (lokasi_awal, lokasi_tujuan, kendaraan),0,1, lp.LpBinary) #Biner
muatan = lp.LpVariable.dicts('Muatan', (lokasi_awal, lokasi_tujuan),0, lp.LpContinuous)

# print(rute)

# Fungsi Tujuan
problem += lp.lpSum(jarak[i][j] * rute[i][j][k] for k in kendaraan for i in lokasi_awal for j in lokasi_tujuan)

# Fungsi Batasan
# 1. Setiap Mitra Menjadi Asal 1x
for i in lokasi_awal:
    if i != 'Depot' :
        problem += lp.lpSum(rute[i][j][k] for k in kendaraan for j in lokasi_tujuan if i != j) == 1

# 2. Setiap Mitra Menjadi Tujuan 1x
for j in lokasi_tujuan:
    if j != 'Depot':
        problem += lp.lpSum(rute[i][j][k] for k in kendaraan for i in lokasi_awal if i != j) == 1

# 3. Setiap Mitra Dilayani 1 Kendaraan
for k in kendaraan :
    for q in lokasi_tujuan :
        problem += lp.lpSum([rute[i][q][k], -rute[q][j][k]] for i in lokasi_awal for j in lokasi_tujuan if i != q and q != j and q != "Depot") == 0

# 4. Setiap Kendaraan Berangkat dari Perusahaan
# for j in lokasi_tujuan:
#     if j != "Depot":
#         problem += lp.lpSum(rute["Depot"][j][k] for k in kendaraan) == 1

# 4.1 Total Kendaraan A yang Berangkat dari Perusahaan == 1
problem += lp.lpSum(rute['Depot'][j]["Kendaraan A"] for j in lokasi_tujuan if j != "Depot") == 1
problem += lp.lpSum(rute['Depot'][j]["Kendaraan B"] for j in lokasi_tujuan if j != "Depot") == 1
problem += lp.lpSum(rute['Depot'][j]["Kendaraan C"] for j in lokasi_tujuan if j != "Depot") == 1

# 5. Setiap Kendaraan yang Berangkat akan Kembali ke Pabrik
# for i in lokasi_awal:
#     if i != "Depot":
#         problem += lp.lpSum(rute[i]["Depot"][k] for k in kendaraan) == 1
problem += lp.lpSum(rute[i]['Depot']["Kendaraan A"] for i in lokasi_awal if i != "Depot") == 1
problem += lp.lpSum(rute[i]['Depot']["Kendaraan B"] for i in lokasi_awal if i != "Depot") == 1
problem += lp.lpSum(rute[i]['Depot']["Kendaraan C"] for i in lokasi_awal if i != "Depot") == 1

# 6. Total Demand yang Dilayani dalam Satu Rute <= Kapasitas Kendaraan
for k in kendaraan :
    problem += lp.lpSum(demand_mitra[i] * rute[i][j][k] for i in lokasi_awal for j in lokasi_tujuan if i != 'Depot' and j != 'Depot' and i != j) <= kapasitas_kendaraan[k]

print(problem)
problem.writeLP("a")
problem.solve()
print('Status : ', lp.LpStatus[problem.status])

for v in problem.variables():
    print(v.name, "=", v.varValue)

if lp.LpStatus[problem.status] == "Optimal":
    print("Total Jarak= ", lp.value(problem.objective))
    ruteterpilih_kendaraan_A =[]
    ruteterpilih_kendaraan_B =[]
    ruteterpilih_kendaraan_C =[]
    for k in kendaraan:
        for i in lokasi_awal:
            for j in lokasi_tujuan:
                if rute[i][j][k].varValue == 1 and k == "Kendaraan A":
                    ruteterpilih_kendaraan_A.append((i, j))
                elif rute[i][j][k].varValue == 1 and k == "Kendaraan B":
                    ruteterpilih_kendaraan_B.append((i, j))
                elif rute[i][j][k].varValue == 1 and k == "Kendaraan C":
                    ruteterpilih_kendaraan_C.append((i, j))
        if ruteterpilih_kendaraan_A and k == "Kendaraan A":
            print(f"Rute Kendaraaan {k}: {ruteterpilih_kendaraan_A}")
        elif ruteterpilih_kendaraan_B and k == "Kendaraan B":
            print(f"Rute Kendaraaan {k}: {ruteterpilih_kendaraan_B}")
        elif ruteterpilih_kendaraan_C and k == "Kendaraan C":
            print(f"Rute Kendaraaan {k}: {ruteterpilih_kendaraan_C}")
        else:
            print(f'Kendaraan {k} tidak beroperasi')
else:
    print('Tidak Ada Solusi Optimal')


