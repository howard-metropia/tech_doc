# DuoReservationMatches Model Documentation

## 📋 Model Overview
- **Purpose:** Manages matching records for duo/carpool reservation pairings
- **Table/Collection:** reservation_match
- **Database Type:** MySQL (portal database)
- **Relationships:** Links reservations with their matched pairs for carpooling

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| reservation_id | INT | Yes | Foreign key to duo_reservation table |
| matched_reservation_id | INT | Yes | Foreign key to matched duo_reservation |
| match_score | DECIMAL | No | Algorithm-calculated match compatibility score |
| status | VARCHAR | No | Match status (pending, accepted, rejected, cancelled) |
| created_at | TIMESTAMP | Yes | Match creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** reservation_id, matched_reservation_id, status
- **Unique Constraints:** Unique combination of reservation_id and matched_reservation_id
- **Default Values:** status = 'pending', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Find matches for a reservation
const matches = await DuoReservationMatches.query()
  .where('reservation_id', reservationId)
  .where('status', 'accepted');

// Get all pending matches
const pendingMatches = await DuoReservationMatches.query()
  .where('status', 'pending')
  .orderBy('match_score', 'desc');

// Accept a match
await DuoReservationMatches.query()
  .where('id', matchId)
  .update({ status: 'accepted' });
```

## 🔗 Related Models
- `DuoReservations` - Many-to-one relationship via reservation_id and matched_reservation_id
- `AuthUsers` - Indirect relationship through reservations

## 📌 Important Notes
- Handles the pairing logic for carpooling/duo ride reservations
- Match score helps prioritize best compatibility matches
- Status field controls the matching workflow
- Supports bidirectional matching relationships

## 🏷️ Tags
**Keywords:** carpool, matching, reservations, duo, pairing
**Category:** #model #database #carpool #matching #mysql

---
Note: This model enables the carpooling matching system for duo reservations.