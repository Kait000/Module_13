import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнование.')
    for i in range(5):
        await asyncio.sleep(10 / power)
        print(f'Силач {name} поднял шар {i+1}')
    print(f'Силач {name} закончил соревнование.')


async def start_tournament():
    andrey = asyncio.create_task(start_strongman('Andrey', 5))
    mihail = asyncio.create_task(start_strongman('Mihail', 4))
    sergei = asyncio.create_task(start_strongman('Sergei', 3))
    await andrey
    await mihail
    await sergei

asyncio.run(start_tournament())
