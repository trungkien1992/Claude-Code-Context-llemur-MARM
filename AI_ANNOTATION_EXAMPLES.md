# AI-Readable Code Annotation Examples

This document demonstrates the AI annotation techniques applied throughout the codebase.

## Function-Level Annotations

### Example 1: API Endpoint with Comprehensive Context
```python
async def authenticate_user(email: str, password: str, request: Request) -> AuthResponse:
    """Authenticate user credentials and return JWT token
    
    @ai-context: Primary authentication endpoint for user login flow
    @security: Rate limited (5 attempts/minute), bcrypt password hashing, JWT signing
    @input-validation: Email format validation, password complexity requirements
    @error-handling: Returns 401 for invalid credentials, 429 for rate limit exceeded
    @performance: Redis cache for user lookup, async database queries
    @testing: Covered by test_auth.py - unit and integration tests
    @dependencies: user_service.py, jwt_utils.py, rate_limiter.py
    @usage-example: POST /auth/login with {"email": "user@example.com", "password": "..."}
    
    @implement:
        1. Validate email format and password requirements
        2. Check rate limiting for this IP/email combination
        3. Retrieve user from database with password hash
        4. Verify password using bcrypt.checkpw()
        5. Generate JWT token with user claims
        6. Log successful authentication for audit
        7. Return AuthResponse with token and user info
    """
    # Implementation here
```

### Example 2: Database Model with Context
```python
class UserModel:
    """User model with authentication and profile data
    
    @ai-context: Core user entity for authentication and profile management
    @database: PostgreSQL table with indexes on email and created_at
    @security: Password field excluded from JSON serialization, PII encrypted
    @relationships: One-to-many with sessions, many-to-many with roles
    @validation: Email uniqueness, password complexity, required fields
    @audit: Tracks created_at, updated_at, last_login timestamps
    @migrations: Use Alembic for schema changes, see migrations/versions/
    
    @schema-design:
        - Primary key: UUID for security and scalability
        - Email: Unique index, case-insensitive storage
        - Password: bcrypt hashed, never stored in plaintext
        - Profile fields: JSON column for flexible user data
    """
    # Model definition here
```

### Example 3: React Component with AI Guidance
```typescript
interface UserDashboardProps {
  userId: string;
  onUserUpdate?: (user: User) => void;
}

const UserDashboard: React.FC<UserDashboardProps> = ({ userId, onUserUpdate }) => {
  /**
   * User dashboard component with real-time updates and notifications
   * 
   * @ai-context: Main dashboard interface for authenticated users
   * @state-management: Uses Redux for user data, React Query for server state
   * @performance: Virtualized lists for large datasets, React.memo for optimization
   * @accessibility: ARIA labels, keyboard navigation, screen reader compatible
   * @responsive: Mobile-first design with breakpoints at 768px, 1024px
   * @testing: Component tests in UserDashboard.test.tsx using React Testing Library
   * 
   * @real-time: WebSocket connection for live notifications and updates
   * @error-boundary: Wrapped in ErrorBoundary for graceful failure handling
   * @loading-states: Skeleton UI during data fetching, proper loading indicators
   * @user-experience: Smooth transitions, optimistic updates, offline support
   * 
   * @integration:
   *   - User API: GET /api/users/:id for user data
   *   - Notifications: WebSocket /ws/notifications for real-time updates
   *   - Analytics: Track user interactions for dashboard optimization
   */
  
  // Component implementation here
};
```

## Class-Level Annotations

