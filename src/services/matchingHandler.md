# `matchingHandler.js`

## Overview

The `matchingHandler.js` service manages the business logic for carpool matching within enterprise and mega-carpool groups. It is responsible for creating and removing match invitations, calculating matching statistics, and identifying users within the same group hierarchy for potential carpool connections. The service directly interfaces with two separate databases, `portal` and `admin`, to handle reservations, group memberships, and organizational structures.

## Key Functions

### `updateMatchingStatistic(partnerIds)`

-   **Purpose:** This function is currently a placeholder and has no implementation. It was likely intended to update matching statistics for a given set of partners.
-   **Parameters:** `partnerIds` - An array of partner identifiers.
-   **Returns:** `undefined`.

### `updateMatchingStatistic2(reservationIds)`

-   **Purpose:** Calculates and updates matching statistics for a given list of reservations. It determines the number of invites sent, invites received, and total matches for each reservation and persists this data to the `reservation_match` table.
-   **Logic:**
    1.  For each `reservationId`, it fetches all sent and received invites from the `duo_reservation` table.
    2.  It queries the `match_statistic` table to count the total number of potential matches, excluding those already invited.
    3.  It then performs an "upsert" operation into the `reservation_match` table, either updating an existing record or inserting a new one with the calculated statistics (`invite_sent`, `invite_received`, `matches`).
-   **Parameters:** `reservationIds` (Array): A list of reservation IDs to process.
-   **Returns:** `void`.

### `getSameGroupUser(userId)`

-   **Purpose:** This is a critical function for identifying the network of potential carpool partners for a given user. It retrieves all other users who belong to the same groups, including those in associated "mega-carpool" organizations.
-   **Logic:**
    1.  Fetches all active groups the `userId` is a member of from the `group_member` table.
    2.  If any of these groups are linked to an enterprise (`enterprise_id`), it queries the `admin` database's `mega_carpool_organizations` table to find all other enterprises belonging to the same mega-organization.
    3.  It then gathers all group IDs from these associated enterprises.
    4.  Finally, it queries the `group_member` table again with the complete list of group IDs to return a unique list of all user IDs within that entire network (excluding the original `userId`).
-   **Parameters:** `userId` (Integer): The ID of the user.
-   **Returns:** (Promise<Array<Integer>>): A promise that resolves to an array of user IDs belonging to the same group network.

### `removeInvitesForGroup(reservationIds)`

-   **Purpose:** Prunes invalid carpool invitations. This function is called when a user's group affiliations change, ensuring that outstanding invitations are only maintained between users who are still in the same group network.
-   **Logic:**
    1.  Retrieves all pending invitations associated with the given `reservationIds`.
    2.  For each invitation, it uses `getSameGroupUser` to check if the inviting user and the invited user are still part of the same group structure.
    3.  If they are no longer in the same group, the invitation is deleted from the `duo_reservation` table.
-   **Parameters:** `reservationIds` (Array): A list of reservation IDs to check.
-   **Returns:** (Promise<Array<Integer>>): A promise that resolves to an array of reservation IDs that were affected.

### `removeMatch(reservationIds)`

-   **Purpose:** Similar to `removeInvitesForGroup`, this function cleans up records in the `match_statistic` table when users are no longer in the same group.
-   **Logic:**
    1.  Fetches all match statistic records associated with the given `reservationIds`.
    2.  For each record, it uses `getSameGroupUser` to verify if the two users are still in the same group.
    3.  If not, the record is deleted from the `match_statistic` table.
-   **Parameters:** `reservationIds` (Array): A list of reservation IDs to check.
-   **Returns:** (Promise<Array<Integer>>): A promise that resolves to an array of matched reservation IDs that were affected.

## Database Connections

-   **`portal` (knex):** The primary database connection used for most operations related to reservations, invites, and group memberships (`duo_reservation`, `reservation_match`, `group_member`, `duo_group`).
-   **`admin` (knex1):** A secondary database connection used specifically to query the `mega_carpool_organizations` table to resolve enterprise-level group hierarchies. 