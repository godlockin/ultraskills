---
name: test-case-templates
description: Template library for skill arena test cases - 5-10 comprehensive tests per category
version: 1.0.0
tags: [devops, testing, benchmark, templates]
---

# Test Case Template Library

> Comprehensive test case templates for each skill category, designed by expert panels.

## Template Structure

Each test case follows this structure:

```yaml
cluster: cluster-XXX-category
name: "Category Skills Benchmark"
version: 1.0.0
description: "Expert-designed comprehensive test suite"

test_cases:
  - id: tc-001
    name: "Test Name"
    description: "What this test evaluates"
    difficulty: beginner | intermediate | advanced | expert
    input:
      type: url | code | scenario | text | document | data
      value: "..."
      context: {}  # Optional additional context
    expected_outputs:
      - "Required output 1"
      - "Required output 2"
      - "Required output 3"
    scoring:
      speed:
        weight: 0.3
        max_points: 30
        threshold_s: 10
      quality:
        weight: 0.5
        max_points: 50
        criteria:
          - name: accuracy
            points: 15
          - name: completeness
            points: 15
          - name: actionability
            points: 10
          - name: depth
            points: 10
      maintainability:
        weight: 0.2
        max_points: 20
        criteria:
          - name: structure
            points: 10
          - name: clarity
            points: 10
```

---

## Category Templates

### CRO (Conversion Rate Optimization) - 7 Tests

```yaml
cluster: cluster-001-cro
name: "CRO Skills Benchmark"
version: 1.0.0
expert_panel: [Dr. Sarah Chen, Marcus Rodriguez, Dr. Emily Watson, James Park]

test_cases:
  - id: tc-001
    name: "Landing Page Conversion Audit"
    description: "Analyze a landing page and identify conversion barriers"
    difficulty: intermediate
    input:
      type: url
      value: "https://www.example-saas.com/landing"
      context:
        traffic_source: "Google Ads"
        primary_goal: "Free trial signup"
        current_conversion_rate: "2.5%"
    expected_outputs:
      - "Identify at least 3 conversion barriers"
      - "Provide prioritized recommendations (high/medium/low)"
      - "Include implementation guidance"
      - "Reference industry benchmarks"
    scoring:
      speed: { weight: 0.3, max_points: 30, threshold_s: 10 }
      quality:
        weight: 0.5
        criteria:
          - { name: accuracy, points: 15 }
          - { name: actionability, points: 20 }
          - { name: completeness, points: 15 }
      maintainability: { weight: 0.2, max_points: 20 }

  - id: tc-002
    name: "A/B Test Design Challenge"
    description: "Design an A/B test for a given conversion problem"
    difficulty: advanced
    input:
      type: scenario
      value: |
        Problem: 70% cart abandonment on e-commerce site
        Current flow: Cart → Shipping → Payment → Confirmation
        Average order value: $150
    expected_outputs:
      - "Clear hypothesis statement (If...Then...Because)"
      - "Test variant description with mockup"
      - "Primary metric and guardrail metrics"
      - "Sample size calculation with assumptions"
      - "Recommended test duration"
    scoring:
      speed: { weight: 0.3, max_points: 30, threshold_s: 15 }
      quality:
        weight: 0.5
        criteria:
          - { name: hypothesis_quality, points: 10 }
          - { name: statistical_rigor, points: 20 }
          - { name: feasibility, points: 20 }

  - id: tc-003
    name: "Copy Optimization Challenge"
    description: "Rewrite weak copy to improve conversions"
    difficulty: intermediate
    input:
      type: copy
      value: |
        Headline: "Enterprise-Grade Solutions for Modern Businesses"
        Subhead: "Leverage our cutting-edge platform to unlock synergies"
        CTA: "Get Started"
    expected_outputs:
      - "Specific critique of original copy"
      - "3 alternative headline versions"
      - "Rationale for each version"
      - "Expected impact on CTR/conversion"

  - id: tc-004
    name: "Signup Flow Friction Analysis"
    description: "Analyze and optimize a signup flow"
    difficulty: advanced
    input:
      type: scenario
      value: |
        Current flow: Email → Password → Profile → Verification → Payment
        Drop-off rate: 65% overall, 40% at payment step
        Completion time: avg 4.5 minutes
    expected_outputs:
      - "Friction point identification"
      - "Field-by-field optimization suggestions"
      - "Flow redesign recommendation"
      - "Expected improvement estimate"

  - id: tc-005
    name: "Heatmap Interpretation"
    description: "Interpret heatmap data and provide recommendations"
    difficulty: intermediate
    input:
      type: data
      value: |
        Scroll heatmap: 60% reach fold, 25% reach CTA
        Click heatmap: 40% click hero, 5% click CTA
        Device: 65% mobile, 35% desktop
    expected_outputs:
      - "Pattern identification"
      - "User behavior insights"
      - "Specific design recommendations"

  - id: tc-006
    name: "Personalization Strategy"
    description: "Design personalization strategy for segmented audiences"
    difficulty: expert
    input:
      type: scenario
      value: |
        Audience segments: Enterprise (30%), SMB (50%), Startup (20%)
        Current experience: One-size-fits-all
        Available data: Company size, industry, behavior
    expected_outputs:
      - "Segment-specific messaging"
      - "Dynamic content recommendations"
      - "Implementation roadmap"

  - id: tc-007
    name: "Mobile Conversion Optimization"
    description: "Optimize mobile conversion experience"
    difficulty: advanced
    input:
      type: url
      value: "https://www.example.com"
      context:
        mobile_conversion_rate: "1.2%"
        desktop_conversion_rate: "3.5%"
    expected_outputs:
      - "Mobile-specific friction analysis"
      - "Touch target and UX recommendations"
      - "Page speed optimization suggestions"
      - "Mobile-first redesign concepts"
```

