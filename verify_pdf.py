import asyncio
import aiohttp
import json
import os

async def test():
    async with aiohttp.ClientSession() as session:
        # 1. Login to get cookie
        login_data = aiohttp.FormData()
        login_data.add_field('username', 'admin@techcorp.com')
        login_data.add_field('password', 'securepassword')
        
        async with session.post('http://localhost:8000/api/v1/auth/login', data=login_data) as resp:
            print("Login:", resp.status)
            if resp.status != 200:
                print(await resp.text())
                return
        
        # 2. Upload test_contract.pdf
        with open('test_contract.pdf', 'rb') as f:
            upload_data = aiohttp.FormData()
            upload_data.add_field('file', f, filename='test_contract.pdf', content_type='application/pdf')
            async with session.post('http://localhost:8000/api/v1/contracts/upload', data=upload_data) as resp:
                print("Upload:", resp.status)
                if resp.status != 200:
                    print(await resp.text())
                    return
                res = await resp.json()
                print("Upload response:", res)
                contract_id = res['contract_id']
                
        # 3. Fetch PDF endpoint
        async with session.get(f'http://localhost:8000/api/v1/contracts/{contract_id}/pdf') as resp:
            print("Fetch PDF:", resp.status)
            if resp.status == 200:
                print("PDF successfully downloaded! Content Type:", resp.headers.get('Content-Type'))
            else:
                print(await resp.text())

if __name__ == "__main__":
    asyncio.run(test())
