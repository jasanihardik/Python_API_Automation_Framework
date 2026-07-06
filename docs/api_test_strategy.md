# API Test Strategy

## Objective

Validate the behavior, contract, authentication flow, and end-to-end booking workflow of a REST API using a reusable Python automation framework.

## Scope

The initial scope focuses on the Restful Booker API.

Covered areas:

- API availability
- Authentication
- Booking creation
- Booking retrieval
- Full booking update
- Partial booking update
- Booking deletion
- Unauthorized operation validation
- Invalid resource validation
- Schema/contract validation
- End-to-end workflow coverage

## Test Types

| Type | Purpose |
|---|---|
| Smoke | Confirm critical API availability |
| Functional | Validate endpoint behavior against expected results |
| Regression | Protect existing API behavior from breaking changes |
| Negative | Validate error handling and unauthorized scenarios |
| Contract | Validate response schema and structure |
| Workflow | Validate real business flow across multiple endpoints |

## Framework Principles

- Tests should not directly call `requests`.
- Endpoint classes should own endpoint-specific behavior.
- Common request logic should stay in the base API client.
- Test data should be reusable and easy to update.
- Schema validation should be separated from functional assertions.
- Setup and cleanup should be handled through fixtures.
- CI execution should produce a test report artifact.

## Stability Considerations

The target API is public and may be reset or temporarily unavailable. Tests use dynamic data, explicit cleanup, response time checks, and clear assertion messages to support troubleshooting.

## Future Enhancements

- Add OpenAPI specification validation
- Add retry only for safe health-check operations
- Add API coverage summary in README
- Add parallel execution using pytest-xdist
- Add Docker Compose profile for local mock APIs
- Add mock server tests for deterministic negative scenarios
- Add GitHub Actions badge after repository creation