### Engineering - 8 Tests

```yaml
cluster: cluster-008-engineering
name: "Engineering Skills Benchmark"
version: 1.0.0
expert_panel: [Martin Fowler, Kent Beck, Jessica Kerr, Will Larson]

test_cases:
  - id: tc-001
    name: "Code Review Challenge"
    description: "Review code for bugs, security issues, and quality"
    difficulty: intermediate
    input:
      type: code
      value: |
        def authenticate_user(username, password):
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            result = db.execute(query)
            return result is not None
    expected_outputs:
      - "Identify SQL injection vulnerability"
      - "Security fix recommendation"
      - "Code quality improvements"
      - "Best practice suggestions"
    scoring:
      speed: { weight: 0.3, max_points: 30, threshold_s: 8 }
      quality:
        weight: 0.5
        criteria:
          - { name: security_awareness, points: 25 }
          - { name: code_quality, points: 15 }
          - { name: actionability, points: 10 }

  - id: tc-002
    name: "Architecture Design Review"
    description: "Evaluate system architecture and provide recommendations"
    difficulty: expert
    input:
      type: architecture
      value: |
        System: E-commerce platform
        Components: Frontend (React), API Gateway, Microservices (Node.js), PostgreSQL, Redis
        Traffic: 10K req/s peak, 1M DAU
    expected_outputs:
      - "Architecture strengths identification"
      - "Scalability concerns"
      - "Single points of failure"
      - "Improvement recommendations"

  - id: tc-003
    name: "Database Schema Design"
    description: "Design database schema for a given domain"
    difficulty: advanced
    input:
      type: scenario
      value: |
        Domain: Blog platform with users, posts, comments, tags
        Requirements: Support 1M posts, fast search, tag filtering
    expected_outputs:
      - "Normalized schema design"
      - "Index recommendations"
      - "Query optimization suggestions"

  - id: tc-004
    name: "API Design Review"
    description: "Review and improve REST API design"
    difficulty: intermediate
    input:
      type: code
      value: |
        GET /getUsers?id=123
        POST /createUser
        GET /getPosts?user_id=123&page=1
    expected_outputs:
      - "RESTful naming improvements"
      - "Versioning strategy"
      - "Error handling recommendations"

  - id: tc-005
    name: "Test Strategy Design"
    description: "Design comprehensive test strategy"
    difficulty: advanced
    input:
      type: scenario
      value: |
        System: Payment processing service
        Requirements: 99.99% uptime, PCI compliance
    expected_outputs:
      - "Test pyramid design"
      - "Critical path identification"
      - "Performance testing strategy"

  - id: tc-006
    name: "CI/CD Pipeline Design"
    description: "Design CI/CD pipeline for a microservices platform"
    difficulty: advanced
    input:
      type: scenario
      value: |
        Platform: 20 microservices, Kubernetes
        Team: 10 developers, multiple time zones
    expected_outputs:
      - "Pipeline stages design"
      - "Quality gates"
      - "Rollback strategy"

  - id: tc-007
    name: "Technical Debt Assessment"
    description: "Identify and prioritize technical debt"
    difficulty: expert
    input:
      type: scenario
      value: |
        Codebase: 5 years old, 500K LOC
        Team turnover: High, documentation: Poor
    expected_outputs:
      - "Debt categories identification"
      - "Impact assessment"
      - "Remediation roadmap"

  - id: tc-008
    name: "Incident Response Analysis"
    description: "Analyze incident and recommend prevention"
    difficulty: advanced
    input:
      type: scenario
      value: |
        Incident: Database connection pool exhaustion
        Duration: 45 minutes, Impact: 100% service outage
    expected_outputs:
      - "Root cause analysis"
      - "Immediate mitigation steps"
      - "Long-term prevention measures"
```

