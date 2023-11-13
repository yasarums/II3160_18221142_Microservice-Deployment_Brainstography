from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

class Progrep(BaseModel):
    no_laporan: int
    tanggal: str
    waktu_awal: str
    waktu_akhir: str
    tempat: str
    peserta: str
    agenda: str
    berkas_penting: str
    hasil: str
    to_do: str

router = APIRouter()

progrep_file = "./data/progrep.json"

with open(progrep_file,"r") as read_file:
    progrep_data = json.load(read_file)

@router.get('/', tags=["Progrep"])
async def get_all_progreps():
    return progrep_data['progrep']

@router.get('/{progrep_no_laporan}', tags=["Progrep"])
async def view_progrep(progrep_no_laporan: int):
    progrep_found = False
    for progrep_iterate in progrep_data['progrep']:
        if progrep_iterate['no_laporan'] == progrep_no_laporan:
            progrep_found = True
            return progrep_iterate
    raise HTTPException(
        status_code = 404, detail =f'progrep belum terdaftar.'
    )
    
@router.post('/progrep', tags=["Progrep"])
async def add_progrep(progrep: Progrep):
    progrep_dict = progrep.dict()
    progrep_found = False
    ''' for progrep_iterate in progrep_data['progrep']:
        if progrep_iterate['no_laporan'] == progrep.no_laporan:
            progrep_found = True
            return "no_laporan sudah digunakan." '''
    if not progrep_found:
        progrep_dict['no_laporan'] = len(progrep_data) + 1    
        progrep_data['progrep'].append(progrep_dict)
        with open(progrep_file, "w") as write_file:
            json.dump(progrep_data, write_file)
        return "Akun progrep berhasil ditambahkan."
    raise HTTPException(
        status_code = 404, detail=f'no_laporan sudah digunakan.'
    )

@router.put('/progrep', tags=["Progrep"])
async def edit_progrep(progrep: Progrep):
    progrep_dict = progrep.dict()
    progrep_found = False

    for progrep_idx, progrep_iterate in enumerate(progrep_data['progrep']):
        if progrep_iterate['no_laporan'] == progrep_dict['no_laporan']:
            progrep_found = True
            progrep_data['progrep'][progrep_idx] = progrep_dict
            with open(progrep_file, "w") as write_file:
                json.dump(progrep_data, write_file)
            return "Akun progrep berhasil diperbarui."
    if not progrep_found:
        return "Akun progrep tidak ditemukan."
    raise HTTPException(
        status_code = 404, detail=f'Pembaruan gagal.'
    )