### Example 4: Service Class with Business Logic
```python
class PaymentProcessor:
    """Handles payment processing with multiple providers and fraud detection
    
    @ai-context: Core payment processing service with fraud prevention
    @providers: Stripe (primary), PayPal (fallback), Apple Pay (mobile)
    @security: PCI DSS compliant, tokenized card storage, fraud detection
    @reliability: Circuit breaker pattern, retry logic, idempotency keys
    @monitoring: Metrics for success rates, latency, fraud detection accuracy
    @compliance: GDPR data handling, PCI DSS requirements, audit logging
    
    @business-rules:
        - Maximum transaction: $10,000 per transaction, $50,000 per day
        - Fraud scoring: Machine learning model with 99.2% accuracy
        - Refund policy: Full refunds within 30 days, partial after
        - Currency support: USD, EUR, GBP with real-time conversion
    
    @error-handling:
        - Payment failures: Graceful degradation to backup providers
        - Network issues: Exponential backoff with jitter
        - Invalid cards: Clear user messaging without exposing details
        - Fraud detection: Silent blocking with admin notification
    
    @testing: Integration tests with payment provider sandboxes
    @documentation: Payment flow diagrams in docs/payments/
    """
    
    def __init__(self, config: PaymentConfig):
        # Initialize payment providers and fraud detection
        pass
```

## Configuration and Infrastructure

### Example 5: Docker Configuration
```dockerfile
# Dockerfile for production deployment
# @ai-context: Production-ready container with security and performance optimization
# @base-image: Node.js 18 Alpine for small attack surface and size
# @security: Non-root user, minimal package installation, security updates
# @performance: Multi-stage build, dependency caching, optimized layers
# @monitoring: Health check endpoint, proper logging configuration
# @deployment: Used with Kubernetes, supports horizontal scaling

FROM node:18-alpine as builder
# @build-stage: Compile TypeScript and bundle assets
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine as production
# @runtime-stage: Minimal runtime environment
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
WORKDIR /app
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --chown=nextjs:nodejs . .

USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["npm", "start"]
```

### Example 6: Database Migration
```sql
-- Migration: Add user roles and permissions system
-- @ai-context: Implements role-based access control (RBAC) for user management
-- @security: Granular permissions, principle of least privilege
-- @performance: Indexed foreign keys, optimized for permission checking queries
-- @rollback: Includes down migration for safe rollback capability
-- @data-migration: Assigns default 'user' role to existing users

-- @migration-safety:
--   - Non-blocking: Uses CREATE INDEX CONCURRENTLY
--   - Backward compatible: Nullable columns with sensible defaults
--   - Tested: Validated on staging with production data snapshot

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- @seed-data: Insert default roles for immediate functionality
INSERT INTO roles (name, description) VALUES 
    ('admin', 'Full system access'),
    ('user', 'Standard user permissions'),
    ('guest', 'Read-only access');

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- @permission-model: Resource-action based permissions for flexibility
INSERT INTO permissions (name, resource, action) VALUES
    ('users.read', 'users', 'read'),
    ('users.write', 'users', 'write'),
    ('admin.access', 'admin', 'access');
```

## Testing with AI Context

### Example 7: Comprehensive Test Suite
```typescript
describe('UserAuthentication', () => {
  /**
   * User authentication test suite with comprehensive coverage
   * 
   * @ai-context: Validates authentication flow security and functionality
   * @test-types: Unit tests, integration tests, security tests, performance tests
   * @coverage: Maintains >95% code coverage for authentication module
   * @security-testing: Validates against OWASP top 10, includes penetration test scenarios
   * @performance: Load testing for 1000 concurrent authentication requests
   * 
   * @test-data: Uses factory pattern for consistent test user generation
   * @mocking: Database calls mocked, external services use test doubles
   * @cleanup: Automatic test database cleanup after each test
   * @ci-integration: Runs on every PR, blocks merge on failure
   */

  describe('successful authentication', () => {
    it('should return JWT token for valid credentials', async () => {
      // @test-scenario: Happy path authentication with valid user
      // @expected-outcome: JWT token with proper claims and expiration
      // @security-check: Password not included in response payload
      
      const user = await createTestUser({
        email: 'test@example.com',
        password: 'SecurePassword123!'
      });

      const response = await request(app)
        .post('/auth/login')
        .send({ email: user.email, password: 'SecurePassword123!' })
        .expect(200);

      expect(response.body).toHaveProperty('token');
      expect(response.body).not.toHaveProperty('password');
      
      // @jwt-validation: Decode and validate token structure
      const decodedToken = jwt.verify(response.body.token, JWT_SECRET);
      expect(decodedToken).toHaveProperty('userId', user.id);
    });
  });

  describe('security validations', () => {
    it('should rate limit authentication attempts', async () => {
      // @security-test: Validates rate limiting implementation
      // @attack-simulation: Simulates brute force attack scenario
      // @expected-behavior: Returns 429 after 5 failed attempts
      
      const attempts = Array.from({ length: 6 }, () => 
        request(app)
          .post('/auth/login')
          .send({ email: 'test@example.com', password: 'wrong' })
      );

      const responses = await Promise.all(attempts);
      const lastResponse = responses[responses.length - 1];
      
      expect(lastResponse.status).toBe(429);
      expect(lastResponse.body.error).toMatch(/rate limit/i);
    });
  });
});
```

