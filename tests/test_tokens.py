# This file was auto-generated by Fern from our API Definition.

from label_studio_sdk import LabelStudio
from label_studio_sdk import AsyncLabelStudio
import typing
from .utilities import validate_response


async def test_blacklist(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    # Type ignore to avoid mypy complaining about the function not being meant to return a value
    assert (
        client.tokens.blacklist(refresh="refresh")  # type: ignore[func-returns-value]
        is None
    )

    assert (
        await async_client.tokens.blacklist(refresh="refresh")  # type: ignore[func-returns-value]
        is None
    )


async def test_get(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    expected_response: typing.Any = [{"token": "token", "created_at": "created_at", "expires_at": "expires_at"}]
    expected_types: typing.Tuple[typing.Any, typing.Any] = (
        "list",
        {0: {"token": None, "created_at": None, "expires_at": None}},
    )
    response = client.tokens.get()
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.tokens.get()
    validate_response(async_response, expected_response, expected_types)


async def test_create(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    expected_response: typing.Any = {"token": "token", "created_at": "created_at", "expires_at": "expires_at"}
    expected_types: typing.Any = {"token": None, "created_at": None, "expires_at": None}
    response = client.tokens.create()
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.tokens.create()
    validate_response(async_response, expected_response, expected_types)


async def test_refresh(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    expected_response: typing.Any = {"access": "access"}
    expected_types: typing.Any = {"access": None}
    response = client.tokens.refresh(refresh="refresh")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.tokens.refresh(refresh="refresh")
    validate_response(async_response, expected_response, expected_types)


async def test_rotate(client: LabelStudio, async_client: AsyncLabelStudio) -> None:
    expected_response: typing.Any = {"refresh": "refresh"}
    expected_types: typing.Any = {"refresh": None}
    response = client.tokens.rotate(refresh="refresh")
    validate_response(response, expected_response, expected_types)

    async_response = await async_client.tokens.rotate(refresh="refresh")
    validate_response(async_response, expected_response, expected_types)
