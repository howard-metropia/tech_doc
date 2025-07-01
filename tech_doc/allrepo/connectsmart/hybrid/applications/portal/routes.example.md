# Portal Routing Configuration Example - Multi-Language URL Routing

## 🔍 Quick Summary (TL;DR)
Web2py routing configuration example for Portal MaaS application enabling language-specific URL routing with automatic language detection and multi-language support for internationalized transportation services.

**Keywords**: `web2py-routing | multi-language-urls | internationalization | i18n-routing | language-detection | url-localization | maas-routing`

**Use Cases**: Multi-language MaaS application deployment, international market support, URL localization, language-based routing

**Compatibility**: Web2py framework 2.15.5+, Portal application, multi-language support

## ❓ Common Questions Quick Index
- Q: How do I enable multi-language routing? → [Setup Instructions](#setup-instructions)
- Q: What languages are supported? → [Language Configuration](#language-configuration)
- Q: How does URL language detection work? → [Language Detection](#language-detection)
- Q: Can I customize language routing? → [Customization Options](#customization-options)
- Q: How do I test language routing? → [Testing Methods](#testing-methods)
- Q: What's the URL structure? → [URL Structure](#url-structure)
- Q: How do I add new languages? → [Adding Languages](#adding-languages)
- Q: What happens without this file? → [Default Behavior](#default-behavior)

## 📋 Functionality Overview
**Non-technical**: Like having automatic translators for different countries - this configuration file tells the transportation app how to show the right language based on the web address users visit, making the service accessible to international users.

**Technical**: Web2py routing configuration implementing language-specific URL patterns (app/lang/controller/function) with automatic language detection from application language files, enabling internationalized MaaS services with localized URLs and content.

**Business Value**: Enables global market expansion by supporting multiple languages in URLs, improves SEO for international markets, enhances user experience for non-English speakers, and facilitates localized marketing campaigns.

**System Context**: Application-level routing configuration for Portal MaaS platform, working with Web2py's global routing system to provide language-aware URL handling and content localization.

## 🔧 Technical Specifications
- **File**: `portal/routes.example.py` (42 lines)
- **Type**: Web2py application routing configuration
- **Dependencies**: Web2py framework, gluon.fileutils, gluon.languages
- **Language Detection**: Automatic from `/languages/` directory
- **URL Pattern**: `app/<language>/controller/function`
- **Activation**: Requires renaming to `routes.py` and global routes configuration

## 📝 Detailed Code Analysis

### Language Detection System
```python
from gluon.fileutils import abspath
from gluon.languages import read_possible_languages

# Automatically detect available languages from application
possible_languages = read_possible_languages(abspath('applications', app))
```

### Router Configuration
```python
routers = {
    app: dict(
        # Set default language from language files
        default_language=possible_languages['default'][0],
        
        # Configure available languages (excluding 'default' key)
        languages=[lang for lang in possible_languages if lang != 'default']
    )
}
```

### Language Activation Pattern
```python
# Enable language forcing in model files
if request.uri_language: 
    T.force(request.uri_language)
```

## 🚀 Usage Methods

### Activation Steps
```bash
# 1. Enable global routing (web2py root)
cp examples/routes.parametric.example.py routes.py

# 2. Enable application routing (portal app)
cp applications/portal/routes.example.py applications/portal/routes.py

# 3. Restart web2py server
sudo systemctl restart web2py
```

### Language File Structure
```
applications/portal/languages/
├── default.py          # Default language (usually English)
├── en.py              # English translations
├── zh-tw.py           # Traditional Chinese
├── es.py              # Spanish  
├── vi.py              # Vietnamese
└── fr.py              # French (if added)
```

### URL Examples with Language Routing
```
# English (default)
https://portal.example.com/en/default/index
https://portal.example.com/en/api/user_profile

# Traditional Chinese
https://portal.example.com/zh-tw/default/index
https://portal.example.com/zh-tw/api/carpooling

# Spanish
https://portal.example.com/es/default/index
https://portal.example.com/es/api/wallet_balance

# Vietnamese
https://portal.example.com/vi/default/index
https://portal.example.com/vi/api/trip_history
```

### Adding New Language Support
```python
# 1. Create language file: applications/portal/languages/fr.py
{
'Welcome to Portal': 'Bienvenue sur Portal',
'Carpooling': 'Covoiturage',
'Wallet Balance': 'Solde du Portefeuille'
}

# 2. Router automatically detects new language
# 3. URLs become available: /fr/controller/function
```

### Language Detection in Controllers
```python
def index():
    """Controller with language awareness"""
    
    # Get current language from URL
    current_lang = request.uri_language or 'en'
    
    # Force language for translations
    if request.uri_language:
        T.force(request.uri_language)
    
    # Use localized messages
    welcome_msg = T('Welcome to Portal MaaS')
    
    return dict(
        language=current_lang,
        message=welcome_msg,
        available_languages=possible_languages
    )
```

## 📊 Output Examples

**Language Detection Result**:
```python
possible_languages = {
    'default': ['en'],
    'en': 'English',
    'zh-tw': 'Traditional Chinese', 
    'es': 'Español',
    'vi': 'Tiếng Việt'
}
```

**Router Configuration Output**:
```python
routers = {
    'portal': {
        'default_language': 'en',
        'languages': ['en', 'zh-tw', 'es', 'vi']
    }
}
```

**URL Routing Examples**:
```
Input URL: /portal/zh-tw/api/balance
Routed to: controller=api, function=balance, language=zh-tw

Input URL: /portal/es/carpooling/search  
Routed to: controller=carpooling, function=search, language=es
```

**Language Forced Translation**:
```python
# In controller with Chinese URL
T.force('zh-tw')
message = T('Wallet Balance')  # Returns: "錢包餘額"
```

## ⚠️ Important Notes

### Setup Requirements
- **Global Routing**: Requires web2py global routes.py configuration
- **File Naming**: Must rename routes.example.py to routes.py to activate
- **Server Restart**: Web2py server restart required after routing changes
- **Language Files**: Languages must exist in /languages/ directory

### Performance Considerations
- **URL Processing**: Language detection adds minimal overhead to request processing
- **Caching**: Web2py caches routing decisions for performance
- **SEO Impact**: Language-specific URLs improve SEO for international markets
- **CDN Compatibility**: Works with CDN configurations for global content delivery

### Common Issues
- **Missing Language Files**: URLs will return 404 if language file doesn't exist
- **Default Language**: Ensure default language is properly configured
- **URL Conflicts**: Avoid controller/function names that match language codes
- **Translation Loading**: Large translation files may impact startup time

### Internationalization Best Practices
- **Language Codes**: Use standard ISO language codes (en, zh-tw, es, vi)
- **Fallback Handling**: Implement graceful fallback to default language
- **Content Localization**: Ensure all user-facing content is translatable
- **Cultural Adaptation**: Consider cultural differences beyond language translation

## 🔗 Related File Links
- **Global Routes**: `/routes.py` (web2py root routing configuration)
- **Language Files**: `/applications/portal/languages/` (translation files)
- **Models**: `/applications/portal/models/db.py` (T.force() implementation)
- **Controllers**: `/applications/portal/controllers/` (language-aware logic)
- **Web2py Documentation**: Framework routing and internationalization guides
- **Example Reference**: `/examples/routes.parametric.example.py`

## 📈 Use Cases
- **Global MaaS Deployment**: Supporting multiple countries and languages
- **Localized Marketing**: Country-specific marketing campaigns with native URLs
- **SEO Optimization**: Language-specific URLs for better search engine ranking
- **User Experience**: Native language navigation for international users
- **A/B Testing**: Language-based feature testing and rollouts
- **Compliance**: Meeting local language requirements for transportation services
- **Customer Support**: Language-specific help and documentation URLs

## 🛠️ Improvement Suggestions
- **Automatic Language Detection**: Add browser language detection and redirect
- **Language Switching**: Implement language switching widget with URL updates
- **Subdomain Support**: Consider language-specific subdomains (en.portal.com)
- **Mobile Optimization**: Ensure routing works properly with mobile applications
- **Analytics Integration**: Track language usage and user preferences
- **Performance Monitoring**: Monitor routing performance across languages
- **Admin Interface**: Create admin interface for managing language configurations

## 🏷️ Document Tags
**Keywords**: web2py-routing, multi-language, internationalization, i18n, url-localization, language-detection, maas-routing, global-deployment

**Technical Tags**: `#web2py #routing #i18n #multi-language #internationalization #url-localization #maas`

**Target Roles**: Web developers (intermediate), DevOps engineers (intermediate), Product managers (beginner), International team leads (beginner)

**Difficulty**: ⭐⭐ (Moderate) - Understanding Web2py routing and internationalization

**Maintenance**: Low - Occasional updates for new languages

**Business Criticality**: Medium - Important for international market expansion

**Related Topics**: Web2py framework, Internationalization, URL routing, Multi-language support, Global deployment