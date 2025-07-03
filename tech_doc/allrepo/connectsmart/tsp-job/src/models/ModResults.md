# ModResults Model

## Overview
Mode detection results model for the TSP Job system. Stores transportation mode classification results, detection accuracy metrics, and mode analysis data.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class ModResults extends Model {
  static get tableName() {
    return 'mod_results';
  }
}
module.exports = ModResults.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `mod_results`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Transportation mode detection
- Classification result storage
- Mode analysis accuracy tracking
- Machine learning model evaluation

## Detection Results
- **Primary Mode**: Main transportation method
- **Secondary Modes**: Multi-modal segments
- **Confidence Scores**: Detection accuracy levels
- **Classification Metadata**: Algorithm parameters

## Transportation Modes
- **Walking**: Pedestrian movement
- **Cycling**: Bicycle transportation
- **Driving**: Personal vehicle use
- **Public Transit**: Bus, train, metro
- **Ridehail**: Uber, Lyft services
- **Multi-Modal**: Combined transportation

## Key Features
- Automated mode detection
- Confidence scoring
- Multi-modal support
- Accuracy validation

## Detection Methods
- **GPS Pattern Analysis**: Movement pattern recognition
- **Speed-Based Classification**: Velocity analysis
- **Accelerometer Data**: Motion sensor integration
- **Location Context**: Venue-based inference

## Integration Points
- **Trips**: Trip mode classification
- **TripDetail**: Detailed mode analysis
- **ClusterTrips**: Pattern-based mode analysis
- **TripTrajectory**: Route-based mode detection

## Accuracy Metrics
- Detection confidence scores
- Validation against ground truth
- False positive/negative rates
- Algorithm performance tracking

## Machine Learning
- Model training data
- Feature extraction results
- Classification algorithms
- Continuous improvement

## Related Models
- Trips: Mode classification
- TripDetail: Detailed analysis
- ClusterTrips: Pattern analysis
- TripTrajectory: Route analysis

## Development Notes
- Machine learning integration
- Accuracy optimization critical
- Multi-modal detection support
- Continuous model improvement