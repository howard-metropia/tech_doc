# TSP Job Service: matchingHandler.js

## Quick Summary

The `matchingHandler.js` service manages carpool matching statistics, invitation tracking, and group-based filtering within the ConnectSmart platform. It maintains comprehensive records of sent/received invitations, calculates matching metrics, and handles enterprise carpool organization relationships. The service ensures accurate matching data for analytics and implements group-based restrictions for carpool partnerships.

## Technical Analysis

### Core Architecture

The service implements a sophisticated matching management system with the following components:

- **Invitation Tracking**: Monitors sent and received carpool invitations
- **Statistics Management**: Maintains matching metrics for reservations
- **Group Relationships**: Handles enterprise carpool organization hierarchies
- **Data Cleanup**: Manages invitation and match record removal
- **Multi-Database Integration**: Coordinates between portal and admin databases

### Key Functions

#### getSentInvites(reservationId)
Retrieves invitations sent by a specific reservation:
```javascript
async function getSentInvites(reservationId) {
  const sql = `select reservation.id, reservation.user_id, reservation.role, reservation.price 
  from duo_reservation
  join reservation on reservation.id = duo_reservation.offer_id
  where duo_reservation.reservation_id = ?
  and duo_reservation.offer_id <> duo_reservation.reservation_id;`;
  
  const [rows] = await knex.raw(sql, [reservationId]);
  return rows.map(row => ({
    reservation_id: row.id,
    role: row.role,
    price: row.price,
    user_id: row.user_id,
  }));
}
```

#### getReceivedInvites(reservationId)
Retrieves invitations received by a specific reservation:
```javascript
async function getReceivedInvites(reservationId) {
  const sql = `select reservation.id, reservation.user_id, reservation.role, reservation.price 
  from duo_reservation
  join reservation on reservation.id = duo_reservation.offer_id
  where duo_reservation.offer_id = ?
  and duo_reservation.offer_id <> duo_reservation.reservation_id;`;
  
  const [rows] = await knex.raw(sql, [reservationId]);
  return rows.map(row => ({
    reservation_id: row.id,
    role: row.role,
    price: row.price,
    user_id: row.user_id,
  }));
}
```

#### updateMatchingStatistic2(reservationIds)
Comprehensive matching statistics update:
```javascript
async function updateMatchingStatistic2(reservationIds) {
  const utcNow = new Date().toISOString().replace('T', ' ').split('.')[0];
  
  for (const reservationId of reservationIds) {
    const inviteSent = await getSentInvites(reservationId);
    const inviteReceived = await getReceivedInvites(reservationId);
    
    // Combine all invitation reservation IDs
    let inviteReservationIds = [];
    inviteReservationIds = inviteReservationIds.concat(
      inviteSent.map((x) => x.reservation_id),
    );
    inviteReservationIds = inviteReservationIds.concat(
      inviteReceived.map((x) => x.reservation_id),
    );
    
    // Get matches excluding invitations
    const sql = `select match_reservation_id from match_statistic 
    where reservation_id = ${reservationId}${
      Array.isArray(inviteReservationIds) && inviteReservationIds.length > 0
        ? ` and match_reservation_id not in (${inviteReservationIds})`
        : ''
    };`;
    
    const [matches] = await knex.raw(sql);
    
    // Update or insert reservation_match record
    const row = await knex('reservation')
      .leftJoin('reservation_match', 'reservation_match.reservation_id', '=', 'reservation.id')
      .where('reservation.id', '=', reservationId)
      .select('reservation_match.id', 'reservation.id as reservation_id', 'reservation.user_id')
      .first();
      
    if (row.id) {
      await knex('reservation_match').where({ id: row.id }).update({
        invite_sent: inviteSent.length,
        invite_received: inviteReceived.length,
        matches: matches.length,
        modified_on: utcNow,
      });
    } else {
      await knex('reservation_match').insert({
        user_id: row.user_id,
        reservation_id: row.reservation_id,
        invite_sent: inviteSent.length,
        invite_received: inviteReceived.length,
        matches: matches.length,
        created_on: utcNow,
        modified_on: utcNow,
      });
    }
  }
}
```

