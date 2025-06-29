# Job Documentation: aws-secrets-manager.js

## 📋 Job Overview
- **Purpose:** Manages AWS Secrets Manager operations (create, read, update, delete secrets)
- **Type:** Manual trigger with parameters
- **Schedule:** On-demand administrative tool
- **Impact:** AWS Secrets Manager configuration and application security credentials

## 🔧 Technical Details
- **Dependencies:** config, @maas/services AWS client
- **Database Operations:** None (AWS Secrets Manager only)
- **Key Operations:** CRUD operations on AWS secrets via SecretsManager client

## 📝 Code Summary
```javascript
const secretsManagerClient = new AWS.SecretsManager(options);

fn: async (action, key, secretValue) => {
  switch (action) {
    case 'create': res = await secretsManagerClient.createSecret(key, secretValue); break;
    case 'read': res = await secretsManagerClient.getSecretValue(key); break;
    case 'update': res = await secretsManagerClient.updateSecret(key, secretValue); break;
    case 'delete': res = await secretsManagerClient.deleteSecret(key); break;
  }
}
```

## ⚠️ Important Notes
- Requires proper AWS IAM permissions for SecretsManager operations
- Input validation ensures key is not empty and secretValue is provided for create/update
- Use extreme caution with delete operations - no rollback available
- LocalStack configuration available for development (commented out)
- Direct console output of sensitive data - use carefully in production

## 📊 Example Output
```bash
# Create secret
node app.js run aws-secrets-manager "create" "db-password" "mySecretPass123"

# Read secret
node app.js run aws-secrets-manager "read" "db-password" ""
# Output: { SecretString: "mySecretPass123", ... }

# Update secret
node app.js run aws-secrets-manager "update" "db-password" "newPassword456"

# Delete secret
node app.js run aws-secrets-manager "delete" "db-password" ""
```

## 🏷️ Tags
**Keywords:** aws, secrets-manager, credentials, security, configuration
**Category:** #job #manual-trigger #aws #secrets #security

---
Note: This tool manages sensitive security credentials - restrict access and audit usage carefully.