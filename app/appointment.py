from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

class Appointment(BaseModel):
    id_pertemuan: int
    pengajuan_tanggal: str
    pengajuan_waktu: str
    pengajuan_durasi: str
    pengajuan_tempat: str
    status: str # 1) Diajukan; 2) Di-review; 3) Disetujui; 4) Ditolak; 5) Dibatalkan; 6) Selesai
    catatan_client: str
    catatan_vendor: str

router = APIRouter()

appointment_file = "./data/appointment.json"

with open(appointment_file,"r") as read_file:
    appointment_data = json.load(read_file)

@router.get('/', tags=["Appointment"])
async def get_all_appointments():
    return appointment_data['appointment']

@router.get('/{appointment_id_pertemuan}', tags=["Appointment"])
async def view_appointment(appointment_id_pertemuan: int):
    appointment_found = False
    for appointment_iterate in appointment_data['appointment']:
        if appointment_iterate['id_pertemuan'] == appointment_id_pertemuan:
            appointment_found = True
            return appointment_iterate
    raise HTTPException(
        status_code = 404, detail =f'appointment belum terdaftar.'
    )
    
@router.post('/appointment', tags=["Appointment"])
async def make_appointment(appointment: Appointment):
    appointment_dict = appointment.dict()
    appointment_found = False
    for appointment_iterate in appointment_data['appointment']:
        if appointment_iterate['id_pertemuan'] == appointment.id_pertemuan:
            appointment_found = True
            return "id_pertemuan sudah digunakan."
    if not appointment_found:    
        appointment_data['appointment'].append(appointment_dict)
        with open(appointment_file, "w") as write_file:
            json.dump(appointment_data, write_file)
        return "Akun appointment berhasil ditambahkan."
    raise HTTPException(
        status_code = 404, detail=f'id_pertemuan sudah digunakan.'
    )

@router.put('/appointment', tags=["Appointment"])
async def edit_appointment(appointment: Appointment):
    appointment_dict = appointment.dict()
    appointment_found = False

    for appointment_idx, appointment_iterate in enumerate(appointment_data['appointment']):
        if appointment_iterate['id_pertemuan'] == appointment_dict['id_pertemuan']:
            appointment_found = True
            appointment_data['appointment'][appointment_idx] = appointment_dict
            with open(appointment_file, "w") as write_file:
                json.dump(appointment_data, write_file)
            return "Akun appointment berhasil diperbarui."
    if not appointment_found:
        return "Akun appointment tidak ditemukan."
    raise HTTPException(
        status_code = 404, detail=f'Pembaruan gagal.'
    )