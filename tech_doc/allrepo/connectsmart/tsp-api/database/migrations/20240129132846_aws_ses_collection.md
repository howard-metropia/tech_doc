# Migration Documentation

## 📋 Migration Overview
- **Purpose:** Create AWS SES email tracking system for delivery, bounce, and complaint monitoring
- **Date:** 2024-01-29 13:28:46
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
CREATE TABLE aws_reports (id, report_type, user_id, user_email, message_id, source_email, subject, bounce_at, complaint_at, delivery_at, send_at, reject_at, open_at, click_at, rendering_failure_at, delivery_delay_at, subscription_at, created_at, updated_at);
CREATE TABLE aws_report_detail (id, notification_message_id, report_id, event_type, message_id, timestamp, from, to, subject, other_info);
CREATE TABLE aws_report_type (id, report_name);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| CREATE | aws_reports | - | Main email tracking table with event timestamps |
| CREATE | aws_report_detail | - | Detailed event information for each email report |
| CREATE | aws_report_type | - | Email report type definitions |
| ADD | aws_reports | bounce_at, complaint_at, delivery_at | Email delivery status tracking |
| ADD | aws_reports | open_at, click_at | Email engagement tracking |

## ⬆️ Up Migration
- Creates comprehensive AWS SES email tracking infrastructure
- Supports tracking email delivery events (bounce, complaint, delivery, send, reject)
- Supports engagement tracking (open, click events)
- Links email events to user accounts via user_id and user_email

## ⬇️ Down Migration
- Drops all three AWS email tracking tables
- Removes all email event tracking capabilities

## ⚠️ Important Notes
- Email addresses stored up to 100 characters
- Message IDs limited to 64 characters
- Subject lines support up to 200 characters
- Includes comprehensive timestamp tracking for all email events

## 🏷️ Tags
**Keywords:** aws, ses, email, tracking, bounce, complaint, delivery
**Category:** #migration #database #schema #email #aws #ses