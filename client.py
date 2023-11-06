from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

class Client(BaseModel):
    email: str
    nama_lengkap: str
    nama_panggilan : str
    url_foto_profil: str
    no_telepon: str
    no_whatsapp: str

router = APIRouter()

client_file = "data/client.json"

with open(client_file,"r") as read_file:
    client_data = json.load(read_file)

@router.get('/')
async def get_all_clients():
    return client_data['client']

@router.get('/{client_email}')
async def view_client(client_email: str):
    client_found = False
    for client_iterate in client_data['client']:
        if client_iterate['email'] == client_email:
            client_found = True
            return client_iterate
    raise HTTPException(
        status_code = 404, detail =f'Client belum terdaftar.'
    )
    
@router.post('/client')
async def add_client(client: Client):
    client_dict = client.dict()
    client_found = False
    for client_iterate in client_data['client']:
        if client_iterate['email'] == client.email:
            client_found = True
            return "Email sudah digunakan."
    if not client_found:    
        client_data['client'].append(client_dict)
        with open(client_file, "w") as write_file:
            json.dump(client_data, write_file)
        return "Akun client berhasil ditambahkan."
    raise HTTPException(
        status_code = 404, detail=f'Penambahan akun gagal.'
    )

@router.put('/client')
async def edit_client(client: Client):
    client_dict = client.dict()
    client_found = False

    for client_idx, client_iterate in enumerate(client_data['client']):
        if client_iterate['email'] == client_dict['email']:
            client_found = True
            client_data['client'][client_idx] = client_dict
            with open(client_file, "w") as write_file:
                json.dump(client_data, write_file)
            return "Akun client berhasil diperbarui."
    if not client_found:
        return "Akun client tidak ditemukan."
    raise HTTPException(
        status_code = 404, detail=f'Pembaruan akun gagal.'
    )

@router.delete('/client/{client_email}')
async def remove_client(client_email: str):
    client_found = False
    for client_idx, client_iterate in enumerate(client_data['client']):
        if client_iterate['email'] == client_email:
            client_found = True
            client_data['client'].pop(client_idx)
            with open(client_file, "w") as write_file:
                json.dump(client_data, write_file)
            return "Akun client berhasil dihapus."
        
    if not client_found:
        return "Akun client tidak ditemukan."
    raise HTTPException(
        status_code = 404, detail=f'Penghapusan akun gagal.'
    )