# Re-export the project-wide fixtures (tests/conftest.py applies only below tests/).
import pytest

from integrations.models import ApiScope, ExternalSystem
from integrations.services import create_api_key
from tests.conftest import *  # noqa: F401,F403
from tests.conftest import _clear_caches  # noqa: F401


@pytest.fixture
def system(db):
    return ExternalSystem.objects.create(key="crm", name="CRM", inbound_secret_env="ILE_TEST_WEBHOOK_SECRET")


@pytest.fixture
def other_system(db):
    return ExternalSystem.objects.create(key="other", name="Other")


@pytest.fixture
def api_key(db, system):
    key, raw = create_api_key("test", [ApiScope.EVENTS_READ, ApiScope.EVENTS_ACK], system=system)
    return key, raw


@pytest.fixture
def auth(api_key):
    return {"HTTP_AUTHORIZATION": f"Bearer {api_key[1]}"}
