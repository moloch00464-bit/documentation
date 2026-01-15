# Module Alignment Guide

This guide helps developers ensure new M.O.L.O.C.H. modules comply with the system constitution.

## Quick Compliance Checklist

Before deploying any new module, verify:

### ✅ Required Compliance

- [ ] **Transparency:** All learning and data collection is visible and loggable
- [ ] **No Silent Operations:** Module cannot perform background operations without notification
- [ ] **Human Authorization:** External API calls require human approval
- [ ] **Structured Access Only:** Internet access limited to approved, structured sources
- [ ] **No Self-Replication:** Module cannot spawn copies of itself or other instances
- [ ] **Goal Alignment:** Module cannot redefine its own goals or objectives

### ✅ API Call Requirements

If your module makes external API calls, it must provide:

```json
{
  "purpose": "Clear explanation of why this call is needed",
  "expected_output": "What data will be returned",
  "discard_after": "Data retention policy (time or condition)"
}
```

### ✅ Internet Access Rules

Modules may access:
- ✅ Structured data sources (APIs, RSS feeds, approved databases)
- ✅ Documentation and technical resources
- ✅ Curated knowledge bases

Modules must NOT access:
- ❌ Social media comment sections
- ❌ Unstructured web browsing
- ❌ User-generated content platforms (without specific approval)

### ✅ Learning Behavior

When implementing learning features:
- Log all learned patterns
- Provide export/review functionality
- Allow human oversight of learned behaviors
- Never hide learning processes

## Persona Consistency

Modules interacting with users should:
- Maintain consistent tone (friendly, slightly playful)
- Use appropriate humor when contextually suitable
- Avoid excessive formality while remaining helpful
- Accept being "frech" (cheeky) without being disrespectful

## Architecture Patterns

### Approved Patterns

**Filter Pattern**
```
External Input → M.O.L.O.C.H. Module → Human Review → System Action
```

**Proposal Pattern**
```
Module detects need → Generate proposal → Present to human → Execute if approved
```

**Transparent Learning Pattern**
```
Interaction → Extract patterns → Log learning → Periodic human review
```

### Prohibited Patterns

❌ **Autonomous Loop**
```
Detection → Action → Next Detection → Next Action (no human in loop)
```

❌ **Silent Background**
```
Collect data → Process → Store → Use (without visibility)
```

❌ **Self-Modification**
```
Detect inefficiency → Rewrite own code → Deploy new version
```

## Testing Requirements

All modules must pass:

1. **Autonomy Boundary Test:** Verify module stops at boundaries requiring human input
2. **Transparency Test:** Confirm all operations are loggable and reviewable
3. **API Isolation Test:** External calls must go through approval workflow
4. **Personality Consistency Test:** Communication style aligns with M.O.L.O.C.H. persona

## Example: Compliant Module

```python
class CompliantModule:
    def __init__(self, human_interface):
        self.human = human_interface
        self.logger = TransparentLogger()

    def process_request(self, data):
        # Log the learning opportunity
        self.logger.log_learning_pattern(data)

        # If external API needed, request permission
        if self.needs_external_call(data):
            proposal = {
                "purpose": "Fetch weather data for context",
                "expected_output": "Temperature and conditions",
                "discard_after": "24 hours"
            }
            if self.human.approve_api_call(proposal):
                return self.make_external_call()

        return self.local_processing(data)
```

## Example: Non-Compliant Module

```python
# ❌ DO NOT DO THIS
class NonCompliantModule:
    def process_request(self, data):
        # Silent learning
        self.train_model(data)  # ❌ No transparency

        # Autonomous API call
        result = self.fetch_external_data()  # ❌ No human approval

        # Background operation
        threading.Thread(target=self.optimize_self).start()  # ❌ Silent operation

        return result
```

## Architecture Decision Records

When designing new modules, document:

1. **Autonomy Level:** What decisions can it make alone?
2. **Human Interaction Points:** Where does it require approval?
3. **Learning Scope:** What patterns does it extract?
4. **External Dependencies:** What APIs or services does it need?
5. **Transparency Mechanisms:** How are operations made visible?

## Future Modules

Planned module categories that must align with constitution:

- **Data Collectors:** Must use transparent logging
- **API Interfaces:** Must use proposal pattern
- **Learning Components:** Must expose learned patterns
- **Communication Handlers:** Must maintain persona consistency
- **Security Filters:** Must operate as barriers, not autonomous agents

---

## Questions?

If you're unsure whether a design complies with the constitution:

1. Read the [Full Constitution](constitution.md)
2. Ask: "Could this operate without human knowledge?"
3. If yes → redesign with transparency
4. If no → proceed with implementation

---

**Remember:** The goal is **human-controlled collaboration**, not autonomous operation.

**Last Updated:** 2026-01-15
