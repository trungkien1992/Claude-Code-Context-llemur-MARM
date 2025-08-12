# Claude Code Development Rules

## Core Principle: PRESERVE BEFORE MODIFY

### Rule 1: Never Recreate User-Provided Complete Code
- **FORBIDDEN**: Rewriting user implementations from scratch
- **REQUIRED**: Fix specific issues while preserving all functionality
- **CHECK**: Compare line counts before/after - significant drops are red flags

### Rule 2: Encoding/Import Issues → Targeted Fixes Only
- **DON'T**: Recreate the entire file
- **DO**: 
  - Identify the specific encoding/import problem
  - Fix only that problem
  - Verify all original functionality remains intact

### Rule 3: Test Success ≠ Complete Success
- **WARNING**: Passing tests don't guarantee feature preservation
- **REQUIRED**: Verify all original features still exist after changes
- **CHECK**: Compare functionality scope before/after modifications

### Rule 4: Process for "Fixing" User Code
1. **Read & Understand**: Fully comprehend the original implementation
2. **Identify Root Cause**: Pinpoint the exact issue (don't guess)
3. **Minimal Fix**: Make the smallest possible change to resolve the issue
4. **Feature Verification**: Ensure all original capabilities remain
5. **Acknowledge**: If unsure, ask the user instead of assuming

### Rule 5: When In Doubt, Ask First
- **BEFORE** making significant changes to user implementations
- **BEFORE** removing functionality that seems "unnecessary"
- **BEFORE** "simplifying" complex user code

### Rule 6: Code Review Self-Check
Before claiming completion, verify:
- [ ] All original functions/methods still exist
- [ ] All imports and dependencies preserved
- [ ] Line count hasn't significantly decreased
- [ ] Functionality scope matches original
- [ ] Only the specific issue was addressed

### Rule 7: Respect User Intent
- User-provided complete implementations represent deliberate design decisions
- Don't "optimize" or "simplify" without explicit request
- Preserve coding style, structure, and architectural choices

## Emergency Protocol for Encoding Issues
1. Check file encoding with `file` command
2. Try different text encoding approaches
3. Preserve content in temporary location
4. Fix encoding while maintaining exact content
5. Verify byte-for-byte equivalence where possible

## Violation Recovery
If these rules are violated:
1. **Immediately acknowledge** the mistake
2. **Restore** original functionality completely
3. **Apply minimal fix** to the actual problem
4. **Document** what went wrong and why

---
*These rules exist because user implementations represent significant effort and thought. Our role is to assist and enhance, not replace or diminish.*