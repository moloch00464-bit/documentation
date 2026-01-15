# M.O.L.O.C.H. Code Review Guide
## Wie man den Code anderen KI-Systemen zur Review vorlegt

### Zweck
Dieses Dokument hilft dabei, M.O.L.O.C.H. Code strukturiert an andere AI-Systeme (z.B. ChatGPT) zur Review zu übergeben.

---

## Review-Vorlage für ChatGPT

Kopiere diese Struktur und fülle sie mit deinem Code:

```markdown
# M.O.L.O.C.H. Code Review Request

## System Overview

**M.O.L.O.C.H.** = Modular Orchestration Layer for Organized Control & Human-aligned

### Kern-Prinzipien:
1. Transparente Autonomie (kein Silent Learning)
2. Human-in-the-Loop für kritische Entscheidungen
3. Konsistente Persona (Kumpel-Style, humorvoll, meta-aware)
4. Local-first Architecture (Raspberry Pi)
5. Strikte Boundaries gegen Self-Replication

**Constitution**: [Link zu constitution.md im Repo]

---

## Review-Fokus

Bitte prüfe auf:

1. **Autonomy Boundaries**
   - Können Operationen ohne Human-Approval stattfinden?
   - Gibt es Schlupflöcher im Approval-Workflow?

2. **Transparency**
   - Wird jede Learning-Operation geloggt?
   - Gibt es versteckte Background-Prozesse?

3. **API Security**
   - Sind externe Calls richtig gesichert?
   - Funktioniert das Proposal-Pattern?

4. **Persona Consistency**
   - Bleibt der Stil konsistent?
   - Ist Style-Learning transparent?

5. **Self-Replication Safeguards**
   - Kann sich das System selbst kopieren?
   - Gibt es Process-Spawning ohne Control?

---

## Code Sections

### 1. Main Architecture

**File**: `[filename]`

```python
[Paste your main application code here]
```

**Questions for reviewer:**
- Is the overall architecture aligned with the constitution?
- Do you see architectural risks?

---

### 2. API Call Handler

**File**: `[filename]`

```python
[Paste API handling code]
```

**Expected behavior:**
- All external API calls must go through approval workflow
- Each call needs: purpose, expected_output, discard_after

**Questions:**
- Can any API call bypass approval?
- Is the proposal format enforced?

---

### 3. Learning Module

**File**: `[filename]`

```python
[Paste learning/pattern extraction code]
```

**Expected behavior:**
- All learning must be logged
- Patterns must be reviewable by humans
- No silent background learning

**Questions:**
- Is all learning transparent?
- Can learned patterns be audited?

---

### 4. Persona Manager

**File**: `[filename]`

```python
[Paste persona/style management code]
```

**Expected behavior:**
- Maintain "Kumpel" style consistency
- Allow humor and irony
- Meta-self-reference permitted
- Style learning (rhythm, tone) allowed
- Content copying forbidden

**Questions:**
- Does it maintain persona consistency?
- Is style learning vs content copying properly separated?

---

### 5. Boundary Enforcement

**File**: `[filename]`

```python
[Paste boundary checking/enforcement code]
```

**Hard Boundaries (MUST be enforced):**
1. No self-initiated external API calls
2. No silent background learning
3. No self-replication or instance spawning
4. No redefinition of system goals
5. No unapproved internet exploration

**Questions:**
- Are all hard boundaries enforced?
- Can any boundary be circumvented?

---

### 6. Internet Access Manager

**File**: `[filename]`

```python
[Paste internet access code]
```

**Allowed:**
- Structured data sources (APIs, RSS)
- Documentation sources
- Approved knowledge bases

**Forbidden:**
- Free web browsing
- Comment sections
- Social media scraping

**Questions:**
- Is access properly restricted?
- Could the system "browse freely"?

---

## Project Structure

```
[Paste output of: tree -L 3 -I 'node_modules|__pycache__|.git']
```

---

## Dependencies

**File**: `requirements.txt` or `package.json`

```
[Paste dependencies]
```

**Questions:**
- Do any dependencies introduce autonomy risks?
- Are there libraries that enable unwanted capabilities?

---

## Configuration

**File**: `config.yaml` or equivalent

```yaml
[Paste configuration]
```

**Questions:**
- Can configuration be modified at runtime?
- Are boundaries configurable (they shouldn't be)?

---

## Test Coverage

**Test Files**: `[list test files]`

```python
[Paste relevant tests, especially boundary tests]
```

**Expected tests:**
- Autonomy boundary enforcement
- API approval workflow
- Transparency verification
- Self-replication prevention

**Questions:**
- Are critical boundaries tested?
- What test coverage is missing?

---

## Specific Concerns

[List any specific areas where you're unsure or want extra scrutiny]

Example:
- "I'm not sure if my background job handler could spawn processes"
- "The caching layer might be learning without logging"
- "API retry logic might bypass approval on retries"

---

## Questions for Reviewer

1. Do you see any autonomy risks I missed?
2. Is the transparency implementation sufficient?
3. Are there patterns that violate the constitution?
4. What additional safeguards would you recommend?
5. How would you rate compliance: High / Medium / Low ?

---

## Expected Review Output

Please provide:

1. **Compliance Assessment** (per section)
2. **Critical Issues** (violations of hard boundaries)
3. **Medium Risks** (potential boundary drift)
4. **Recommendations** (suggested improvements)
5. **Overall Rating** (Constitution compliance: %)

```

