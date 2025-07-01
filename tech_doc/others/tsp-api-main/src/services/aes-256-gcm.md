# AES-256-GCM Encryption Service Documentation

## 🔍 Quick Summary (TL;DR)
This service provides a straightforward and secure way to perform symmetric encryption and decryption using the **AES-256-GCM** algorithm. It encapsulates Node.js's native `crypto` library to offer two simple functions: `encrypt` and `decrypt`. This service is crucial for protecting sensitive data, such as user information from microsurveys, by ensuring both its **confidentiality** (it can't be read) and its **integrity** (it can't be secretly changed).

**Keywords:** crypto | encryption | decryption | security | aes-256-gcm | symmetric-key | nodejs-crypto | aead | data-protection

**Primary use cases:** 
- Encrypting sensitive data before storing it in the database.
- Decrypting data after retrieving it from the database to be used by the application.
- Ensuring the privacy and integrity of user-submitted information.

**Compatibility:** Node.js >= 16.0.0.

## ❓ Common Questions Quick Index
- **Q: What is AES-256-GCM?** → It's a modern, highly secure, and efficient symmetric encryption standard that provides both encryption and an authenticity check in one.
- **Q: What is the `KEY` and where does it come from?** → It's the secret password used for both encryption and decryption. It's loaded securely from the application's configuration files and is critical to keep secret.
- **Q: What is an "IV" (Initialization Vector)?** → It's a random, one-time-use number that ensures that encrypting the same plaintext multiple times results in different ciphertexts. This is critical for security.
- **Q: What is the "Authentication Tag"?** → It's a cryptographic signature that GCM mode produces. It's used during decryption to verify that the encrypted data has not been tampered with or corrupted.
- **Q: Is this service secure?** → Yes, the implementation follows modern cryptographic best practices: it uses a strong, standardized algorithm (AES-256-GCM), a full-strength key, and a unique, random IV for every encryption operation. Its security ultimately depends on the secrecy of the encryption key in the configuration.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as providing a **magical, ultra-secure lockbox**.
- **`encrypt` (Putting something in the box):** You give the service a secret message (plaintext). The service puts it in the box, generates a brand new, unique key for the lock (`IV`), and locks it using a master secret password (`KEY`). It then attaches a special, tamper-proof wax seal (the `Authentication Tag`) to the outside of the box. It gives you back the locked box, with the unique key (`IV`) and the wax seal (`Tag`) attached to the outside.
- **`decrypt` (Opening the box):** You give the service a locked box. The service first inspects the wax seal (`Tag`). If the seal is broken or looks forged, it immediately destroys the box and tells you something is wrong. If the seal is intact, it uses the unique key (`IV`) on the outside of the box and the master secret password (`KEY`) to unlock it and give you back your original secret message.

**Technical explanation:** 
This module implements AES-256-GCM, which is an **Authenticated Encryption with Associated Data (AEAD)** cipher.
- **`encrypt`**: This function takes a UTF-8 string, generates a cryptographically random 12-byte Initialization Vector (IV), and uses it with the pre-configured 32-byte key to encrypt the data. After encryption, it retrieves a 16-byte authentication tag. It then concatenates the `IV`, `tag`, and `ciphertext` into a single buffer and returns it as a Base64 encoded string. This format is self-contained and ideal for storage or transmission.
- **`decrypt`**: This function takes a Base64 encoded string, decodes it back into a buffer, and carefully unpacks it into its three constituent parts: the IV, the authentication tag, and the ciphertext. It initializes the AES-256-GCM decipher with the same secret key and the extracted IV. Crucially, it sets the expected authentication tag. The final decryption step will fail and throw an error if the computed tag does not match the provided tag, thus preventing the application from processing tampered or corrupted data.

**Business value explanation:**
Data privacy and security are paramount for user trust and regulatory compliance (e.g., GDPR, CCPA). This service provides the fundamental building block for securing sensitive user data within the application. By encrypting data like microsurvey responses, the company protects its users' privacy and protects itself from the consequences of data breaches. The use of an authenticated cipher (GCM) is particularly valuable as it prevents a wide range of attacks where an attacker might try to manipulate stored ciphertext, ensuring the integrity of the data an application operates on.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/aes-256-gcm.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Native Node.js `crypto` module
- **Type:** Cryptography Utility Service
- **File Size:** < 1 KB
- **Complexity Score:** ⭐⭐ (Low - The code is simple, but understanding the underlying cryptographic concepts is essential.)

**Dependencies (Criticality Level):**
- `crypto`: The native Node.js module for all cryptographic operations (**Critical**).
- `config`: Used to securely load the encryption key. The application is insecure without this (**Critical**).

## 📝 Detailed Code Analysis

### Constants
- `ALGORITHM`: Specifies `'aes-256-gcm'`, a modern, fast, and secure industry standard.
- `KEY`: A 32-byte (256-bit) buffer derived from a hexadecimal string in the configuration file. The security of all data encrypted by this service rests on the secrecy of this key.
- `IV_LENGTH`: Set to 12 bytes (96 bits). This is the NIST-recommended length for the IV in GCM mode for optimal performance and security.
- `AUTH_TAG_LENGTH`: Set to 16 bytes (128 bits). This is the full, standard-length authentication tag for GCM, providing the maximum level of integrity protection.

### `encrypt(plainText)` Function
1.  `const iv = crypto.randomBytes(IV_LENGTH);`: Generates a new, cryptographically secure random Initialization Vector. **This is the most critical step for the security of GCM mode.** A unique IV must be used for every single encryption operation performed with the same key.
2.  `const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);`: Creates and configures the cipher instance with the chosen algorithm, the secret key, and the newly generated unique IV.
3.  `const encrypted = Buffer.concat([...]);`: Performs the actual encryption. `cipher.update` handles the bulk of the data, and `cipher.final` handles any remaining padding.
4.  `const tag = cipher.getAuthTag();`: Retrieves the 16-byte authentication tag. This tag is a function of the key, IV, and the plaintext, acting as a protected checksum.
5.  `return Buffer.concat([iv, tag, encrypted]).toString('base64');`: This is the packing step. It creates a single data blob with the structure `[IV][Auth Tag][Ciphertext]` and encodes it in Base64. Base64 is used to convert the binary data into a text-safe format that can be easily stored in a database or transmitted in a JSON payload.

### `decrypt(cipherText)` Function
1.  `const data = Buffer.from(cipherText, 'base64');`: The reverse of the final encryption step, decoding the Base64 string back into a raw binary buffer.
2.  `const iv = data.slice(...)`, `const tag = data.slice(...)`, `const text = data.slice(...)`: This is the unpacking step. Using the known, fixed lengths of the IV and the tag, it slices the buffer into its three original components.
3.  `const decipher = crypto.createDecipheriv(ALGORITHM, KEY, iv);`: Creates the decipher instance, providing the same secret key and the IV that was extracted from the payload.
4.  `decipher.setAuthTag(tag);`: This is the crucial integrity-check step. The decipher is told what the authentication tag *should* be.
5.  `const decrypted = Buffer.concat([...]);`: The decryption is performed. Internally, the decipher calculates its own authentication tag based on the key, IV, and ciphertext. If this computed tag does not exactly match the tag provided via `setAuthTag`, this line will throw an `Unsupported state or unable to authenticate` error, and the function will fail.
6.  `return decrypted.toString('utf8');`: If and only if the authentication succeeds, the decrypted buffer is converted back to a human-readable string.

## 🚀 Usage Methods

```javascript
const { encrypt, decrypt } = require('@app/src/services/aes-256-gcm');

// The sensitive data to be protected
const originalText = 'This is a secret message for a microsurvey.';
console.log('Original Text:', originalText);

// Encrypt the data
const encryptedText = encrypt(originalText);
console.log('Encrypted (Base64):', encryptedText);
// -> Outputs a long Base64 string like: 'e6A7p5c5A1g9m7p5...=='

// ... some time later, after retrieving from the database ...

try {
  // Decrypt the data
  const decryptedText = decrypt(encryptedText);
  console.log('Decrypted Text:', decryptedText);
  // -> Outputs: 'This is a secret message for a microsurvey.'

  // Test tampered data
  const tamperedText = encryptedText.slice(0, -5) + 'abcde';
  decrypt(tamperedText); // This line will throw an error
} catch (error) {
  console.error('Decryption Failed:', error.message);
  // -> Outputs: 'Decryption Failed: Unsupported state or unable to authenticate'
}
```

## 🔐 Security Best Practices & Considerations
- **Key Management**: The most critical security aspect is the management of the `microSurveyEncryption` key stored in the config. In a production environment, this key should not be in a plain text config file checked into version control. It should be managed by a dedicated secrets management service like AWS Secrets Manager, HashiCorp Vault, or Google Secret Manager, and injected into the application as an environment variable at runtime.
- **Key Rotation**: For long-lived applications, the encryption key should be rotated periodically. This service as written does not support key rotation (e.g., key versioning), and adding it would require storing a key identifier alongside the ciphertext.
- **Error Handling**: Any code calling the `decrypt` function **must** be wrapped in a `try...catch` block. A thrown error during decryption is a security feature, indicating that the data is not authentic, and it must be handled as a security event, not just a regular error.

## 🔗 Related File Links
- **Node.js Documentation:** [crypto `Cipher` objects](https://nodejs.org/api/crypto.html#class-cipher)
- **Configuration:** The application's `config` files where `vendor.incentive.microSurveyEncryption` is defined.

---
*This documentation was generated to provide a comprehensive, in-depth explanation of this critical cryptographic service, its implementation, and its security implications.* 