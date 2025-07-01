# Portal Language File - Traditional Chinese (Taiwan)

## Overview
Traditional Chinese (Taiwan) language localization file for the ConnectSmart Portal application, providing comprehensive translations for Traditional Chinese-speaking users across all mobility platform features including carpooling, transit, wallet, and notification systems.

## File Details
- **Location**: `/applications/portal/languages/zh-tw.py`
- **Type**: Python Language Dictionary
- **Language Code**: `zh-tw`
- **Language Name**: 中文 (Chinese)
- **Total Entries**: 503 translation entries

## Language Structure

### System-Required Entries
Framework and system messages (lines 3-294) that remain untranslated per requirements:
- Language metadata and web2py framework messages
- Database operation responses
- Cache and administration interface
- Error logs and system debugging

### Application-Specific Translations

#### Authentication & User Management
```python
'Duplicate Email': '另一個用戶已經使用過此電子郵件，請嘗試使用其他電子郵件來註冊帳戶。'
'Email verification': '電子郵件驗證'
'User not found': '找不到使用者'
'Wrong password': '密碼錯誤'
```

#### Carpooling & Trip Management
```python
'Oh no! Your driver %(first_name)s has cancelled the carpooling trip.': '喔不！您的司機 %(first_name)s 已取消此趟共乘行程'
'You have a new match!': '一個新媒合對象'
'Your trip with %(first_name)s is complete. Total %(chip_in)s Coins have been added to your Wallet!': '您與 %(first_name)s 的共乘已完成。 %(chip_in)s 美元硬幣已添加到您的錢包中！'
```

#### Financial & Wallet Features
```python
'Coins balance not enough for escrow, there\'re %(short)s short.': '錢幣不足，尚需%(short)s，無法扣保證金'
'TWD': '台幣'
'USD': '美金'
'Coin product not found': '找不到錢幣商品項目'
```

#### Trip States & Driver Communication
```python
'Driver Has Arrived': '司機已抵達'
'Driver Is Approaching': '司機即將抵達'
'En Route': '在路途中'
'Arriving Now': '已經抵達'
```

#### Group & Enterprise Features
```python
'Congratulations! You\'ve officially joined the %(group_name)s carpooling group!': '恭喜！您已成功加入 %(group_name)s 共乘群組！'
'The group %(group_name)s has been disbanded.': '群組 %(group_name)s 已解散'
'No same group': '沒有相同的共乘群組'
```

## Key Features

### 1. Traditional Chinese Localization
- **Traditional Characters**: Uses Traditional Chinese characters (繁體中文)
- **Taiwan Terminology**: Taiwan-specific terms and expressions
- **Currency Support**: Local currency (台幣/TWD) and international (美金/USD)
- **Cultural Context**: Appropriate formality levels for service interactions

### 2. Transportation Terminology
```python
'driver': '司機'
'Driver': '司機'
'rider': '乘客'
'Passenger': '乘客'
'Carpooling': '共乘'
'Trip': '行程'
'共乘群組': 'Carpooling group'
```

### 3. Formal Communication Style
Maintains professional and respectful tone:
```python
'請點擊下方按鈕驗證您的 Email 信箱': 'Please click the button below to verify your email address'
'請盡快回覆': 'Please reply soon'
'感謝您使用': 'Thank you for using'
```

### 4. Financial & Transaction Language
```python
'錢幣不足': 'Insufficient coins'
'交易失敗': 'Transaction failed'
'信用卡': 'Credit card'
'錢包': 'Wallet'
'儲值': 'Recharge/Top-up'
```

## Language Characteristics

### 1. Time & Location Expressions
Traditional Chinese expressions for temporal and spatial concepts:
```python
'%(first_name)s 將於五分鐘內抵達': '%(first_name)s will arrive within 5 minutes'
'司機已出發': 'Driver has departed'
'即將抵達': 'Arriving soon'
```

### 2. Status & State Descriptions
Clear status communication in Traditional Chinese:
```python
'共乘行程開始': 'Carpooling trip begin'
'共乘行程完成': 'Carpooling trip complete'
'共乘取消': 'Carpooling cancelled'
```

