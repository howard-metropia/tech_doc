# TSP API Welcome Coin Controller Documentation

## 🔍 Quick Summary (TL;DR)
The welcome coin controller manages new user welcome bonuses and promotional coin distributions in the TSP platform's reward system.

**Keywords:** welcome-coin | user-rewards | promotional-coins | user-onboarding | coin-system | welcome-bonus | reward-distribution | user-incentives

**Primary use cases:** Retrieving welcome coin information, checking eligibility for welcome bonuses, managing new user rewards, onboarding incentives

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, reward/coin management systems

## ❓ Common Questions Quick Index
- **Q: What are welcome coins?** → Promotional coins given to new users as onboarding incentives
- **Q: How do I check welcome coin status?** → GET `/api/v2/welcome_coin` with authentication
- **Q: Is authentication required?** → Yes, JWT authentication with user context
- **Q: When are welcome coins awarded?** → Based on service logic for new user onboarding
- **Q: Can users claim multiple welcome bonuses?** → Depends on service implementation rules
- **Q: What happens after claiming?** → Service handles coin distribution and eligibility updates

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as the **welcome gift counter** for new users of the transportation app. When someone joins the platform, they might be eligible for free coins or credits as a welcome bonus - like getting a coupon when you sign up for a new service. This controller checks if you have any welcome gifts waiting and helps you claim them.

**Technical explanation:** 
A minimal Koa.js REST controller that provides welcome coin information for authenticated users. It extracts user context from headers and delegates to the welcome coin service to determine eligibility, available amounts, and claim status for new user promotional rewards.

