import asyncio
import models
import jaarfivts

myvts = jaarfivts.JaarfiVts()


async def connect(vts: jaarfivts.JaarfiVts):
    await vts.connect()
    await vts.authenticate(models.AuthenticationTokenRequest())
    # await vts.request(models.AvailableModelsRequest())
    request = models.ModelLoadRequest(
        data=models.ModelLoadData(model_id="7e8ee3b101fc429f94f501407fccb8bc")
    )
    print(request.model_dump_json(by_alias=True))
    a = await vts.request(request)
    print(a)
    await vts.close()


asyncio.run(connect(myvts))