### 3. Error Messages & System Feedback
```python
'參數錯誤': 'Invalid parameters'
'此電子信箱已被其他帳號使用': 'This email has already been used'
'電話號碼已使用': 'Phone number already in use'
'城市不在支持範圍': 'City not in our support range'
```

## Advanced Translation Features

### 1. Contextual Notifications
Detailed notification messages maintaining context:
```python
'因為我們無法確認您加入此趟共乘，因此您的車資錢幣已被退回': 'Because we could not confirm that you joined this carpool, your trip fee coins have been refunded'
```

### 2. Multi-Scenario Cancellation Messages
Comprehensive cancellation reasons with appropriate Chinese expressions:
```python
'您已發送邀請的司機 %(first_name)s 由於地點更改，已取消此趟共乘行程': 'The driver %(first_name)s you invited has cancelled this carpool trip due to location changes'
'您已發送邀請的司機 %(first_name)s 由於時間更改，已取消此趟共乘行程': 'The driver %(first_name)s you invited has cancelled this carpool trip due to time changes'
```

### 3. Business Logic Integration
```python
'找不到共乘群組': 'DUO group not found'
'共乘預訂不支持更新': 'DUO reservation does not support updates'
'活動類型名稱重複': 'Duplicate activity type name'
```

## Technical Implementation

### 1. Character Encoding
- **UTF-8 Support**: Full Traditional Chinese character support
- **Font Compatibility**: Ensures proper rendering across devices
- **Input Method Support**: Compatible with Traditional Chinese input methods

### 2. Mixed Language Content
Strategic use of English terms where internationally recognized:
```python
'Auto Refill paused': 'Auto Refill paused' # Technical terms maintained
'$%(amount)s Coins have been deposited': '$%(amount)s Coins have been deposited'
'Trip Completed': 'Trip Completed'
```

### 3. Regional Considerations
Taiwan-specific terminology and cultural elements:
```python
'台幣': 'TWD (Taiwan Dollar)'
'美金': 'USD (US Dollar)'
'驗證碼': 'Verification code'
```

## Integration Points

### Mobile Application Support
- Traditional Chinese input and display
- Push notifications in Traditional Chinese
- Error handling and user guidance
- Financial transaction confirmations

### Web Portal Interface
- Form validation in Traditional Chinese
- Navigation and menu translations
- User feedback and system messages
- Help and support content

### Communication Systems
- Email templates in Traditional Chinese
- SMS notifications
- Customer support communications
- Account verification processes

## Translation Quality Standards

### 1. Cultural Appropriateness
Maintains Taiwan cultural context and communication norms:
```python
'歡迎加入!': 'Welcome to join!'
'恭喜！您已成功加入': 'Congratulations! You have successfully joined'
```

### 2. Technical Accuracy
Precise translation of technical concepts while maintaining clarity:
```python
'共乘驗證失敗': 'Carpool verification failed'
'時間無法匹配': 'Time cannot be matched'
'群組管理者': 'Group manager'
```

### 3. User Experience Focus
Clear, actionable language for optimal user experience:
```python
'立即開啟 App': 'Open the App now'
'驗證 Email 信箱': 'Verify email address'
'申請加入群組': 'Apply to join group'
```

## Dependencies
- **Python**: Dictionary-based language file with UTF-8 encoding
- **web2py Framework**: T() translation function with Traditional Chinese support
- **Portal Controllers**: Traditional Chinese language key mapping
- **Font Systems**: Traditional Chinese font rendering support

## Usage Example
```python
# Basic translation
T('You have a new match!') # Returns: "一個新媒合對象"

# With parameters
T('Oh no! Your driver %(first_name)s has cancelled the carpooling trip.', 
  dict(first_name='王小明')) 
# Returns: "喔不！您的司機 王小明 已取消此趟共乘行程"

# Financial notifications
T('Coins balance not enough for escrow, there\'re %(short)s short.', 
  dict(short='5'))
# Returns: "錢幣不足，尚需5，無法扣保證金"
```

This Traditional Chinese language file provides comprehensive localization for Traditional Chinese-speaking users, particularly those in Taiwan, ensuring culturally appropriate and linguistically accurate communication across all ConnectSmart mobility platform features.