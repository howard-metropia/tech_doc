# Job Documentation: sample.js

## 📋 Job Overview
- **Purpose:** Example/template job demonstrating basic job structure and parameter handling
- **Type:** Manual trigger / Development template
- **Schedule:** On-demand for testing or as development reference
- **Impact:** No system impact - outputs provided name parameter to console

## 🔧 Technical Details
- **Dependencies:** None
- **Database Operations:** None
- **Key Operations:** Simple console output of input parameter

## 📝 Code Summary
```javascript
module.exports = {
  inputs: {
    name: String,
  },
  fn: async function (name) {
    console.log(name);
  },
};
```

## ⚠️ Important Notes
- This is a template/example job for development reference
- Safe to run in any environment - no side effects
- Demonstrates basic job structure with input parameters
- Can be used as starting point for new job development
- No error handling or logging - purely educational

## 📊 Example Output
```bash
# Usage: node app.js run sample "Hello World"
Hello World

# Usage: node app.js run sample "Test Parameter"
Test Parameter
```

## 🏷️ Tags
**Keywords:** sample, template, example, development, testing
**Category:** #job #template #development #example

---
Note: This is a development template job - use as reference for creating new jobs with parameter inputs.