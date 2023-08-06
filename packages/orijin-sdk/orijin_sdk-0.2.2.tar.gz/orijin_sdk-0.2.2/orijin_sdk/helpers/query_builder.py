"""This builder simply provides typing for IDE prompting and default input values for a few common queries"""

from enum import Enum

from orijin_sdk.types import Profile, User

class FilterOption(Enum):
	All = "All"
	Active = "Active"
	Archived = "Archived"
	ProductWithoutOrder = "ProductWithoutOrder"
	ProductWithoutCarton = "ProductWithoutCarton"
	ProductWithoutSKU = "ProductWithoutSKU"
	CartonWithoutPallet = "CartonWithoutPallet"
	PalletWithoutContainer = "PalletWithoutContainer"
	System = "System"
	Blockchain = "Blockchain"
	Pending = "Pending"

class SortByOption(Enum):
	DateCreated = "DateCreated"
	DateUpdated = "DateUpdated"
	Alphabetical = "Alphabetical"

class SortDir(Enum):
	Ascending = "Ascending"
	Descending = "Descending"

class Search:
	search: str | None
	filter: FilterOption | None
	sortBy: SortByOption | None
	sortDir: SortDir | None

	def __init__(
		self,
		search: str = None,
		filter: FilterOption = None,
		sortBy: SortByOption = None,
		sortDir: SortDir = None
	):
		self.search  = search
		self.filter  = filter
		self.sortBy  = sortBy
		self.sortDir = sortDir

def skus(request_fields = "total, skus { id }", search: Search={}, limit: int=100, offset: int=0, isPointBound: bool=None, isApproved: bool=None):
	query = """
query skus($search: SearchFilter!, $limit: Int!, $offset: Int!, $isPointBound: Boolean, $isApproved: Boolean) {{
	skus(search: $search, limit: $limit, offset: $offset, isPointBound: $isPointBound, isApproved: $isApproved) {{
		__typename
		{0}
	}}
}}""".format(request_fields)

	variables = {
		'search': search,
		'limit': limit,
		'offset': offset,
		'isPointBound': isPointBound,
		'isApproved': isApproved,
	}

	return query, variables

def products(request_fields = "total, products { id }", search: Search={}, limit: int=100, offset: int=0, cartonID: int=None, orderID: int=None, skuID: int=None, contractID: int=None):
	query = """
query products(
		$search: SearchFilter!
		$limit: Int!
		$offset: Int!
		$cartonID: ID
		$orderID: ID
		$skuID: ID
		$contractID: ID
	) {{
		products(
			search: $search
			limit: $limit
			offset: $offset
			isPointBound: false
			skuID: $skuID
			orderID: $orderID
			cartonID: $cartonID
			contractID: $contractID
		) {{
			__typename
			{0}
		}}
	}}
""".format(request_fields)

	variables = {
		'search': search,
		'limit': limit,
		'offset': offset,
		'cartonID': cartonID,
		'orderID': orderID,
		'skuID': skuID,
		'contractID': contractID,
	}

	return query, variables

def me(request_fields = """
	id
	email
	firstName
	lastName
	phone
	userType
	isAdmin
	isMember
	isCustomer
	# address: Address
	organization { id }
	role { name }
	affiliateOrganization { organization { id } }
	profile {
		referralCode
		walletPoints
		dateOfBirth
		gender
		createdAt
	}
	createdAt
	# trackActions: [TrackAction!]!
	isFieldappAccess
	isPlatformAccess
	"""
):
	query = """
	query me {{
		me {{
			__typename
			{0}
		}}
	}}""".format(request_fields)

	variables = {}

	def decoder(json_result):
		try:
			org_id = json_result["data"]["me"]["organization"]["id"]
		except:
			org_id = None
		
		try:
			affiliateOrganization_id = json_result["data"]["me"]["affiliateOrganization"]["organization"]["id"]
		except:
			affiliateOrganization_id = None
		
		try:
			profile = Profile(
				json_result["data"]["me"]["profile"]["referralCode"],
				json_result["data"]["me"]["profile"]["wallerPoints"],
				json_result["data"]["me"]["profile"]["dateOfBirth"],
				json_result["data"]["me"]["profile"]["gender"],
				json_result["data"]["me"]["profile"]["createdAt"]
			)
		except:
			profile = None
		
		try:
			role_name = json_result["data"]["me"]["role"]["name"]
		except:
			role_name = None

		return User(
			id = json_result["data"]["me"]["id"],
			email = json_result["data"]["me"]["email"],
			firstName = json_result["data"]["me"]["firstName"],
			lastName = json_result["data"]["me"]["lastName"],
			phone = json_result["data"]["me"]["phone"],
			userType = json_result["data"]["me"]["userType"],
			isAdmin = json_result["data"]["me"]["isAdmin"],
			isMember = json_result["data"]["me"]["isMember"],
			isCustomer = json_result["data"]["me"]["isCustomer"],
			organization_id = org_id,
			role_name = role_name,
			affiliateOrganization_id = affiliateOrganization_id,
			profile = profile,
			createdAt = json_result["data"]["me"]["createdAt"],
			isFieldappAccess = json_result["data"]["me"]["isFieldappAccess"],
			isPlatformAccess = json_result["data"]["me"]["isPlatformAccess"],
		)

	return query, variables, decoder
