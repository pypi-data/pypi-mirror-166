from datetime import datetime


class APIs:
    """For IDE prompting (instead of entering API addresses all over the place), define what endpoints the system will use endpoints here."""
    def __init__(
        self,
        domain: str            = "",
        gql: str               = "/api/gql/query",
        file_uploads: str      = "/api/gql/query",
        consumer_login: str    = "/api/auth/customer/login",
        consumer_register: str = "/api/auth/customer/register",
        brand_login: str       = "/api/auth/login",
        brand_register: str    = "/api/auth/member/register",
    ) -> None:
        self.gql                = domain.strip('/') + gql
        self.file_uploads       = domain.strip('/') + file_uploads
        self.consumer_login     = domain.strip('/') + consumer_login
        self.consumer_register  = domain.strip('/') + consumer_register
        self.brand_login        = domain.strip('/') + brand_login
        self.brand_register     = domain.strip('/') + brand_register

class Profile:
    def __init__(
        self,
        referralCode: str | None = None,
        walletPoints: int = None,
        dateOfBirth: str = None,
        gender: str = None,
        createdAt: datetime = None,
    ) -> None:
        self.referralCode = referralCode
        self.walletPoints = walletPoints
        self.dateOfBirth = dateOfBirth
        self.gender = gender
        self.createdAt = createdAt

class User:
    def __init__(
        self,
        id: str | int = None,
        email: str = None,
        firstName: str = None,
        lastName: str = None,
        phone: str = None,
        userType: str = None,
        isAdmin: bool = None,
        isMember: bool = None,
        isCustomer: bool = None,
        # address: Address = None, # TODO: Address class
        organization_id: str | int = None,
        role_name: str = None,
        affiliateOrganization_id: str | int = None,
        profile: Profile = None,
        createdAt: datetime = None,
        # trackActions: list[TrackAction] = None, # TODO: TrackAction class
        isFieldappAccess: bool = None,
        isPlatformAccess: bool = None,
    ) -> None:
        self.id = id
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.userType = userType
        self.isAdmin = isAdmin
        self.isMember = isMember
        self.isCustomer = isCustomer
        self.organization_id = organization_id
        self.role_name = role_name
        self.affiliateOrganization_id = affiliateOrganization_id
        self.profile = profile
        self.createdAt = createdAt
        self.isFieldappAccess = isFieldappAccess
        self.isPlatformAccess = isPlatformAccess

