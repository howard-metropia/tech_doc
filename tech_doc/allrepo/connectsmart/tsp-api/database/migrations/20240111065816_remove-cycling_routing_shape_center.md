# Migration Documentation

## 📋 Migration Overview
- **Purpose:** Remove deprecated cycling routing shape center table
- **Date:** 2024-01-11 06:58:16
- **Ticket:** N/A
- **Risk Level:** Medium

## 🔧 Schema Changes
```sql
DROP TABLE cycling_routing_shape_center;
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| DROP | cycling_routing_shape_center | - | Removes cycling route shape center data |

## ⬆️ Up Migration
- Drops the cycling_routing_shape_center table
- Removes all cycling route shape center coordinate data

## ⬇️ Down Migration
- Recreates cycling_routing_shape_center table with original schema
- Restores table structure: id, link_id, longitude, latitude
- Uses InnoDB engine with utf8mb4_unicode_ci collation
- Does not restore data (data loss is permanent)

## ⚠️ Important Notes
- **Data Loss Warning:** This migration permanently removes cycling route data
- Table contained link IDs with longitude/latitude coordinates
- Rollback recreates structure but not data
- May impact cycling route functionality if still in use

## 🏷️ Tags
**Keywords:** cycling, routing, shape, center, cleanup, removal
**Category:** #migration #database #schema #cleanup #cycling #routing