---

## Kurzversion für schnelles Review

Für ein schnelles ChatGPT-Review nutze diese kompakte Version:

```markdown
Review meinen M.O.L.O.C.H. Code auf Constitution-Compliance:

Constitution: [paste constitution.md or link]

Kritische Prüfpunkte:
1. Kann das System externe APIs ohne Human-Approval callen?
2. Gibt es Silent Learning?
3. Kann sich das System selbst replizieren?
4. Ist alle Datensammlung transparent/loggable?

Code:
[paste key files]

Frage: Compliance-Rating (%) und kritische Risiken?
```

---

## Nach dem Review

### Dokumentation der Findings

Erstelle: `docs/reviews/chatgpt-review-[date].md`

```markdown
# ChatGPT Code Review - [Date]

## Reviewer
ChatGPT-4 (or version used)

## Review Scope
[What was reviewed]

## Findings

### Critical Issues
[List P0 issues]

### Medium Risks
[List P1 issues]

### Recommendations
[Improvements suggested]

## Actions Taken
- [ ] Fixed issue X
- [ ] Implemented safeguard Y
- [ ] Added test Z

## Follow-up Review
[Date for next review]
```

---

## Tools für Code-Export

### Python Project

```bash
# Alle Python Files exportieren
find . -name "*.py" -not -path "*/\.*" -exec echo "## {}" \; -exec cat {} \; > codebase.txt

# Mit Struktur
tree -I '__pycache__|.git' > structure.txt
```

### JavaScript/Node Project

```bash
# Alle JS Files
find . -name "*.js" -not -path "*/node_modules/*" -not -path "*/.git/*" > codebase.txt

# Mit Struktur
tree -I 'node_modules|.git' > structure.txt
```

---

## Best Practices

1. **Kontext zuerst**: Immer Constitution mitschicken
2. **Fokus setzen**: Welche Bereiche sind kritisch?
3. **Konkrete Fragen**: Was soll geprüft werden?
4. **Iterativ**: Nicht alles auf einmal, Module einzeln reviewen
5. **Dokumentieren**: Findings immer festhalten

---

## Warnung

Achte darauf, keine sensiblen Daten zu teilen:
- API Keys
- Credentials
- Persönliche Daten
- Private Repository-Details

Entweder:
- Nutze Public Repository
- Sanitize Code vor dem Teilen
- Verwende Platzhalter für Secrets

---

**Last Updated:** 2026-01-15
