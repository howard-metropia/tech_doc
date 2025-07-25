# ConnectSmart Platform Technical Documentation

## =� Overview

This repository contains comprehensive technical documentation for the ConnectSmart MaaS (Mobility as a Service) platform, including detailed documentation for all microservices, APIs, and system components.

## <� Platform Architecture

The ConnectSmart platform consists of:

- **Hybrid (Web2py)**: Portal application with web2py framework (327 files)
- **TSP API (Node.js)**: Transportation Service Provider API (589 files)  
- **Admin Platform API**: Administrative interface for campaign management
- **GoMyWay Workspace**: Modern npm workspace monorepo

## =� Repository Structure

```
tech_doc/
   allrepo/connectsmart/
      hybrid/           # Web2py Portal application documentation
         applications/ # Portal app modules, controllers, models
         gluon/        # Web2py framework components
         handlers/     # WSGI and server handlers
      tsp-api/          # TSP API documentation
          src/          # Controllers, models, services, schemas
          config/       # Database and application configuration
          database/     # Migrations and seeds
          test/         # Test files and fixtures
   maas-api/             # MaaS API service documentation
   config/               # Configuration files
   database/             # Database schemas and migrations
   src/                  # Source code documentation
   test/                 # Test documentation
```

## =' Technology Stack

### Hybrid (Web2py Framework)
- **Python**: Web2py application framework
- **PyDAL**: Database Abstraction Layer
- **YATL**: Yet Another Template Language
- **Gluon**: Web2py core components

### TSP API (Node.js)
- **Framework**: Koa.js with Objection.js ORM
- **Database**: MySQL with Knex.js migrations
- **Cache**: MongoDB, Redis
- **External APIs**: HERE Maps, Stripe, Twilio, AWS services

## =� Documentation Statistics

- **Total Files**: 1,654
- **Hybrid Documentation**: 327 files
- **TSP API Documentation**: 589 files  
- **Other Components**: 738 files
- **Coverage**: 100% of source code documented

## =� Key Features Documented

### Mobility Services
- Ridehail integration (Uber, Lyft)
- Public transit integration
- Parking and bike sharing
- Carpool and ride matching
- Trip validation and incentives

### Platform Services
- User authentication and authorization
- Payment processing (Stripe integration)
- Notification system (push, SMS, email)
- Analytics and reporting
- Campaign management

### External Integrations
- **Maps**: HERE Maps, Google Maps, Mapbox
- **Payments**: Stripe payment processing
- **Communications**: Twilio SMS, email services
- **Cloud**: AWS S3, SQS, Pinpoint
- **Transit**: GTFS, real-time transit data

## =� How to Use This Documentation

1. **Browse by Service**: Navigate to specific service folders
2. **Search**: Use GitHub's search to find specific functions or features
3. **API Reference**: Check controller and service documentation for API details
4. **Database**: Review model and migration files for data structure

## = Version Information

- **Version**: v0629
- **Last Updated**: June 29, 2025
- **Documentation Status**: Complete (100% coverage)
- **Synchronization**: Perfect 1:1 mapping with source code

## =� Documentation Standards

All documentation follows these standards:
- **Comprehensive**: Every source file has corresponding documentation
- **Structured**: Consistent format with overview, technical specs, and examples
- **Searchable**: Tagged with relevant keywords and categories
- **Up-to-date**: Synchronized with latest source code changes

## =� Development Workflow

This documentation is automatically maintained and synchronized with the source codebase to ensure accuracy and completeness.

---

**Generated with Claude Code** | **MaaS Platform Technical Documentation** | **v0629**