### Enterprise Group Management

#### getSameGroupUser(userId)
Retrieves users within the same carpool organization network:
```javascript
async function getSameGroupUser(userId) {
  // Get user's direct groups
  const group1 = await knex('group_member')
    .join('duo_group', 'duo_group.id', '=', 'group_member.group_id')
    .where('group_member.user_id', userId)
    .where('group_member.member_status', '>', 1)
    .where('duo_group.disabled', 'F')
    .groupBy('duo_group.id')
    .select('duo_group.*');
    
  let groupIds = group1.map((x) => x.id);
  const enterpriseIds = group1.reduce((p, c) => {
    if (c.enterprise_id) p.push(c.enterprise_id);
    return p;
  }, []);
  
  // Handle mega carpool organizations
  if (enterpriseIds.length > 0) {
    const targets = await knex1('mega_carpool_organizations')
      .join('mega_carpool_organizations as target', 'target.mega_id', '=', 'mega_carpool_organizations.mega_id')
      .whereIn('mega_carpool_organizations.org_id', enterpriseIds)
      .where('target.mega_id', '=', 'mega_carpool_organizations.mega_id')
      .whereNotIn('target.org_id', enterpriseIds)
      .groupBy('target.org_id')
      .select('target.org_id');
      
    const enterprises = targets.map((x) => x.org_id);
    const groups = await knex('duo_group')
      .whereIn('enterprise_id', enterprises)
      .where('disabled', 'F')
      .select('id');
      
    groupIds = groupIds.concat(groups.map((x) => x.id));
  }
  
  // Get all users in these groups
  let result = [];
  if (groupIds.length > 0) {
    result = await knex('group_member')
      .whereIn('group_id', groupIds)
      .where('user_id', '!=', userId)
      .where('member_status', '>', 1)
      .groupBy('user_id')
      .select('user_id');
  }
  
  return result.map((x) => x.user_id);
}
```

### Data Cleanup Operations

#### removeInvitesForGroup(reservationIds)
Removes invitations between users not in the same group:
```javascript
async function removeInvitesForGroup(reservationIds) {
  const rows = await knex('duo_reservation')
    .join('reservation', 'duo_reservation.reservation_id', 'reservation.id')
    .join('reservation as invited', 'duo_reservation.offer_id', 'invited.id')
    .where((builder) => {
      builder
        .whereIn('duo_reservation.reservation_id', reservationIds)
        .orWhereIn('duo_reservation.offer_id', reservationIds);
    })
    .where('duo_reservation.reservation_id', '!=', 'offer_id')
    .where('reservation.status', '=', 1)
    .select(
      'duo_reservation.id',
      'duo_reservation.reservation_id',
      'duo_reservation.offer_id',
      'reservation.user_id',
      'invited.user_id as invited_user_id',
    );

  const affectedReservationIds = [];
  for (const row of rows) {
    const memberIds = await getSameGroupUser(row.user_id);
    if (memberIds.indexOf(row.invited_user_id) < 0) {
      await knex('duo_reservation').where({ id: row.id }).delete();
      logger.debug(`[Duo] Remove reservation(${row.reservation_id}) invite reservation(${row.offer_id})`);
      
      // Clean up orphaned invitation records
      const otherInvite = await knex('duo_reservation')
        .where('offer_id', '=', 'offer_id')
        .where('offer_id', '!=', 'reservation_id');
        
      if (otherInvite.length === 0) {
        await knex('duo_reservation').where({ offer_id: row.offer_id }).delete();
      }
    }
  }
  
  return affectedReservationIds;
}
```

## Usage/Integration

### Periodic Statistics Updates

The service is typically called after matching operations to maintain accurate statistics:

```javascript
const { updateMatchingStatistic2 } = require('./matchingHandler');

// Update statistics for processed reservations
const reservationIds = [12345, 67890, 54321];
await updateMatchingStatistic2(reservationIds);

console.log(`Updated matching statistics for ${reservationIds.length} reservations`);
```

### Group-Based Filtering

Used during matching processes to enforce group restrictions:

