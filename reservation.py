from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

class Reservation(BaseModel):
    id_reservasi: int
    tanggal_pemotretan: str
    lokasi_pemotretan: str
    waktu_pemotretan: str
    durasi_pemotretan: str
    keperluan_reservasi: str
    jumlah_model: int

router = APIRouter()

reservation_file = "data/reservation.json"

with open(reservation_file,"r") as read_file:
    reservation_data = json.load(read_file)

@router.get('/')
async def get_all_reservations():
    return reservation_data['reservation']

@router.get('/{reservation_id_reservasi}')
async def view_reservation(reservation_id_reservasi: int):
    reservation_found = False
    for reservation_iterate in reservation_data['reservation']:
        if reservation_iterate['id_reservasi'] == reservation_id_reservasi:
            reservation_found = True
            return reservation_iterate
    raise HTTPException(
        status_code = 404, detail =f'reservation belum terdaftar.'
    )
    
@router.post('/reservation')
async def add_reservation(reservation: Reservation):
    reservation_dict = reservation.dict()
    reservation_found = False
    for reservation_iterate in reservation_data['reservation']:
        if reservation_iterate['id_reservasi'] == reservation.id_reservasi:
            reservation_found = True
            return "id_reservasi sudah digunakan."
    if not reservation_found:    
        reservation_data['reservation'].append(reservation_dict)
        with open(reservation_file, "w") as write_file:
            json.dump(reservation_data, write_file)
        return "Akun reservation berhasil ditambahkan."
    raise HTTPException(
        status_code = 404, detail=f'id_reservasi sudah digunakan.'
    )

@router.put('/reservation')
async def edit_reservation(reservation: Reservation):
    reservation_dict = reservation.dict()
    reservation_found = False

    for reservation_idx, reservation_iterate in enumerate(reservation_data['reservation']):
        if reservation_iterate['id_reservasi'] == reservation_dict['id_reservasi']:
            reservation_found = True
            reservation_data['reservation'][reservation_idx] = reservation_dict
            with open(reservation_file, "w") as write_file:
                json.dump(reservation_data, write_file)
            return "Akun reservation berhasil diperbarui."
    if not reservation_found:
        return "Akun reservation tidak ditemukan."
    raise HTTPException(
        status_code = 404, detail=f'Pembaruan akun gagal.'
    )

@router.delete('/reservation/{reservation_id_reservasi}')
async def cancel_reservation(reservation_id_reservasi: int):
    reservation_found = False
    for reservation_idx, reservation_iterate in enumerate(reservation_data['reservation']):
        if reservation_iterate['id_reservasi'] == reservation_id_reservasi:
            reservation_found = True
            reservation_data['reservation'].pop(reservation_idx)
            with open(reservation_file, "w") as write_file:
                json.dump(reservation_data, write_file)
            return "Akun reservation berhasil dihapus."
        
    if not reservation_found:
        return "Akun reservation tidak ditemukan."
    raise HTTPException(
        status_code = 404, detail=f'Penghapusan akun gagal.'
    )