## Configuration Files with Context

### Example 8: Environment Configuration
```yaml
# docker-compose.yml - Development environment
# @ai-context: Local development setup with hot reload and debugging
# @purpose: Provides consistent development environment across team
# @services: Web app, database, Redis cache, background workers
# @networking: Internal Docker network with service discovery
# @data-persistence: Named volumes for database and Redis data
# @debugging: Exposes debugging ports, includes dev tools

version: '3.8'

services:
  web:
    # @service: Main web application with hot reload
    # @development: Volume mounting for live code updates
    # @debugging: Node.js inspector enabled on port 9229
    build: 
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"    # @port: Main application
      - "9229:9229"    # @port: Node.js debugger
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/app_dev
      - REDIS_URL=redis://redis:6379
    volumes:
      - .:/app:cached  # @volume: Live code reload
      - node_modules:/app/node_modules
    depends_on:
      - db
      - redis

  db:
    # @service: PostgreSQL database with persistent storage
    # @data-persistence: Named volume for database files
    # @configuration: Development settings, not for production use
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app_dev
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    ports:
      - "5432:5432"    # @port: Database access for debugging
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  postgres_data:     # @volume: Persistent database storage
  node_modules:      # @volume: Node modules cache for faster builds
```

## API Documentation with AI Context

### Example 9: OpenAPI Specification
```yaml
# @api-context: User management API with authentication and RBAC
# @security: JWT bearer token required for all authenticated endpoints
# @rate-limiting: 100 requests per minute per authenticated user
# @versioning: Semantic versioning with backward compatibility
# @error-handling: Consistent error response format across all endpoints

openapi: 3.0.3
info:
  title: User Management API
  description: |
    Comprehensive user management API with authentication and role-based access control.
    
    @ai-guidance:
      - Use consistent error handling patterns
      - Implement proper input validation for all endpoints
      - Follow REST conventions for resource naming
      - Include comprehensive request/response examples
  
  version: 2.1.0
  contact:
    name: Development Team
    email: dev@example.com

paths:
  /auth/login:
    post:
      # @endpoint-context: User authentication with JWT token generation
      # @security: Rate limited, password validation, audit logging
      # @error-scenarios: Invalid credentials (401), rate limit (429), server error (500)
      summary: Authenticate user and return JWT token
      description: |
        Validates user credentials and returns a JWT token for authenticated requests.
        
        @implementation-notes:
          - Passwords are validated against bcrypt hash
          - Rate limiting: 5 attempts per minute per IP
          - Successful logins are audited for security
          - Tokens expire after 24 hours
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                  example: "user@example.com"
                  # @validation: Email format, maximum 255 characters
                password:
                  type: string
                  minLength: 8
                  example: "SecurePassword123!"
                  # @security: Minimum 8 characters, complexity requirements
      
      responses:
        '200':
          description: Authentication successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                    description: JWT token for authenticated requests
                    # @token-format: Bearer token, 24-hour expiration
                  user:
                    $ref: '#/components/schemas/User'
                  expiresAt:
                    type: string
                    format: date-time
                    description: Token expiration timestamp
        '401':
          # @error-context: Invalid credentials or account locked
          description: Authentication failed
        '429':
          # @error-context: Rate limit exceeded for this IP/email
          description: Too many authentication attempts
```

These examples demonstrate comprehensive AI-readable code annotation techniques applied throughout the codebase, providing context for development, security, performance, testing, and maintenance concerns.