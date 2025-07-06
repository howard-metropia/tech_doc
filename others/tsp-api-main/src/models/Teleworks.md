# Teleworks Model Documentation

## 📋 Model Overview
- **Purpose:** Manages telework and remote work arrangements for users
- **Table/Collection:** telework
- **Database Type:** MySQL
- **Relationships:** References users and work schedules

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| user_id | Integer | - | User who has telework arrangement |
| work_date | Date | - | Date of telework |
| work_type | String | - | Full remote, hybrid, in-office |
| location | String | - | Work location (home, office, other) |
| status | String | - | Scheduled, active, completed |
| start_time | Time | - | Work start time |
| end_time | Time | - | Work end time |
| notes | Text | - | Additional notes or comments |
| approved_by | Integer | - | Manager who approved |
| approval_date | DateTime | - | When arrangement was approved |
| is_recurring | Boolean | - | Whether this is recurring |
| recurring_pattern | String | - | Weekly, monthly pattern |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on user_id, work_date, status
- **Unique Constraints:** Possibly user_id+work_date
- **Default Values:** Auto-generated timestamps

## 📝 Usage Examples
```javascript
// Schedule telework day
const telework = await Teleworks.query().insert({
  user_id: userId,
  work_date: '2024-06-25',
  work_type: 'full_remote',
  location: 'home',
  status: 'scheduled',
  start_time: '09:00:00',
  end_time: '17:00:00'
});

// Get user's telework schedule
const schedule = await Teleworks.query()
  .where('user_id', userId)
  .where('work_date', '>=', new Date())
  .orderBy('work_date');

// Approve telework request
await Teleworks.query()
  .where('id', teleworkId)
  .patch({
    status: 'approved',
    approved_by: managerId,
    approval_date: new Date()
  });
```

## 🔗 Related Models
- **AuthUsers**: Telework arrangements belong to users
- **WorkSchedules**: May integrate with regular work schedules
- **Managers**: Approval workflow references managers

## 📌 Important Notes
- Supports flexible work arrangements and remote work policies
- Approval workflow for management oversight
- Recurring pattern support for regular arrangements
- Time tracking integration for work hours
- Location tracking for compliance and reporting

## 🏷️ Tags
**Keywords:** telework, remote-work, flexible-work, scheduling
**Category:** #model #database #work #scheduling