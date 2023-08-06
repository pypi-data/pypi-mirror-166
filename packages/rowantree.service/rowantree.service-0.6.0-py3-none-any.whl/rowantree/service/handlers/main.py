""" The Rowan Tree Service Layer Handler(s) """

import logging
import os
from pathlib import Path

from fastapi import FastAPI, Header, status
from mysql.connector.pooling import MySQLConnectionPool
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from rowantree.contracts import (
    ActionQueue,
    User,
    UserActive,
    UserFeature,
    UserFeatures,
    UserIncomes,
    UserMerchants,
    UserPopulation,
    UserState,
    UserStores,
    WorldStatus,
)
from rowantree.service.sdk import MerchantTransformRequest, UserIncomeSetRequest, UserTransportRequest

from ..config.server import ServerConfig
from ..controllers.action_queue_process import ActionQueueProcessController
from ..controllers.merchant_transforms_perform import MerchantTransformPerformController
from ..controllers.user_active_get import UserActiveGetController
from ..controllers.user_active_set import UserActiveSetController
from ..controllers.user_create import UserCreateController
from ..controllers.user_delete import UserDeleteController
from ..controllers.user_features_active_get import UserFeaturesActiveGetController
from ..controllers.user_features_get import UserFeaturesGetController
from ..controllers.user_income_get import UserIncomeGetController
from ..controllers.user_income_set import UserIncomeSetController
from ..controllers.user_merchant_transforms_get import UserMerchantTransformsGetController
from ..controllers.user_population_get import UserPopulationGetController
from ..controllers.user_state_get import UserStateGetController
from ..controllers.user_stores_get import UserStoresGetController
from ..controllers.user_transport import UserTransportController
from ..controllers.world_get import WorldStatusGetController
from ..db.dao import DBDAO
from ..db.utils import get_connect_pool

# Generating server configuration
config: ServerConfig = ServerConfig()

# Setup logging
Path(config.log_dir).mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG,
    filemode="w",
    filename=f"{config.log_dir}/{os.uname()[1]}.therowantree.service.log",
)

logging.debug("Starting server")

logging.debug(config.json(by_alias=True, exclude_unset=True))

# Creating database connection pool, and DAO
cnxpool: MySQLConnectionPool = get_connect_pool(config=config)
dao: DBDAO = DBDAO(cnxpool=cnxpool)

# Create controllers
merchant_transforms_perform_controller = MerchantTransformPerformController(dao=dao)
user_active_get_controller = UserActiveGetController(dao=dao)
user_active_set_controller = UserActiveSetController(dao=dao)
user_create_controller = UserCreateController(dao=dao)
user_delete_controller = UserDeleteController(dao=dao)
user_features_get_controller = UserFeaturesGetController(dao=dao)
user_features_active_get_controller = UserFeaturesActiveGetController(dao=dao)
user_income_get_controller = UserIncomeGetController(dao=dao)
user_income_set_controller = UserIncomeSetController(dao=dao)
user_merchant_transforms_get_controller = UserMerchantTransformsGetController(dao=dao)
user_population_get_controller = UserPopulationGetController(dao=dao)
user_transport_controller = UserTransportController(dao=dao)
user_state_get_controller = UserStateGetController(dao=dao)
user_stores_get_controller = UserStoresGetController(dao=dao)
world_status_get_controller = WorldStatusGetController(dao=dao)
action_queue_process_controller = ActionQueueProcessController(dao=dao)

# Create the FastAPI application
app = FastAPI()

