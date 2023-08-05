""" Database DAO Definition """

import logging
import socket
from datetime import datetime
from typing import Optional, Tuple

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.pooling import MySQLConnectionPool

from rowantree.contracts import (
    ActionQueue,
    Merchant,
    User,
    UserActive,
    UserEvent,
    UserFeature,
    UserFeatures,
    UserIncome,
    UserIncomes,
    UserMerchants,
    UserNotification,
    UserNotifications,
    UserPopulation,
    UserStore,
    UserStores,
)
from rowantree.service.sdk import UserIncomeSetRequest

from .incorrect_row_count_error import IncorrectRowCountError


class DBDAO:
    """
    Database DAO

    Attributes
    ----------
    cnxpool: Any
        MySQL Connection Pool
    """

    cnxpool: MySQLConnectionPool

    def __init__(self, cnxpool: MySQLConnectionPool):
        self.cnxpool = cnxpool

    def merchant_transform_perform(self, user_guid: str, store_name: str) -> None:
        args: list = [user_guid, store_name]
        self._call_proc("peformMerchantTransformByGUID", args)

    def user_active_feature_get(self, user_guid: str) -> UserFeature:
        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str]] = self._call_proc("getUserActiveFeatureByGUID", args)
        if len(rows) != 1:
            raise IncorrectRowCountError(f"Result count was not exactly one. Received: {rows}")
        feature_detail: UserFeature = UserFeature(name=rows[0][0])
        return feature_detail

    def user_active_feature_state_details_get(self, user_guid: str) -> UserFeature:
        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str, Optional[str]]] = self._call_proc("getUserActiveFeatureStateDetailsByGUID", args)
        if len(rows) != 1:
            raise IncorrectRowCountError(f"Result count was not exactly one. Received: {rows}")

        feature_detail: UserFeature = UserFeature(name=rows[0][0], description=rows[0][1])
        return feature_detail

    def users_active_get(self) -> list[str]:
        my_active_users: list[str] = []
        rows: list[Tuple] = self._call_proc("getActiveUsers", [])
        for response_tuple in rows:
            my_active_users.append(response_tuple[0])
        return my_active_users

    def user_active_state_get(self, user_guid: str) -> UserActive:
        args: list[str, int] = [
            user_guid,
        ]
        rows: list[Tuple[int]] = self._call_proc("getUserActivityStateByGUID", args, True)
        if len(rows) != 1:
            raise IncorrectRowCountError(f"Result count was not exactly one. Received: {rows}")
        if rows[0][0] == 0:
            active: bool = False
        else:
            active: bool = True
        return UserActive(active=active)

    def user_active_state_set(self, user_guid: str, active: bool) -> None:
        args = [
            user_guid,
        ]
        if active:
            proc = "setUserActiveByGUID"
        else:
            proc = "setUserInactiveByGUID"
        self._call_proc(name=proc, args=args)

    def user_create(self) -> User:
        rows: list[Tuple[str]] = self._call_proc("createUser", [])
        if len(rows) != 1:
            raise IncorrectRowCountError(f"Result count was not exactly one. Received: {rows}")
        return User(guid=rows[0][0])

    def user_delete(self, user_guid: str) -> None:
        args: list = [
            user_guid,
        ]
        self._call_proc("deleteUserByGUID", args)

    def user_features_get(self, user_guid: str) -> UserFeatures:
        features: list[UserFeature] = []

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str]] = self._call_proc("getUserFeaturesByGUID", args)
        for row in rows:
            features.append(UserFeature(name=row[0]))
        return UserFeatures(features=features)

    def user_income_get(self, user_guid: str) -> UserIncomes:
        income_sources: list[UserIncome] = []

        args: list[str] = [
            user_guid,
        ]
        rows: list[Tuple[int, str, Optional[str]]] = self._call_proc("getUserIncomeByGUID", args)
        for row in rows:
            income: UserIncome = UserIncome(amount=row[0], name=row[1], description=row[2])
            income_sources.append(income)
        return UserIncomes(incomes=income_sources)

    def user_income_set(self, user_guid: str, transaction: UserIncomeSetRequest) -> None:
        args = [user_guid, transaction.income_source_name, transaction.amount]
        self._call_proc("deltaUserIncomeByNameAndGUID", args)

    def user_merchant_transforms_get(self, user_guid: str) -> UserMerchants:
        merchants: list[Merchant] = []

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[str]] = self._call_proc("getUserMerchantTransformsByGUID", args)
        for row in rows:
            merchants.append(Merchant(name=row[0]))
        return UserMerchants(merchants=merchants)

    def user_notifications_get(self, user_guid: str) -> UserNotifications:
        notifications: list[UserNotification] = []

        args: list = [
            user_guid,
        ]
        rows: list[Tuple[int, datetime, str]] = self._call_proc("getUserNotificationByGUID", args)
        for row in rows:
            notification: UserNotification = UserNotification(
                index=row[0], timestamp=row[1], event=UserEvent.parse_raw(row[2])
            )
            notifications.append(notification)
        return UserNotifications(notifications=notifications)

    def user_population_by_guid_get(self, user_guid: str) -> UserPopulation:
        rows: list[Tuple[int]] = self._call_proc(
            "getUserPopulationByGUID",
            [
                user_guid,
            ],
        )
        return UserPopulation(population=rows[0][0])

    def user_stores_get(self, user_guid: str) -> UserStores:
        stores: list[UserStore] = []

        args: list[str, int] = [
            user_guid,
        ]
        rows: list[Tuple[str, Optional[str], int]] = self._call_proc("getUserStoresByGUID", args)
        for row in rows:
            stores.append(UserStore(name=row[0], description=row[1], amount=row[2]))
        return UserStores(stores=stores)

    def user_transport(self, user_guid: str, location: str) -> UserFeature:
        args: list = [user_guid, location]
        rows: list[Tuple[str, Optional[str]]] = self._call_proc("transportUserByGUID", args)
        if len(rows) != 1:
            raise IncorrectRowCountError(f"Result count was not exactly one. Received: {rows}")
        location_tuple: Tuple[str, Optional[str]] = rows[0]
        location: UserFeature = UserFeature(name=location_tuple[0], description=location_tuple[1])
        return location

    # Utility functions

    def process_action_queue(self, action_queue: ActionQueue) -> None:
        for action in action_queue.queue:
            self._call_proc(action.name, action.arguments)

    # pylint: disable=duplicate-code
    def _call_proc(self, name: str, args: list, debug: bool = False) -> Optional[list[Tuple]]:
        if debug:
            logging.debug("[DAO] [Stored Proc Call Details] Name: {%s}, Arguments: {%s}", name, args)
        rows: Optional[list[Tuple]] = None
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            cursor.callproc(name, args)
            for result in cursor.stored_results():
                rows = result.fetchall()
            cursor.close()
        except socket.error as error:
            logging.debug(error)
            raise error
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.debug("Something is wrong with your user name or password")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                logging.debug("Database does not exist")
            else:
                logging.debug(error)
            raise error
        else:
            cnx.close()

        if debug:
            logging.debug("[DAO] [Stored Proc Call Details] Returning:")
            logging.debug(rows)
        return rows