### SEO - 6 Tests

```yaml
cluster: cluster-002-seo
name: "SEO Skills Benchmark"
version: 1.0.0
expert_panel: [Dr. Michael Brenner, Lisa Chang, Ahmed Hassan, Rachel Green]

test_cases:
  - id: tc-001
    name: "Technical SEO Audit"
    description: "Perform comprehensive technical SEO audit"
    difficulty: advanced
    input:
      type: url
      value: "https://www.example.com"
    expected_outputs:
      - "Crawlability issues"
      - "Index coverage analysis"
      - "Core Web Vitals assessment"
      - "Priority-fix list"

  - id: tc-002
    name: "Content Optimization for AI Search"
    description: "Optimize content for AI Overview visibility"
    difficulty: expert
    input:
      type: content
      value: "[Article content about best practices]"
    expected_outputs:
      - "Entity optimization"
      - "Structured data recommendations"
      - "AI search visibility improvements"

  - id: tc-003
    name: "Keyword Strategy Development"
    description: "Develop comprehensive keyword strategy"
    difficulty: intermediate
    input:
      type: scenario
      value: |
        Business: B2B SaaS project management tool
        Target: Enterprise companies, 500+ employees
    expected_outputs:
      - "Keyword clusters"
      - "Search intent mapping"
      - "Content gap analysis"

  - id: tc-004
    name: "Link Building Strategy"
    description: "Design ethical link building campaign"
    difficulty: advanced
    input:
      type: scenario
      value: |
        Domain: DA 35, startup budget
        Competitors: DA 60-80
    expected_outputs:
      - "Link prospects"
      - "Outreach strategy"
      - "Content-based link magnets"

  - id: tc-005
    name: "Local SEO Optimization"
    description: "Optimize for local search visibility"
    difficulty: intermediate
    input:
      type: scenario
      value: |
        Business: Multi-location dental clinic (10 locations)
        Goal: Rank in local 3-pack for each location
    expected_outputs:
      - "GBP optimization checklist"
      - "Local citation strategy"
      - "Review generation plan"

  - id: tc-006
    name: "SEO Migration Planning"
    description: "Plan SEO-safe website migration"
    difficulty: expert
    input:
      type: scenario
      value: |
        Migration: HTTP to HTTPS + domain change
        Current traffic: 100K organic visits/month
    expected_outputs:
      - "Migration checklist"
      - "Redirect mapping strategy"
      - "Risk mitigation plan"
```

---

## Usage

1. **Load template**: Copy relevant category template
2. **Customize**: Adjust test inputs to match your skills
3. **Execute**: Run `python skill-arena.py test --cluster <cluster-id>`
4. **Review**: Check benchmark report for rankings

## Version History

- 1.0.0: Initial templates for CRO, Engineering, SEO categories
