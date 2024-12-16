from sqlalchemy.orm import registry

table_mapper = registry()

from salonsuite.models.service_category import ServiceCategory
from salonsuite.models.service import Service
from salonsuite.models.status import Status
from salonsuite.models.users import Users
