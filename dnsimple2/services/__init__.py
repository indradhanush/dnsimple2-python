# This has to be above all the imports
from dnsimple2.services.base import BaseService

from dnsimple2.services.accounts import AccountService
from dnsimple2.services.certificates import CertificateService
from dnsimple2.services.domains import DomainService
from dnsimple2.services.whoami import WhoAmIService
