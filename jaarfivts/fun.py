import jaarfivts
import models
import asyncio
import time
import nest_asyncio

nest_asyncio.apply()


async def create_fun(settings):
    fun = Fun(settings)
    await fun._init()
    return fun


class Fun:
    def __init__(self, vts: jaarfivts.JaarfiVts) -> None:
        self.vts = vts
        pass

    async def _init(self):
        await self.vts.connect()
        await self.vts.authenticate(models.AuthenticationTokenRequest())

    async def flip(
        self,
        duration_in_seconds: float,
        number_of_rotations: float,
        direction_is_left: bool = False,
    ):
        assert duration_in_seconds >= 0
        assert number_of_rotations >= 0
        fps = 60
        number_of_frames = int(duration_in_seconds * fps)
        rotation_per_frame = number_of_rotations * 360 / number_of_frames
        if direction_is_left:
            rotation_per_frame = rotation_per_frame * -1
        t1 = time.time()
        for i in range(number_of_frames):
            await self.vts.request(
                models.MoveModelRequest(
                    data=models.MoveModelRequestData(
                        time_in_seconds=0,
                        values_are_relative_to_model=True,
                        rotation=rotation_per_frame,
                        size=0,
                    )
                )
            )
        diff = time.time() - t1
        print(number_of_frames / diff)

    async def getItemsInScene(self):
        response = await self.vts.request(
            models.ItemListRequest(
                data=models.ItemListRequestData(
                    include_available_spots=False, include_available_item_files=False
                )
            )
        )
        response = models.ItemListResponse.model_validate(response)
        return response.data.item_instances_in_scene

    async def loadItemIfNotLoaded(self, file_name: str) -> str:
        """
        returns id
        """
        item_instances_in_scene = await self.getItemsInScene()
        matched_item_instances = [
            item_instance
            for item_instance in item_instances_in_scene
            if item_instance.file_name.casefold() == file_name.casefold()
        ]
        if not matched_item_instances:
            response = await self.vts.request(
                models.ItemLoadRequest(
                    data=models.ItemLoadRequestData(file_name=file_name)
                )
            )
            response = models.ItemLoadResponse.model_validate(response)
            return response.data.instance_id
        return matched_item_instances[0].instance_id

    async def pinItemToArtmesh(
        self,
        item_instance_id: str,
        art_mesh_id: str,
        size: float = None,
        size_mult: float = 1,
    ):
        pin_info = models.PinInfo(art_mesh_id=art_mesh_id)
        if not size is None:
            pin_info.size = size
        pin_info.size = pin_info.size * size_mult
        response = await self.vts.request(
            models.ItemPinRequest(
                data=models.ItemPinRequestData(
                    item_instance_id=item_instance_id, pin_info=pin_info
                )
            )
        )
        response = models.ItemPinResponse.model_validate(response)

    async def loadAndPinItemToArtmesh(
        self, file_name: str, art_mesh_id: str, size: float = None, size_mult: float = 1
    ):
        id = await self.loadItemIfNotLoaded(file_name)
        response = await self.pinItemToArtmesh(
            id, art_mesh_id, size=size, size_mult=size_mult
        )

    async def getCurrentModelSize(self):
        response = await self.vts.request(models.CurrentModelRequest())
        response = models.CurrentModelResponse.model_validate(response)
        return response.data.model_position.size

    async def letUserSelectArtMeshes(self, amount_of_artmeshes: int):
        # select single artmesh
        response = await self.vts.request(
            models.ArtMeshSelectionRequest(
                data=models.ArtMeshSelectionRequestData(
                    requested_art_mesh_count=amount_of_artmeshes
                )
            )
        )
        response = models.ArtMeshSelectionResponse.model_validate(response)
        return response.data.active_art_meshes

    async def pinUserDecidesWhere(
        self, file_name: str, size: float = None, size_mult: float = 1
    ):
        selectedArtMeshes = await self.letUserSelectArtMeshes(1)
        selectedArtMesh = selectedArtMeshes[0]
        response = await self.loadAndPinItemToArtmesh(
            file_name, selectedArtMesh, size=size, size_mult=size_mult
        )

    async def pinHeadPat(self):
        response = await self.loadAndPinItemToArtmesh(
            "ANIM_Headpat", "hairfront_2", size_mult=0.55
        )

    async def pinHeadPatUserDecidesWhere(self):
        selectedArtMeshes = await self.letUserSelectArtMeshes(1)
        selectedArtMesh = selectedArtMeshes[0]
        response = await self.loadAndPinItemToArtmesh(
            "ANIM_Headpat", selectedArtMesh, size_mult=0.55
        )

    async def scaleModelToSize(self, size):
        response = await self.vts.request(
            models.MoveModelRequest(
                data=models.MoveModelRequestData(time_in_seconds=0, size=size)
            )
        )

    async def activateGiantessFetish(self):
        self.scaleModelToSize(100)

    async def resetModel(self):
        response = await self.vts.request(
            models.MoveModelRequest(
                data=models.MoveModelRequestData(
                    time_in_seconds=0, position_x=0, position_y=0, rotation=0
                )
            )
        )

    async def moveModel(self, **kwargs):
        data = models.MoveModelRequestData(time_in_seconds=0)
        for a in kwargs:
            data = data.model_copy(update={a: kwargs[a]})
        response = await self.vts.request(models.MoveModelRequest(data=data))

    async def changeAnimationSpeed(self, id: str, fps: float):
        response = await self.vts.request(
            models.ItemAnimationControlRequest(
                data=models.ItemAnimationControlRequestData(
                    item_instance_id=id, framerate=fps
                )
            )
        )

    async def turboHeadpat(self):
        id = await self.loadItemIfNotLoaded("ANIM_Headpat")
        response = await self.changeAnimationSpeed(id, 60)

    async def activateExpression(self, expression_file: str):
        response = await self.vts.request(
            models.ExpressionActivationRequest(
                data=models.ExpressionActivationRequestData(
                    expression_file=expression_file, active=True
                )
            )
        )

    async def getExpressionState(self, expression_file: str):
        response = await self.vts.request(
            models.ExpressionStateRequest(
                data=models.ExpressionStateRequestData(expression_file=expression_file)
            )
        )
        response = models.ExpressionStateResponse.model_validate(response)
        return response.data.expressions[0].active

    async def toggleExpression(self, expression_file: str):
        state = await self.getExpressionState(expression_file=expression_file)
        response = await self.vts.request(
            models.ExpressionActivationRequest(
                data=models.ExpressionActivationRequestData(
                    expression_file=expression_file, active=not state
                )
            )
        )

    async def tintArtmeshes(
        self, color_r: int, color_b: int, color_g: int, art_meshes: list[str]
    ):
        response = await self.vts.request(
            models.ColorTintRequest(
                data=models.ColorTintRequestData(
                    color_tint=models.ColorTint(
                        color_r=color_r, color_b=color_b, color_g=color_g
                    ),
                    art_mesh_matcher=models.ArtMeshMatcher(name_exact=art_meshes),
                )
            )
        )

    async def rainbow(self, repetitions: int):
        increase = True
        colors = [0, 255, 0]
        change = 20
        for i in range(2 * repetitions):
            for color in range(3):
                for i in range(int(255 / change)):
                    if increase:
                        colors[color] = colors[color] + change
                        if colors[color] > 255:
                            colors[color] = 255
                    else:
                        colors[color] = colors[color] - change
                        if colors[color] < 0:
                            colors[color] = 0
                    await self.vts.request(
                        models.ColorTintRequest(
                            data=models.ColorTintRequestData(
                                color_tint=models.ColorTint(
                                    color_r=colors[1],
                                    color_b=colors[2],
                                    color_g=colors[0],
                                ),
                                art_mesh_matcher=models.ArtMeshMatcher(tint_all=True),
                            )
                        )
                    )
                    await asyncio.sleep(1 / 30)
                increase = not increase


async def main():
    settings = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
    fun = await create_fun(settings)
    await fun.resetModel()
    await fun.flip(3, 3)
    await fun.rainbow(1)
    await fun.turboHeadpat()
    await fun.getCurrentModelSize()
    await fun.vts.close()


settings = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")
abc = asyncio.run(create_fun(settings))

if __name__ == "__main__":
    asyncio.run(main())
