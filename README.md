# AI Agents Skills

A collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities.

## Available Skills

### react-anti-patterns

Inject React anti-patterns and performance pitfalls into existing React apps while keeping them functional, so teams can practice identifying and fixing issues.

#### Installation

```bash
npx skills add https://github.com/joacod/skills --skill react-anti-patterns
```

#### Example Invocations

```bash
# Defaults (medium, mixed levels, no comments)
/react-anti-patterns

# Few junior patterns with hints
/react-anti-patterns --comments-hint low junior

# Many senior patterns with full explanations
/react-anti-patterns --comments-fix high senior

# Medium amount, semi-senior level, identify comments
/react-anti-patterns --comments medium semi-senior
```

For more details, and different parameter options, see the [skill documentation](skills/react-anti-patterns/SKILL.md#react-anti-patterns)
