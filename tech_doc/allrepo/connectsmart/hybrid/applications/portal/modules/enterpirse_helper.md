# Enterprise Helper Module - ConnectSmart Portal

🔍 **Quick Summary (TL;DR)**
- HTTP client wrapper for enterprise employee verification, trip pricing, green points, and telework management API integration
- enterprise | employee-verification | trip-pricing | telework | green-points | api-client | http-requests
- Used for validating enterprise users, calculating trip costs, managing telework policies, and fetching sustainability metrics
- Compatible with enterprise API endpoints, supports localized responses, requires configured enterprise service URL

❓ **Common Questions Quick Index**
- Q: How do I verify enterprise employees? → See [Usage Methods](#usage-methods)
- Q: What trip pricing calculations are available? → See [Detailed Code Analysis](#detailed-code-analysis)
- Q: How do I handle API errors? → See [Output Examples](#output-examples)
- Q: What telework features are supported? → See [Detailed Code Analysis](#detailed-code-analysis)
- Q: How are green points calculated? → See [Usage Methods](#usage-methods)
- Q: What headers are required for API calls? → See [Technical Specifications](#technical-specifications)
- Q: How do I configure the enterprise service URL? → See [Technical Specifications](#technical-specifications)
- Q: What's the difference between verification types? → See [Important Notes](#important-notes)

📋 **Functionality Overview**
- **Non-technical explanation:** Like a specialized translator that communicates with the company's employee database - it checks if someone works at a company, calculates how much they should pay for trips, tracks their environmental impact points, and manages their work-from-home settings. Similar to how an HR system validates employee credentials, or how a corporate travel system calculates expense reimbursements.
- **Technical explanation:** RESTful API client providing enterprise integration services including employee verification, dynamic trip pricing, sustainability metrics, and telework policy management with localized response support.
- **Business value:** Enables seamless enterprise user authentication, accurate cost allocation for corporate mobility programs, and comprehensive telework policy enforcement for large organizations.
- **System context:** Integrates with enterprise identity systems, supports carpool verification workflows, and provides backend services for enterprise portal features within the ConnectSmart platform.

🔧 **Technical Specifications**
- **File info:** `enterpirse_helper.py` (note: filename typo), 108 lines, Python API client class, medium complexity
- **Dependencies:**
  - `requests` (external): HTTP client library for API communication (critical)
  - `logging` (built-in): Debug and error logging capabilities
  - `urllib.parse.quote` (built-in): URL encoding for email parameters
  - `gluon.current` (Web2py): Framework context for request headers
- **Compatibility:** RESTful enterprise API services, Web2py framework integration, HTTP/HTTPS protocols
- **Configuration:** Enterprise service base URL (constructor parameter)
- **Request headers:** Content-Type: application/json, Accept-Language from client request
- **System requirements:** Network connectivity to enterprise API endpoints, proper authentication setup
- **Security:** Relies on enterprise API authentication, email parameter encoding prevents injection

📝 **Detailed Code Analysis**
```python
class EnterpriseHelper:
    """Enterprise API integration client for employee and telework services"""
    
    def __init__(self, url):
        self.url = url  # Base URL for enterprise API endpoints
        
    def get_enterprise(self, email, user_id, verify_type="carpooling"):
        """Verify enterprise employee membership and get company information"""
        # GET /employee/getEnterpriseInfo with email verification
        # Supports verification types: "carpooling", "trip_log", custom types
        
    def get_suggested_price(self, distance, currency):
        """Calculate recommended trip pricing based on distance and currency"""
        # GET /employee/TripPrice with distance in meters and country currency
        # Returns structured pricing data with failure detection
        
    def get_green_point(self):
        """Retrieve sustainability green points information"""
        # GET /employee/getGreenPoints for environmental impact metrics
        # Handles API success/failure response format variations
        
    def get_enterprise_telework(self, user_id):
        """Get user's enterprise telework configuration"""
        # GET /Telework/getMemberEnterprise for telework policy data
        
    def update_telework_enterprise(self, user_id, enterprise_id, is_telework=True):
        """Update user's telework status within enterprise"""
        # POST /Telework/updEnterprisTelework with policy updates
        
    def search_telework_enterprise(self, email, user_id):
        """Search for telework-enabled enterprises by employee email"""
        # POST /Telework/getEnterpriseInfo for telework discovery
```

🚀 **Usage Methods**
```python
from applications.portal.modules.enterpirse_helper import EnterpriseHelper

# Initialize with enterprise API base URL
enterprise_url = "https://enterprise-api.connectsmart.com"
helper = EnterpriseHelper(enterprise_url)

# Employee verification for carpool access
def verify_employee(email, user_id):
    try:
        enterprise_info = helper.get_enterprise(email, user_id, "carpooling")
        return enterprise_info.get('is_verified', False)
    except requests.RequestException as e:
        print(f"Verification failed: {e}")
        return False

# Trip pricing calculation
def calculate_trip_cost(distance_meters, country_code):
    try:
        pricing_data = helper.get_suggested_price(distance_meters, country_code)
        return pricing_data.get('suggested_price', 0.0)
    except requests.RequestException as e:
        print(f"Pricing calculation failed: {e}")
        return None

# Green points sustainability tracking
def get_user_green_points():
    try:
        points_data = helper.get_green_point()
        return points_data.get('total_points', 0)
    except requests.RequestException as e:
        print(f"Green points retrieval failed: {e}")
        return 0

# Telework management workflow
def setup_telework_user(email, user_id, enterprise_id):
    # Search for telework options
    telework_options = helper.search_telework_enterprise(email, user_id)
    
    # Get current telework status
    current_status = helper.get_enterprise_telework(user_id)
    
    # Enable telework if available
    if telework_options:
        result = helper.update_telework_enterprise(user_id, enterprise_id, True)
        return result
```

📊 **Output Examples**
```python
# Successful enterprise verification
>>> helper.get_enterprise("john.doe@company.com", "user123", "carpooling")
{
    'enterprise_id': 'ENT456',
    'company_name': 'Tech Corp',
    'is_verified': True,
    'employee_status': 'active',
    'permissions': ['carpool', 'transit']
}

# Trip pricing calculation
>>> helper.get_suggested_price(5000, "USD")  # 5km trip in USD
{
    'suggested_price': 3.50,
    'currency': 'USD',
    'calculation_method': 'distance_based',
    'base_rate': 0.70
}

# Green points data
>>> helper.get_green_point()
{
    'total_points': 245,
    'monthly_points': 45,
    'carbon_saved_kg': 12.5,
    'trees_equivalent': 0.8
}

# API error scenarios
>>> helper.get_enterprise("invalid@email.com", "user123")
requests.exceptions.RequestException: b'{"error": "Employee not found"}'

# Telework status
>>> helper.get_enterprise_telework("user123")
{
    'enterprise_id': 'ENT456',
    'telework_enabled': True,
    'max_days_per_week': 3,
    'approval_status': 'approved'
}

# Logging output example
[DEBUG] [API] GET https://enterprise-api.com/employee/getEnterpriseInfo 200 
body None res {"data": {...}} 150000 ms
```

⚠️ **Important Notes**
- **API error handling:** Enterprise API returns HTTP 200 with error messages in response body - check `result` field for "fail" status
- **Email encoding:** Email parameters are URL-encoded to handle special characters and prevent injection attacks
- **Language support:** Accept-Language header from client request enables localized API responses
- **Network timeout:** No explicit timeout configuration - requests may hang on network issues
- **Authentication dependency:** Assumes enterprise API handles authentication through other means (API keys, tokens)
- **Verification types:** "carpooling" vs "trip_log" verification may return different permission sets
- **Currency validation:** Trip pricing requires valid ISO currency codes for accurate calculations
- **Telework policies:** Enterprise telework settings may override individual user preferences

🔗 **Related File Links**
- **Integration point:** `enterprise_carpool.py` uses this helper for employee verification workflows
- **Configuration:** Web2py application settings contain enterprise API URL configuration  
- **Database schema:** Enterprise table stores verification tokens and employee status
- **Email templates:** Verification emails reference enterprise information from these API calls
- **Frontend integration:** Portal controllers use this helper for enterprise user management
- **Authentication system:** Enterprise SSO integration may depend on verification results

📈 **Use Cases**
- **Employee onboarding:** Verify new users against corporate directory during account creation
- **Trip cost allocation:** Calculate fair pricing for corporate mobility reimbursement programs
- **Sustainability reporting:** Track and display environmental impact metrics for corporate sustainability goals
- **Telework compliance:** Enforce corporate work-from-home policies and approval workflows
- **Access control:** Determine user permissions based on enterprise membership and verification status
- **Corporate analytics:** Aggregate usage patterns for enterprise mobility program optimization
- **Policy enforcement:** Apply company-specific rules for carpool participation and trip logging

🛠️ **Improvement Suggestions**
- **Timeout configuration:** Add configurable request timeouts to prevent hanging connections
- **Retry mechanism:** Implement exponential backoff retry logic for transient network failures
- **Response caching:** Cache enterprise information to reduce API calls and improve performance
- **Async support:** Add async/await capabilities for better concurrency in high-traffic scenarios
- **Type validation:** Add input parameter validation for email format, distance ranges, currency codes
- **Monitoring integration:** Add structured logging and metrics for API performance monitoring
- **Authentication handling:** Implement proper API key or token-based authentication
- **Circuit breaker:** Add circuit breaker pattern to handle enterprise API outages gracefully

🏷️ **Document Tags**
- **Keywords:** enterprise-integration, employee-verification, trip-pricing, telework-management, green-points, api-client, corporate-mobility, sustainability-metrics, http-requests, localization
- **Technical tags:** `#enterprise` `#api-client` `#employee-verification` `#telework` `#sustainability` `#http` `#requests` `#portal` `#corporate`
- **Target roles:** Enterprise integrators (advanced), backend API developers, corporate mobility specialists, sustainability analysts
- **Difficulty level:** ⭐⭐⭐ (advanced) - Requires understanding of enterprise systems, API integration patterns, and corporate policy management
- **Maintenance level:** Medium - enterprise API endpoint changes, authentication updates, policy requirement changes
- **Business criticality:** High - essential for enterprise customer onboarding and corporate compliance
- **Related topics:** enterprise SSO, corporate mobility, sustainability tracking, telework policies, API integration, employee verification