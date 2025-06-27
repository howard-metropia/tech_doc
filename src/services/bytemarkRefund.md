# Bytemark CSV Refund Service Documentation

## 🔍 Quick Summary (TL;DR)
This service is an administrative tool designed to process bulk user refunds from a static CSV file. It reads a file named `bytemark-refund-data.csv`, parses the user IDs and refund amounts, and then uses the `walletService` to credit points back to each user's wallet. This is not a real-time API service but a script intended for manual execution by an administrator to handle specific refund scenarios, such as a service outage or a promotional event. It also contains a small, hardcoded test function.

**Keywords:** refund | bulk-processing | csv | wallet | points | administrative-script | batch-job

**Primary use cases:** 
- Processing a batch of refunds for multiple users at once from a predefined CSV file.
- Acting as a manually-triggered script for crediting user wallets for special circumstances related to Bytemark.

**Compatibility:** Node.js >= 16.0.0.

## ❓ Common Questions Quick Index
- **Q: What is this service for?** → It gives users refunds by reading a list from a CSV file.
- **Q: Is this an API that gets called by the app?** → No. This is a script that a developer or administrator would run manually to process a batch of refunds.
- **Q: Where does the refund data come from?** → A hardcoded file named `bytemark-refund-data.csv` located in the `src/static/` directory.
- **Q: How does it actually give the refund?** → It calls another service, `walletService`, which is responsible for managing user points and transactions.
- **Q: What is `sbTest`?** → A simple test function to give a fixed refund to two hardcoded user IDs. It's for development and debugging, not for production.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as an **accountant running a special refund program**.
1.  **Pick up the Refund List:** The accountant picks up a specific spreadsheet from their desk named `bytemark-refund-data.csv`. This list contains the names (user IDs) of customers to be refunded and how much each should get. The last line of the spreadsheet has the grand total.
2.  **Check the Math:** Before starting, the accountant quickly adds up all the individual refund amounts on the list to make sure they match the grand total written at the bottom. If they don't, they stop immediately, knowing the list is faulty.
3.  **Issue the Credits:** For each person on the list, the accountant goes to the main customer ledger (`walletService`) and adds the specified credit amount to their account, making a note that it was for a "Bytemark refund."

**Technical explanation:** 
The service exports two async functions. The main function, `refund`, reads and parses a CSV file located at `src/static/bytemark-refund-data.csv` using Node's `fs` module. The CSV parsing is done manually by splitting the file content by newlines and commas. It assumes the first line is a header, the last line is a summary containing a total, and all intermediate lines are data rows. It performs a validation step by summing the 'Value' column of the data and comparing it to the total in the summary row. If the validation passes, it iterates through each parsed row and calls `walletService.pointsTransaction`, passing the `User_id` and `Value` to credit points to the user's wallet with the static reason "Bytemark refund". The secondary `sbTest` function is a small utility that gives a hardcoded amount of points to a hardcoded list of user IDs, intended for testing.

**Business value explanation:**
This script provides a simple, effective, and controlled way for administrators to handle bulk refunds or credits to users. While not automated, its manual nature is a form of safety, ensuring that large-scale point adjustments are only made deliberately. It provides a necessary tool for customer service and operational teams to respond to issues that affect multiple users, such as ticketing system failures, by allowing them to issue compensation in the form of wallet points.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/bytemarkRefund.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `fs`, `path`, `moment-timezone`, `@app/src/services/wallet`
- **Type:** Administrative Script / Batch Job
- **File Size:** ~2 KB
- **Complexity Score:** ⭐⭐ (Low-Medium. The logic is simple, but its dependency on a static file and manual execution make it a unique type of service.)

## 📝 Detailed Code Analysis

### Static File Dependency
The entire functionality of the `refund` function is tightly coupled to the existence and specific format of `bytemark-refund-data.csv`. Any change to the CSV's location or structure (e.g., column order, summary line position) would break the script. This makes the script fragile but also very specific to its purpose.

### Manual CSV Parsing
The script does not use a dedicated CSV parsing library (like `csv-parse` or `papaparse`). Instead, it relies on `String.prototype.split()`. This is sufficient for a simple, well-formatted CSV but could fail unexpectedly with more complex data (e.g., if a field contained a comma).

### Validation Logic
The inclusion of a check `if (checkTotal !== Number(data.summary))` is a simple but important data integrity check. It prevents the script from running with an incomplete or corrupt data file, which could lead to only a subset of users being refunded correctly.

### Idempotency
The script is **not idempotent**. If it is run twice with the same CSV file, users will be refunded twice. This is a critical operational consideration. An administrator running this script must ensure it is run only once per file and that the file is updated or removed after a successful run to prevent accidental duplicate payments.

## 🚀 Usage Methods

```bash
# This service is intended to be run from a Node.js script or shell.
# 1. An administrator would first place the correct `bytemark-refund-data.csv`
#    file into the `allrepo/connectsmart/tsp-api/src/static/` directory.

# 2. Then, they would execute it via a runner script. For example:

# file: ./scripts/run-refund.js
const bytemarkRefundService = require('../src/services/bytemarkRefund');

async function main() {
  try {
    console.log('Starting Bytemark refund process...');
    await bytemarkRefundService.refund();
    console.log('Refund process completed successfully.');
  } catch (error) {
    console.error('An error occurred during the refund process:', error);
    process.exit(1);
  }
}

main();

# 3. Execute the script from the terminal
# > node ./scripts/run-refund.js
```

## ⚠️ Important Notes
- **NOT IDEMPOTENT:** Running the script multiple times with the same input file will result in multiple refunds being issued to users. Extreme care must be taken during execution.
- **Static File:** The script is completely dependent on the `bytemark-refund-data.csv` file. The process for updating this file must be clearly defined.
- **Manual Execution:** This is not an automated service and requires manual intervention to run.

## 🔗 Related File Links
- **Core Dependency:** `@app/src/services/wallet.js`
- **Data Source:** `allrepo/connectsmart/tsp-api/src/static/bytemark-refund-data.csv` (not checked into source control, but expected to be present at runtime)

---
*This documentation was generated to explain the administrative, script-like nature of this service for processing bulk refunds from a CSV file.* 