```javascript
const { getSameGroupUser, removeInvitesForGroup } = require('./matchingHandler');

// Get users in the same carpool organization
const userId = 12345;
const groupMembers = await getSameGroupUser(userId);
console.log(`User ${userId} can carpool with ${groupMembers.length} group members`);

// Clean up invalid invitations
const affectedReservations = await removeInvitesForGroup([67890, 54321]);
console.log(`Cleaned invitations for ${affectedReservations.length} reservations`);
```

### Statistics Retrieval

Monitor invitation patterns for individual reservations:

```javascript
const { getSentInvites, getReceivedInvites } = require('./matchingHandler');

const reservationId = 12345;
const sentInvites = await getSentInvites(reservationId);
const receivedInvites = await getReceivedInvites(reservationId);

console.log(`Reservation ${reservationId}:`);
console.log(`  Sent: ${sentInvites.length} invitations`);
console.log(`  Received: ${receivedInvites.length} invitations`);
```

## Dependencies

### External Packages
- `@maas/core/mysql`: Database connectivity for both portal and admin databases
- `@maas/core/log`: Centralized logging system

### Database Schema Dependencies

**Portal Database (knex):**
- **reservation**: Core reservation records
- **duo_reservation**: Invitation relationships
- **match_statistic**: Matching algorithm results
- **reservation_match**: Aggregated matching statistics
- **group_member**: Group membership records
- **duo_group**: Carpool group definitions

**Admin Database (knex1):**
- **mega_carpool_organizations**: Enterprise organization hierarchies

## Code Examples

### Basic Statistics Update
```javascript
const matchingHandler = require('./matchingHandler');

// Update statistics for a single reservation
await matchingHandler.updateMatchingStatistic2([12345]);

// Bulk update for multiple reservations
const reservationIds = [12345, 67890, 54321, 98765];
await matchingHandler.updateMatchingStatistic2(reservationIds);
```

### Group Membership Analysis
```javascript
// Check group relationships
const userId = 12345;
const groupMembers = await matchingHandler.getSameGroupUser(userId);

console.log(`User ${userId} group members:`, groupMembers);

// Verify group access for invitation
const targetUserId = 67890;
const canInvite = groupMembers.includes(targetUserId);
console.log(`Can invite user ${targetUserId}: ${canInvite}`);
```

### Invitation Tracking
```javascript
// Get complete invitation picture for a reservation
const reservationId = 12345;

const [sentInvites, receivedInvites] = await Promise.all([
  matchingHandler.getSentInvites(reservationId),
  matchingHandler.getReceivedInvites(reservationId)
]);

console.log('Sent invitations:');
sentInvites.forEach(invite => {
  console.log(`  To user ${invite.user_id}, role ${invite.role}, price $${invite.price}`);
});

console.log('Received invitations:');
receivedInvites.forEach(invite => {
  console.log(`  From user ${invite.user_id}, role ${invite.role}, price $${invite.price}`);
});
```

### Data Cleanup Operations
```javascript
// Remove invalid group invitations
const reservationIds = [12345, 67890];
const affectedIds = await matchingHandler.removeInvitesForGroup(reservationIds);

console.log(`Removed invalid invitations affecting ${affectedIds.length} reservations`);

// Remove invalid matches
const matchAffectedIds = await matchingHandler.removeMatch(reservationIds);
console.log(`Cleaned matches affecting ${matchAffectedIds.length} reservations`);
```

### Enterprise Organization Queries
```javascript
// Trace enterprise relationships
const userId = 12345;

// Get user's direct groups
const directGroups = await knex('group_member')
  .join('duo_group', 'duo_group.id', '=', 'group_member.group_id')
  .where('group_member.user_id', userId)
  .select('duo_group.*');

console.log(`User belongs to ${directGroups.length} direct groups`);

// Get extended network through mega organizations
const sameGroupUsers = await matchingHandler.getSameGroupUser(userId);
console.log(`Total network: ${sameGroupUsers.length} users`);
```

The matchingHandler service provides comprehensive matching management capabilities, ensuring accurate statistics, proper group-based filtering, and clean data maintenance for the ConnectSmart carpool system.