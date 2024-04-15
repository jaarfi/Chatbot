"""
Contains all the data structure for the different requests you can send to VTS
"""

from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel, to_snake


class _Model(BaseModel):
    """
    Base for all Data Structures
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel, validation_alias=to_snake
        )
    )


class BaseRequest(_Model):
    """
    The Base for all coming requests
    """

    api_name: str = "VTubeStudioPublicAPI"
    """Name of the API"""
    api_version: str = "1.0"
    """Version of the API"""
    request_id: str = "SomeID"
    """Id for the request, does not have to be unique"""
    message_type: str
    """Defining which request gets sent to VTubeStudio"""
    data: _Model | None
    """The data associated with the request type, can be non in case messageType is """


class APIStateRequest(BaseRequest):
    """Request the current state of the API"""

    message_type: Literal["APIStateRequest"] = "APIStateRequest"
    data: None = None


class AuthenticationTokenData(_Model):
    """
    Data structure for an AuthenticationTokenRequest
    """

    plugin_name: str = "PyVtsPlugin"
    """Name of the Plugin"""
    plugin_developer: str = "jaarfi"
    """Name of the Developer"""
    plugin_icon: str | None = None
    """optional: Base64 encoded PNG or JPG with exact dimensions of 128x128"""


class AuthenticationTokenRequest(BaseRequest):
    """
    Request an Authentication Token, this token is valid even after restarting the plugin or VTS.

    This will trigger a PopUp inside of VTubeStudio provided that Plugins are enabled.
    """

    message_type: Literal["AuthenticationTokenRequest"] = "AuthenticationTokenRequest"
    data: AuthenticationTokenData = AuthenticationTokenData()


class AuthenticationData(_Model):
    """
    Data structure for an AuthenticationRequest
    """

    plugin_name: str = "PyVtsPlugin"
    """Name of the Plugin, has to match the provided name upon requesting a token"""
    plugin_developer: str = "jaarfi"
    """Name of the Developer, has to match the provided dev upon requesting a token"""
    authentication_token: str
    """The authentication Token that a AuthenticationTokenRequest returned"""


class AuthenticationRequest(BaseRequest):
    """
    Request an Authentication for this session using a token, this has to be done once per session.

    Data has to match the data provided when requesting the token.
    """

    message_type: Literal["AuthenticationRequest"] = "AuthenticationRequest"
    data: AuthenticationData


class StatisticsRequest(BaseRequest):
    message_type: Literal["StatisticsRequest"] = "StatisticsRequest"
    data: None = None


class VTSFolderInfoRequest(BaseRequest):
    message_type: Literal["VTSFolderInfoRequest"] = "VTSFolderInfoRequest"
    data: None = None


class CurrentModelRequest(BaseRequest):
    message_type: Literal["CurrentModelRequest"] = "CurrentModelRequest"
    data: None = None


class AvailableModelsRequest(BaseRequest):
    message_type: Literal["AvailableModelsRequest"] = "AvailableModelsRequest"
    data: None = None


class ModelLoadData(_Model):
    model_id: str = Field(serialization_alias="modelID")
    """Unique Id of Model to load"""


class ModelLoadRequest(BaseRequest):
    message_type: Literal["ModelLoadRequest"] = "ModelLoadRequest"
    data: ModelLoadData


class ModelMoveData(_Model):
    time_in_seconds: float = Field(ge=0, le=2)
    """ 0 <= time_in_seconds <= 2
    The time the movement should take in seconds, if set to 0 the model will instantly appear in the new position"""
    values_are_relative_to_model: bool = False
    """If the values are relative to the model, they get added to the models current values, otherwise they are absolute"""
    position_x: Optional[float] = Field(ge=-1, le=1)
    """ -1 <= position_x <= 1
    0 positions the middle of the model in the middle of the x-axis, """
    position_y: Optional[float] = Field(ge=-1, le=1)
    """ -1 <= position_x <= 1
    0 positions the middle of the model in the middle of the y-axis, """
    rotation: Optional[float] = Field(ge=-360, le=360)
    """ -360 <= rotation <= 360
    Desired rotation in degrees, positive rotate clockwise, negative rotates counter-clockwise
    """
    size: float = Field(default=-70, ge=-100, le=100)
    """The size the model should shrink/enlargen to, -70 is normal size"""

class ModelMoveRequest(BaseRequest):
    message_type: Literal["ModelMoveRequest"] = "ModelMoveRequest"
    data: ModelMoveData