#  Apply COR Configuration | https://fastapi.tiangolo.com/tutorial/cors/
origins = ["http://localhost", "http://localhost:8080", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Naive auth system until idp can be introduced
def authorize(api_access_key: str) -> None:
    """
    Performs naive authorization.

    Parameters
    ----------
    api_access_key: str
        The external provided access key to validate.
    """

    if api_access_key != config.access_key:
        logging.debug("bad access key")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad Access Key")


# Define our handlers


@app.get("/health/plain", status_code=status.HTTP_200_OK)
async def health_plain() -> bool:
    """
    Get Application Health
    [GET] /health/plain

    Returns
    -------
    [STATUS CODE] 200: OK
        health: bool
            A true/false response of server health.
    """

    return True


@app.post("/v1/user/{user_guid}/merchant", status_code=status.HTTP_201_CREATED)
async def merchant_transforms_perform_handler(
    user_guid: str, request: MerchantTransformRequest, api_access_key: str = Header(default=None)
) -> None:
    """
    Perform Merchant Exchange (Transform) For User
    [POST] /v1/user/{user_guid}/merchant

    Path
    ----
    user_guid: str
        The target user guid.

    Body
    ----
    request: MerchantTransformRequest
        The requested merchant transform.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    [STATUS CODE]
        201 - Accepted
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    merchant_transforms_perform_controller.execute(user_guid=user_guid, request=request)


@app.get("/v1/user/{user_guid}/merchant", status_code=status.HTTP_200_OK)
async def user_merchant_transforms_get_handler(
    user_guid: str, api_access_key: str = Header(default=None)
) -> UserMerchants:
    """
    Gets user merchants.
    [GET] /v1/user/{user_guid}/merchant

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_merchants: UserMerchants
        The user merchants.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_merchant_transforms_get_controller.execute(user_guid=user_guid)


# Get User's Active State
@app.get("/v1/user/{user_guid}/active", status_code=status.HTTP_200_OK)
async def user_active_get_handler(user_guid: str, api_access_key: str = Header(default=None)) -> UserActive:
    """
    Gets user's active state.
    [GET] /v1/user/{user_guid}/active

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_active_state: UserActive
        The user active state

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_active_get_controller.execute(user_guid=user_guid)


# Set User's Active State
@app.post("/v1/user/{user_guid}/active", status_code=status.HTTP_200_OK)
async def user_active_set_handler(
    user_guid: str, request: UserActive, api_access_key: str = Header(default=None)
) -> UserActive:
    """
    Sets user's active state.
    [POST] /v1/user/{user_guid}/active

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_active_state: UserActive
        The user active state

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_active_set_controller.execute(user_guid=user_guid, request=request)


# Create User
@app.post("/v1/user", status_code=status.HTTP_201_CREATED)
async def user_create_handler(api_access_key: str = Header(default=None)) -> User:
    """
    Creates a user.
    [POST] /v1/user

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_active_state: User
        The user.

    [STATUS CODE]
        201 - Accepted
        401 - Not authorized
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_create_controller.execute()


# Delete User
@app.delete("/v1/user/{user_guid}", status_code=status.HTTP_200_OK)
async def user_delete_handler(user_guid: str, api_access_key: str = Header(default=None)) -> None:
    """
    Deletes a user.
    [DELETE] /v1/user/{user_guid}

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    user_delete_controller.execute(user_guid=user_guid)


@app.get("/v1/user/{user_guid}/features", status_code=status.HTTP_200_OK)
async def user_features_get_handler(user_guid: str, api_access_key: str = Header(default=None)) -> UserFeatures:
    """
    Get User Features.
    [GET] /v1/user/{user_guid}/features

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_features: UserFeatures
    The user features.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_features_get_controller.execute(user_guid=user_guid)


@app.get("/v1/user/{user_guid}/features/active", status_code=status.HTTP_200_OK)
async def user_features_active_get_handler(
    user_guid: str, api_access_key: str = Header(default=None), details: bool = False
) -> UserFeature:
    """
    Get Active User Features.
    [GET] /v1/user/{user_guid}/features/active

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_features: UserFeatures
    The active user features.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_features_active_get_controller.execute(user_guid=user_guid, details=details)


@app.get("/v1/user/{user_guid}/income", status_code=status.HTTP_200_OK)
async def user_income_get_handler(user_guid: str, api_access_key: str = Header(default=None)) -> UserIncomes:
    """
    Get User Income Sources.
    [GET] /v1/user/{user_guid}/income

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_incomes: UserIncomes
    The user income sources.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_income_get_controller.execute(user_guid=user_guid)


@app.post("/v1/user/{user_guid}/income", status_code=status.HTTP_200_OK)
async def user_income_set_handler(
    user_guid: str, request: UserIncomeSetRequest, api_access_key: str = Header(default=None)
) -> None:
    """
    Set User Income Source.
    [POST] /v1/user/{user_guid}/income

    Path
    ----------
    user_guid: str
        The target user guid.

    Body
    ----
    request: UserIncomeSetRequest
        The user income set request.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    user_income_set_controller.execute(user_guid=user_guid, request=request)


@app.get("/v1/user/{user_guid}/population", status_code=status.HTTP_200_OK)
async def user_population_get_handler(user_guid: str, api_access_key: str = Header(default=None)) -> UserPopulation:
    """
    Set User Population.
    [GET] /v1/user/{user_guid}/population

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_population: UserPopulation
        User population.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_population_get_controller.execute(user_guid=user_guid)


@app.post("/v1/user/{user_guid}/transport", status_code=status.HTTP_200_OK)
async def user_transport_handler(
    user_guid: str, request: UserTransportRequest, api_access_key: str = Header(default=None)
) -> UserFeature:
    """
    Transport User
    [POST] /v1/user/{user_guid}/transport

    Path
    ----------
    user_guid: str
        The target user guid.

    Body
    ----
    request: UserTransportRequest
        The user transport request.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_feature: UserFeature
        Active User Feature.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_transport_controller.execute(user_guid=user_guid, request=request)


@app.get("/v1/user/{user_guid}/state", status_code=status.HTTP_200_OK)
async def user_state_get_handler(user_guid: str, api_access_key: str = Header(default=None)) -> UserState:
    """
    Get User State
    [GET] /v1/user/{user_guid}/state

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_state: UserState
        User state.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_state_get_controller.execute(user_guid=user_guid)


@app.get("/v1/user/{user_guid}/stores", status_code=status.HTTP_200_OK)
async def user_stores_get_handler(user_guid: str, api_access_key: str = Header(default=None)) -> UserStores:
    """
    Get User Stores
    [GET] /v1/user/{user_guid}/stores

    Path
    ----------
    user_guid: str
        The target user guid.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    user_stores: UserStores
        User stores.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        404 - User not found
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return user_stores_get_controller.execute(user_guid=user_guid)


@app.get("/v1/world", status_code=status.HTTP_200_OK)
async def world_get_handler(api_access_key: str = Header(default=None)) -> WorldStatus:
    """
    Get World Status
    [GET] /v1/world

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    world_status: WorldStatus
        World status.

    [STATUS CODE]
        200 - OK
        401 - Not authorized
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    return world_status_get_controller.execute()


@app.post("/v1/world/queue", status_code=status.HTTP_200_OK)
async def action_queue_process_handler(request: ActionQueue, api_access_key: str = Header(default=None)) -> None:
    """
    Progress Action Queue
    [POST] /v1/world/queue

    Body
    ----
    request: ActionQueue
        Action queue.

    Header
    ------
    api_access_key: str
        Request Access Key

    Returns
    -------
    [STATUS CODE]
        200 - OK
        401 - Not authorized
        500 - Server failure
    """

    authorize(api_access_key=api_access_key)
    action_queue_process_controller.execute(request=request)