**Business value explanation:**
Essential for user acquisition and onboarding optimization. Welcome coins incentivize new user registration, improve initial user engagement, reduce onboarding friction, and support user retention strategies through immediate value delivery in the platform's reward ecosystem.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/welcomeCoin.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** User Rewards Controller
- **File Size:** ~0.6 KB
- **Complexity Score:** ⭐ (Low - Single endpoint with service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@app/src/helpers/fields-of-header`: Header field extraction (**High**)
- `@app/src/services/welcomeCoin`: Welcome coin business logic (**Critical**)

## 📝 Detailed Code Analysis

### Get Welcome Coin Endpoint (`GET /welcome_coin`)

**Purpose:** Retrieves welcome coin information and eligibility for the authenticated user

**Processing Flow:**
1. **Authentication:** JWT validation via auth middleware
2. **Header Processing:** Extracts user ID from request headers
3. **Service Delegation:** Calls welcome coin service for user-specific data
4. **Response:** Returns welcome coin information in standardized format

**Implementation:**
```javascript
router.get('getWelcomeCoin', '/welcome_coin', auth, bodyParser(), async (ctx) => {
  const { userId } = fetchFieldsFromHeader(ctx.request.header);
  const result = await service.get(userId);
  ctx.body = success(result);
});
```

**Data Flow:**
- **Headers → User Context:** Extract userId from authenticated request
- **Service Call → Business Logic:** Delegate to service for welcome coin processing
- **Response → Client:** Return welcome coin status and details

## 🚀 Usage Methods

### Check Welcome Coin Status
```bash
curl -X GET "https://api.tsp.example.com/api/v2/welcome_coin" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### JavaScript Client Example
```javascript
async function getWelcomeCoin(authToken, userId) {
  try {
    const response = await fetch('/api/v2/welcome_coin', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId
      }
    });
    
    const result = await response.json();
    
    if (result.result === 'success') {
      console.log('Welcome coin information:', result.data);
      return result.data;
    } else {
      console.error('Failed to get welcome coin info:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Welcome coin request error:', error);
    throw error;
  }
}

// Usage example
getWelcomeCoin(authToken, 'usr_12345').then(coinInfo => {
  if (coinInfo.eligible) {
    console.log(`Welcome bonus available: ${coinInfo.amount} coins`);
    // Show welcome bonus UI
  } else {
    console.log('No welcome bonus available');
  }
});
```

### React Component Example
```javascript
function WelcomeCoinBanner({ authToken, userId }) {
  const [coinInfo, setCoinInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchWelcomeCoin() {
      try {
        setLoading(true);
        const response = await fetch('/api/v2/welcome_coin', {
          headers: {
            'Authorization': `Bearer ${authToken}`,
            'userid': userId
          }
        });
        
        const result = await response.json();
        
        if (result.result === 'success') {
          setCoinInfo(result.data);
        } else {
          setError(result.error);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    if (authToken && userId) {
      fetchWelcomeCoin();
    }
  }, [authToken, userId]);

  if (loading) return <div>Loading welcome bonus...</div>;
  if (error) return null; // Fail silently for non-critical feature
  if (!coinInfo?.eligible) return null;

  return (
    <div className="welcome-coin-banner">
      <h3>🎉 Welcome Bonus Available!</h3>
      <p>Claim your {coinInfo.amount} welcome coins</p>
      <button onClick={() => claimWelcomeCoins(coinInfo.claimId)}>
        Claim Now
      </button>
    </div>
  );
}
```

### Integration with Onboarding Flow
```javascript
class OnboardingManager {
  constructor(authToken, userId) {
    this.authToken = authToken;
    this.userId = userId;
  }

  async completeOnboarding() {
    try {
      // Complete other onboarding steps...
      
      // Check for welcome bonus
      const welcomeCoins = await this.getWelcomeCoin();
      
      if (welcomeCoins.eligible) {
        // Show welcome bonus notification
        this.showWelcomeBonus(welcomeCoins);
      }
      
      // Continue with onboarding flow
      this.proceedToMainApp();
      
    } catch (error) {
      console.error('Onboarding completion error:', error);
      // Continue even if welcome coin check fails
      this.proceedToMainApp();
    }
  }

  async getWelcomeCoin() {
    const response = await fetch('/api/v2/welcome_coin', {
      headers: {
        'Authorization': `Bearer ${this.authToken}`,
        'userid': this.userId
      }
    });
    
    const result = await response.json();
    return result.data;
  }

  showWelcomeBonus(coinInfo) {
    // Display welcome bonus UI
    const modal = new WelcomeBonusModal({
      amount: coinInfo.amount,
      description: coinInfo.description,
      onClaim: () => this.claimWelcomeCoins(coinInfo.claimId)
    });
    modal.show();
  }
}
```

## 📊 Output Examples

### Welcome Coin Available
```json
{
  "result": "success",
  "data": {
    "eligible": true,
    "amount": 100,
    "currency": "coins",
    "description": "Welcome to TSP! Enjoy 100 free coins to get started with premium features.",
    "claimId": "welcome_claim_abc123",
    "expiresAt": "2024-07-25T14:30:00Z",
    "claimed": false,
    "claimedAt": null,
    "rules": {
      "newUserOnly": true,
      "oneTimeOffer": true,
      "expirationDays": 30
    }
  }
}
```

### Already Claimed
```json
{
  "result": "success",
  "data": {
    "eligible": false,
    "amount": 100,
    "currency": "coins",
    "description": "Welcome bonus previously claimed",
    "claimId": "welcome_claim_abc123",
    "expiresAt": "2024-07-25T14:30:00Z",
    "claimed": true,
    "claimedAt": "2024-06-20T10:15:00Z",
    "rules": {
      "newUserOnly": true,
      "oneTimeOffer": true,
      "expirationDays": 30
    }
  }
}
```

### Not Eligible
```json
{
  "result": "success",
  "data": {
    "eligible": false,
    "amount": 0,
    "currency": "coins",
    "description": "Welcome bonus not available for this account",
    "claimId": null,
    "expiresAt": null,
    "claimed": false,
    "claimedAt": null,
    "reason": "account_too_old",
    "rules": {
      "newUserOnly": true,
      "oneTimeOffer": true,
      "expirationDays": 30
    }
  }
}
```

### Expired Offer
```json
{
  "result": "success",
  "data": {
    "eligible": false,
    "amount": 100,
    "currency": "coins",
    "description": "Welcome bonus offer has expired",
    "claimId": "welcome_claim_abc123",
    "expiresAt": "2024-06-15T14:30:00Z",
    "claimed": false,
    "claimedAt": null,
    "reason": "expired",
    "rules": {
      "newUserOnly": true,
      "oneTimeOffer": true,
      "expirationDays": 30
    }
  }
}
```

### Authentication Error
```json
{
  "error": "AuthenticationError",
  "message": "Invalid or expired JWT token",
  "code": 401
}
```

## ⚠️ Important Notes

### Welcome Coin Rules
Common welcome coin eligibility criteria:
- **New Users Only:** Typically limited to first-time users
- **One-Time Offer:** Usually can only be claimed once per user
- **Time Limits:** Often expire after a certain period
- **Account Status:** May require verified or active accounts
- **Geographic Restrictions:** May be limited to certain regions

### Business Logic Considerations
- **Fraud Prevention:** Service should validate user eligibility
- **Audit Trail:** Track all welcome coin distributions
- **A/B Testing:** Different welcome amounts for testing
- **Campaign Management:** Support for promotional campaigns
- **Budget Controls:** Limits on total welcome coin distributions

### Integration Points
- **User Registration:** Welcome coins often triggered during signup
- **Onboarding Flow:** Part of new user experience
- **Notification System:** Alerts users about available bonuses
- **Wallet Integration:** Coins added to user's digital wallet
- **Analytics:** Track conversion and engagement metrics

### Service Layer Responsibilities
The welcome coin service likely handles:
- **Eligibility Checking:** Complex business rules for qualification
- **Expiration Management:** Time-based offer validity
- **Claim Processing:** Actual coin distribution
- **Fraud Detection:** Preventing abuse and duplicate claims
- **Campaign Configuration:** Managing different welcome offers

### Error Handling
- **Service Errors:** Handle service unavailability gracefully
- **Authentication Issues:** Proper error responses for auth failures
- **Rate Limiting:** Prevent excessive welcome coin checks
- **Data Consistency:** Ensure atomic claim operations

### Performance Considerations
- **Caching:** Service may cache eligibility results
- **Lightweight Endpoint:** Minimal processing in controller
- **Fast Response:** Quick eligibility checks for good UX
- **Scalability:** Handle high volume during user acquisition campaigns

### User Experience
- **Clear Messaging:** Explain welcome coin benefits clearly
- **Easy Claiming:** Simple claim process for users
- **Transparency:** Show eligibility rules and expiration
- **Immediate Value:** Quick coin delivery after claiming

## 🔗 Related File Links

- **Welcome Coin Service:** `allrepo/connectsmart/tsp-api/src/services/welcomeCoin.js`
- **Header Helper:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Related Controllers:** Wallet and coin management controllers

---
*This controller provides essential welcome bonus functionality for user onboarding and retention in the TSP platform's reward system.*