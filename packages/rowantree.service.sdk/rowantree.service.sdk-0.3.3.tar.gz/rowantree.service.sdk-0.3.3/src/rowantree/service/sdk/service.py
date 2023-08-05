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

from .commands.action_queue_process import ActionQueueProcessCommand
from .commands.health_get import HealthGetCommand
from .commands.merchant_transforms_perform import MerchantTransformPerformCommand
from .commands.user.active_get import UserActiveGetCommand
from .commands.user.active_set import UserActiveSetCommand
from .commands.user.create import UserCreateCommand
from .commands.user.delete import UserDeleteCommand
from .commands.user.feature_active_get import UserFeatureActiveGetCommand
from .commands.user.features_get import UserFeaturesGetCommand
from .commands.user.income_get import UserIncomeGetCommand
from .commands.user.income_set import UserIncomeSetCommand
from .commands.user.merchant_transforms_get import UserMerchantTransformsGetCommand
from .commands.user.population_get import UserPopulationGetCommand
from .commands.user.state_get import UserStateGetCommand
from .commands.user.stores_get import UserStoresGetCommand
from .commands.user.transport import UserTransportCommand
from .commands.world_get import WorldStatusGetCommand
from .common.config import Config
from .contracts.requests.merchant_transform import MerchantTransformRequest
from .contracts.requests.user.income_set import UserIncomeSetRequest
from .contracts.requests.user.transport import UserTransportRequest


# pylint: disable=too-many-instance-attributes
class RowanTreeService:
    config: Config

    user_active_get_command: UserActiveGetCommand
    user_active_set_command: UserActiveSetCommand

    user_create_command: UserCreateCommand
    user_delete_command: UserDeleteCommand

    user_feature_active_get_command: UserFeatureActiveGetCommand
    user_features_get_command: UserFeaturesGetCommand

    user_income_get_command: UserIncomeGetCommand
    user_income_set_command: UserIncomeSetCommand

    user_merchant_transforms_get_command: UserMerchantTransformsGetCommand
    user_population_get_command: UserPopulationGetCommand
    user_state_get_command: UserStateGetCommand
    user_stores_get_command: UserStoresGetCommand
    user_transport_command: UserTransportCommand

    merchant_transform_perform_command: MerchantTransformPerformCommand
    action_queue_process_command: ActionQueueProcessCommand
    health_get_command: HealthGetCommand
    world_status_get_command: WorldStatusGetCommand

    def __init__(self):
        self.config = Config()

        self.user_active_get_command = UserActiveGetCommand(config=self.config)
        self.user_active_set_command = UserActiveSetCommand(config=self.config)

        self.user_create_command = UserCreateCommand(config=self.config)
        self.user_delete_command = UserDeleteCommand(config=self.config)

        self.user_feature_active_get_command = UserFeatureActiveGetCommand(config=self.config)
        self.user_features_get_command = UserFeaturesGetCommand(config=self.config)

        self.user_income_get_command = UserIncomeGetCommand(config=self.config)
        self.user_income_set_command = UserIncomeSetCommand(config=self.config)

        self.user_merchant_transforms_get_command = UserMerchantTransformsGetCommand(config=self.config)
        self.user_population_get_command = UserPopulationGetCommand(config=self.config)
        self.user_state_get_command = UserStateGetCommand(config=self.config)
        self.user_stores_get_command = UserStoresGetCommand(config=self.config)
        self.user_transport_command = UserTransportCommand(config=self.config)

        self.merchant_transform_perform_command = MerchantTransformPerformCommand(config=self.config)
        self.health_get_command = HealthGetCommand(config=self.config)
        self.action_queue_process_command = ActionQueueProcessCommand(config=self.config)
        self.world_status_get_command = WorldStatusGetCommand(config=self.config)

    # User Commands

    def user_active_get(self, user_guid: str) -> UserActive:
        return self.user_active_get_command.execute(user_guid=user_guid)

    def user_active_set(self, user_guid: str, active: bool) -> UserActive:
        request: UserActive = UserActive(active=active)
        return self.user_active_set_command.execute(user_guid=user_guid, request=request)

    def user_create(self) -> User:
        return self.user_create_command.execute()

    def user_delete(self, user_guid: str) -> None:
        self.user_delete_command.execute(user_guid=user_guid)

    def user_feature_active_get(self, user_guid: str, details: bool) -> UserFeature:
        return self.user_feature_active_get_command.execute(user_guid=user_guid, details=details)

    def user_features_get(self, user_guid: str) -> UserFeatures:
        return self.user_features_get_command.execute(user_guid=user_guid)

    def user_income_get(self, user_guid: str) -> UserIncomes:
        return self.user_income_get_command.execute(user_guid=user_guid)

    def user_income_set(self, user_guid: str, income_source_name: str, amount: int) -> None:
        request: UserIncomeSetRequest = UserIncomeSetRequest(income_source_name=income_source_name, amount=amount)
        self.user_income_set_command.execute(user_guid=user_guid, request=request)

    def user_merchant_transforms_get(self, user_guid: str) -> UserMerchants:
        return self.user_merchant_transforms_get_command.execute(user_guid=user_guid)

    def user_population_get(self, user_guid: str) -> UserPopulation:
        return self.user_population_get_command.execute(user_guid=user_guid)

    def user_state_get(self, user_guid: str) -> UserState:
        return self.user_state_get_command.execute(user_guid=user_guid)

    def user_stores_get(self, user_guid: str) -> UserStores:
        return self.user_stores_get_command.execute(user_guid=user_guid)

    def user_transport(self, user_guid: str, location: str) -> UserFeature:
        request: UserTransportRequest = UserTransportRequest(location=location)
        return self.user_transport_command.execute(user_guid=user_guid, request=request)

    # Merchant Commands

    def merchant_transform_perform(self, user_guid: str, store_name: str) -> None:
        request: MerchantTransformRequest = MerchantTransformRequest(store_name=store_name)
        self.merchant_transform_perform_command.execute(user_guid=user_guid, request=request)

    # Admin Commands

    def health_get(self) -> bool:
        return self.health_get_command.execute()

    def action_queue_process(self, queue: ActionQueue) -> None:
        self.action_queue_process_command.execute(request=queue)

    def world_status_get(self) -> WorldStatus:
        return self.world_status_get_command.execute()
