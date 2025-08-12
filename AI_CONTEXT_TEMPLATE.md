# AI Context Template for Claude Code Integration

## Project Context Specification (PCS)

### Core Information
```markdown
# Add to notebook with: ctx notebook add "project_type" "web_application"
- **Project Type**: [web_application|api_service|data_pipeline|mobile_app]
- **Primary Language**: [typescript|python|java|go]
- **Framework**: [react|nextjs|django|fastapi|spring|gin]
- **Database**: [postgresql|mongodb|redis|mysql]
- **Deployment**: [docker|kubernetes|serverless|traditional]
```

### Architecture Context
```bash
# Store architecture decisions
ctx notebook add "architecture_style" "microservices_with_api_gateway"
ctx notebook add "data_flow" "event_driven_with_message_queues"
ctx notebook add "auth_strategy" "jwt_with_refresh_tokens"
```

### Development Context
```bash
# Current development focus
ctx notebook add "current_sprint" "user_authentication_system"
ctx notebook add "active_feature" "social_login_integration"
ctx notebook add "technical_debt" "refactor_user_model_validation"
```

### AI Guidance Annotations
```bash
# Specific AI instructions
ctx notebook add "coding_style" "functional_components_with_hooks"
ctx notebook add "error_handling" "custom_error_classes_with_logging"
ctx notebook add "testing_approach" "unit_tests_with_jest_integration_with_cypress"
ctx notebook add "security_focus" "input_validation_and_sql_injection_prevention"
```

## Claude Code AI Context Commands

### Essential Context Preparation
```bash
# Compile comprehensive context for AI
ctx compile "ai-development-context"
ctx compile export-md "ai-development-context" --output .context/current-session.md

# Prepare for Claude Code session
python src/claude_integration.py --copy
```

### Session Management
```bash
# Start new development session
ctx notebook add "session_goal" "implement_user_registration_api"
ctx notebook add "session_blockers" "database_schema_needs_migration"

# End session documentation
ctx notebook add "session_completed" "user_registration_endpoints_functional"
ctx notebook add "next_session" "implement_email_verification_flow"
```

### Context Sharing
```bash
# Export for team collaboration
ctx compile export-md "team-handoff" --output docs/dev-sessions/$(date +%Y-%m-%d)-handoff.md

# Import insights from Claude artifacts
ctx compile import-artifacts claude-suggestions.json
```

## AI-Readable Code Patterns

### Function Documentation
```python
def authenticate_user(email: str, password: str) -> AuthResult:
    """Authenticate user with email and password
    
    @ai-context: This is the main authentication entry point
    @security: Implements rate limiting and password hashing validation
    @returns: AuthResult with user data or error details
    @related: user_model.py, auth_middleware.py
    """
```

### API Endpoint Context
```typescript
// @ai-context: User registration endpoint with validation
// @security: Rate limited, input sanitized, password complexity enforced
// @testing: Covered by auth.test.ts integration tests
// @dependencies: user.model.ts, validation.middleware.ts
export async function registerUser(req: Request, res: Response) {
    // Implementation
}
```

### Configuration Context
```yaml
# docker-compose.yml
# @ai-context: Development environment setup
# @purpose: Local development with hot reload and debugging
# @security: Development secrets only, not for production
services:
  web:
    build: .
    ports:
      - "3000:3000"
```

## Best Practices for Claude Code

### 1. Pre-Session Setup
```bash
# Before starting Claude Code session
ctx notebook list  # Review current context
ctx compile "current-state"  # Create snapshot
python src/claude_integration.py  # Show context
```

### 2. During Development
```bash
# Add insights as you work
ctx notebook add "current_bug" "validation_middleware_not_catching_edge_case"
ctx notebook add "solution_approach" "add_custom_validator_for_nested_objects"
```

### 3. Post-Session
```bash
# Capture what was accomplished
ctx notebook add "completed_today" "user_registration_api_with_validation"
ctx notebook add "lessons_learned" "middleware_order_matters_for_validation"
ctx compile "session-$(date +%Y-%m-%d)"
```

## Integration with Existing Tools

### Git Integration
```bash
# Git hooks for automatic context updates
# .git/hooks/post-commit
ctx notebook add "last_commit" "$(git log -1 --oneline)"
ctx compile "auto-snapshot-$(git rev-parse --short HEAD)"
```

### CI/CD Integration
```yaml
# .github/workflows/context-update.yml
name: Update AI Context
on: [push]
jobs:
  update-context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update development context
        run: |
          ctx compile "ci-snapshot-${{ github.sha }}"
          ctx compile export-md "ci-snapshot-${{ github.sha }}" --output .context/latest.md
```

## Advanced Patterns

### Multi-Repository Context
```bash
# Share context across related projects
ctx compile export-md "microservice-auth-api" --output ../shared-context/auth-api.md
ctx compile export-md "frontend-client" --output ../shared-context/frontend.md
```

### Team Collaboration
```bash
# Morning standup context preparation
ctx compile "daily-standup-$(date +%Y-%m-%d)"
ctx compile export-md "daily-standup-$(date +%Y-%m-%d)" --output standup-notes.md
```

This template provides the foundation for implementing AI-readable code practices specifically with Claude Code and our MARM memory system.