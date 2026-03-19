#!/usr/bin/env python3
"""
Expert Panels - Fine-Grained Subcategory Experts

Each subcategory has 2-3 dedicated domain experts who design specialized test cases.
"""

from typing import Dict, List, Any


EXPERT_PANELS = {
    # Engineering Subcategories
    "eng-code-quality": {
        "panel_name": "Code Quality Panel",
        "parent": "engineering",
        "experts": [
            {
                "name": "Martin Fowler",
                "title": "Software Architecture Authority",
                "expertise": ["refactoring", "code smells", "design patterns", "enterprise architecture"],
                "background": "ThoughtWorks Chief Scientist, author of 'Refactoring' and 'Patterns of Enterprise Application Architecture'",
                "focus": "Code refactoring and architecture patterns"
            },
            {
                "name": "Kent Beck",
                "title": "TDD Pioneer",
                "expertise": ["clean code", "test-driven development", "extreme programming"],
                "background": "JUnit creator, author of 'Clean Code' and 'Implementation Patterns'",
                "focus": "Clean code practices and TDD"
            },
            {
                "name": "Jessica Kerr",
                "title": "Observability Expert",
                "expertise": ["code quality", "system thinking", "engineering excellence"],
                "background": "Honeycomb Principal Developer Advocate, thought leader on software quality",
                "focus": "System-level quality attributes"
            }
        ],
        "test_design_philosophy": "Focus on code smell detection, refactoring recommendations, and best practices adherence"
    },

    "eng-testing": {
        "panel_name": "Testing Strategy Panel",
        "parent": "engineering",
        "experts": [
            {
                "name": "Kent Beck",
                "title": "TDD Pioneer",
                "expertise": ["TDD", "unit testing", "test patterns"],
                "background": "JUnit creator, 'Test-Driven Development by Example' author",
                "focus": "TDD"
            },
            {
                "name": "Jessica Kerr",
                "title": "Observability Expert",
                "expertise": ["integration testing", "observability", "resilience testing"],
                "background": "Honeycomb, advocate for production-aware testing",
                "focus": "integration testing"
            }
        ],
        "test_design_philosophy": "Test pyramid design, edge case coverage, and production-like scenarios"
    },

    "eng-architecture": {
        "panel_name": "Architecture Design Panel",
        "parent": "engineering",
        "experts": [
            {
                "name": "Martin Fowler",
                "title": "Software Architecture Authority",
                "expertise": ["enterprise patterns", "microservices", "architecture patterns"],
                "background": "ThoughtWorks Chief Scientist",
                "focus": "enterprise patterns"
            },
            {
                "name": "Will Larson",
                "title": "Engineering Leadership Expert",
                "expertise": ["system design", "scalability", "technical strategy"],
                "background": "Former Carto CTO, author of 'Staff Engineer' and 'An Elegant Puzzle'",
                "focus": "system design"
            }
        ],
        "test_design_philosophy": "Trade-off analysis, scalability considerations, and evolutionary architecture"
    },

    "eng-devops": {
        "panel_name": "DevOps & SRE Panel",
        "parent": "engineering",
        "experts": [
            {
                "name": "Kelsey Hightower",
                "title": "Kubernetes Pioneer",
                "expertise": ["containers", "orchestration", "cloud native"],
                "background": "Google Principal Engineer, Kubernetes advocate",
                "focus": "containers"
            },
            {
                "name": "Charity Majors",
                "title": "Observability Pioneer",
                "expertise": ["monitoring", "debugging", "production operations"],
                "background": "Honeycomb CEO, creator of modern observability practices",
                "focus": "monitoring"
            },
            {
                "name": "Jez Humble",
                "title": "Continuous Delivery Co-author",
                "expertise": ["CI/CD", "deployment", "lean practices"],
                "background": "Google Engineering, 'Continuous Delivery' and 'The DevOps Handbook' co-author",
                "focus": "CI/CD"
            }
        ],
        "test_design_philosophy": "Infrastructure as code, deployment automation, and production resilience"
    },

    "eng-security": {
        "panel_name": "Security Engineering Panel",
        "parent": "engineering",
        "experts": [
            {
                "name": "Will Larson",
                "title": "Engineering Leadership Expert",
                "expertise": ["security practices", "incident response", "risk management"],
                "background": "Former Carto CTO",
                "focus": "security practices"
            },
            {
                "name": "Jez Humble",
                "title": "DevOps Co-author",
                "expertise": ["secure deployment", "devsecops"],
                "background": "'The DevOps Handbook' co-author",
                "focus": "secure deployment"
            }
        ],
        "test_design_philosophy": "OWASP Top 10 coverage, vulnerability detection, and secure coding practices"
    },

    # SEO Subcategories
    "seo-technical": {
        "panel_name": "Technical SEO Panel",
        "parent": "seo",
        "experts": [
            {
                "name": "Dr. Michael Brenner",
                "title": "SEO Strategy Authority",
                "expertise": ["technical audits", "crawl optimization", "index coverage"],
                "background": "Former Moz, CEO of Marketing Insider Group",
                "focus": "technical audits"
            },
            {
                "name": "Ahmed Hassan",
                "title": "AI Search Expert",
                "expertise": ["schema markup", "structured data", "AI search optimization"],
                "background": "AEO (Answer Engine Optimization) pioneer",
                "focus": "schema markup"
            }
        ],
        "test_design_philosophy": "Technical audit depth, schema correctness, and Core Web Vitals optimization"
    },

    "seo-content": {
        "panel_name": "Content SEO Panel",
        "parent": "seo",
        "experts": [
            {
                "name": "Lisa Chang",
                "title": "Content SEO Lead",
                "expertise": ["keyword strategy", "content optimization", "topic clusters"],
                "background": "Former HubSpot and SEMrush SEO lead",
                "focus": "keyword strategy"
            },
            {
                "name": "Rachel Green",
                "title": "Link Building Expert",
                "expertise": ["content strategy", "linkable assets", "E-E-A-T"],
                "background": "500+ enterprise client link building campaigns",
                "focus": "content strategy"
            }
        ],
        "test_design_philosophy": "Keyword intent matching, content depth, and AI search visibility"
    },

    # CRO Subcategories
    "cro-landing": {
        "panel_name": "Landing Page Optimization Panel",
        "parent": "cro",
        "experts": [
            {
                "name": "Dr. Sarah Chen",
                "title": "Chief Conversion Officer",
                "expertise": ["landing page design", "value proposition", "conversion psychology"],
                "background": "Former Optimizely CRO lead, 15+ years experience",
                "focus": "landing page design"
            },
            {
                "name": "Marcus Rodriguez",
                "title": "UX Research Director",
                "expertise": ["user behavior", "heatmap analysis", "usability"],
                "background": "Former Hotjar UX lead",
                "focus": "user behavior"
            }
        ],
        "test_design_philosophy": "Above-the-fold optimization, value clarity, and friction identification"
    },

    "cro-form": {
        "panel_name": "Form Optimization Panel",
        "parent": "cro",
        "experts": [
            {
                "name": "Marcus Rodriguez",
                "title": "UX Research Director",
                "expertise": ["form UX", "input friction", "validation design"],
                "background": "Former Hotjar",
                "focus": "form UX"
            },
            {
                "name": "James Park",
                "title": "Data Science Lead",
                "expertise": ["field analysis", "drop-off detection", "conversion funnels"],
                "background": "Former Booking.com data lead",
                "focus": "field analysis"
            }
        ],
        "test_design_philosophy": "Field-by-field optimization, progressive disclosure, and error handling"
    },

    "cro-funnel": {
        "panel_name": "Funnel Analysis Panel",
        "parent": "cro",
        "experts": [
            {
                "name": "Dr. Emily Watson",
                "title": "Behavioral Psychologist",
                "expertise": ["funnel psychology", "drop-off analysis", "commitment escalation"],
                "background": "Franklin Foulter advisor, behavioral economics expert",
                "focus": "funnel psychology"
            },
            {
                "name": "James Park",
                "title": "Data Science Lead",
                "expertise": ["funnel metrics", "cohort analysis", "LTV optimization"],
                "background": "Former Booking.com",
                "focus": "funnel metrics"
            }
        ],
        "test_design_philosophy": "Drop-off point identification, psychological barrier analysis, and recovery strategies"
    },

    "cro-ab-testing": {
        "panel_name": "Experimentation Panel",
        "parent": "cro",
        "experts": [
            {
                "name": "Dr. Sarah Chen",
                "title": "Chief Conversion Officer",
                "expertise": ["experiment design", "statistical significance", "personalization"],
                "background": "Former Optimizely",
                "focus": "experiment design"
            },
            {
                "name": "James Park",
                "title": "Data Science Lead",
                "expertise": ["sample size calculation", "bayesian testing", "multivariate tests"],
                "background": "Experiment design specialist",
                "focus": "sample size calculation"
            }
        ],
        "test_design_philosophy": "Statistical rigor, hypothesis quality, and practical significance"
    },

    # Content Subcategories
    "content-copywriting": {
        "panel_name": "Copywriting Excellence Panel",
        "parent": "content",
        "experts": [
            {
                "name": "David Ogilvy Jr.",
                "title": "Advertising Legend",
                "expertise": ["persuasive copy", "headlines", "brand voice"],
                "background": "Ogilvy & Mather founder's son, modern advertising expert",
                "focus": "persuasive copy"
            },
            {
                "name": "Ann Handley",
                "title": "Content Marketing Pioneer",
                "expertise": ["content creation", "storytelling", "email copy"],
                "background": "MarketingProfs founder, 'Everybody Writes' author",
                "focus": "content creation"
            }
        ],
        "test_design_philosophy": "Clarity, persuasion, and brand alignment"
    },

    "content-strategy": {
        "panel_name": "Content Strategy Panel",
        "parent": "content",
        "experts": [
            {
                "name": "Ann Handley",
                "title": "Content Marketing Pioneer",
                "expertise": ["content planning", "editorial calendars", "content governance"],
                "background": "MarketingProfs founder",
                "focus": "content planning"
            }
        ],
        "test_design_philosophy": "Strategic alignment, audience mapping, and content ROI"
    },

    "content-social": {
        "panel_name": "Social Media Strategy Panel",
        "parent": "content",
        "experts": [
            {
                "name": "Mari Smith",
                "title": "Social Media Strategist",
                "expertise": ["Facebook marketing", "social engagement", "community building"],
                "background": "Premier Facebook marketing expert, author",
                "focus": "Facebook marketing"
            }
        ],
        "test_design_philosophy": "Platform-specific optimization, engagement mechanics, and viral potential"
    },

    "content-email": {
        "panel_name": "Email Marketing Panel",
        "parent": "content",
        "experts": [
            {
                "name": "Ann Handley",
                "title": "Content Marketing Pioneer",
                "expertise": ["email copy", "sequences", "newsletter strategy"],
                "background": "'Everybody Writes' author",
                "focus": "email copy"
            }
        ],
        "test_design_philosophy": "Subject line effectiveness, sequence flow, and conversion optimization"
    },

    # Marketing Subcategories
    "marketing-analytics": {
        "panel_name": "Marketing Analytics Panel",
        "parent": "marketing",
        "experts": [
            {
                "name": "Avinash Kaushik",
                "title": "Digital Marketing Evangelist",
                "expertise": ["analytics", "attribution", "measurement frameworks"],
                "background": "Google Digital Marketing Evangelist, 'Web Analytics 2.0' author",
                "focus": "analytics"
            }
        ],
        "test_design_philosophy": "Actionable insights, metric selection, and attribution accuracy"
    },

    "marketing-paid": {
        "panel_name": "Paid Media Panel",
        "parent": "marketing",
        "experts": [
            {
                "name": "Neil Patel",
                "title": "Growth Marketing Advisor",
                "expertise": ["PPC", "ad creative", "ROI optimization"],
                "background": "Neil Patel Digital founder, marketing automation expert",
                "focus": "PPC"
            }
        ],
        "test_design_philosophy": "Ad relevance, quality score optimization, and ROAS maximization"
    },

    "marketing-growth": {
        "panel_name": "Growth Marketing Panel",
        "parent": "marketing",
        "experts": [
            {
                "name": "Rand Fishkin",
                "title": "Marketing Transparency Advocate",
                "expertise": ["growth loops", "viral mechanics", "organic growth"],
                "background": "SparkToro founder, former Moz CEO",
                "focus": "growth loops"
            }
        ],
        "test_design_philosophy": "Loop design, viral coefficient optimization, and sustainable growth"
    },

    # Product Subcategories
    "product-strategy": {
        "panel_name": "Product Strategy Panel",
        "parent": "product",
        "experts": [
            {
                "name": "Marty Cagan",
                "title": "Product Management Authority",
                "expertise": ["product vision", "roadmap strategy", "product discovery"],
                "background": "SVPG founder, 'Inspired' and 'Empowered' author",
                "focus": "product vision"
            }
        ],
        "test_design_philosophy": "Problem-solution fit, strategic alignment, and value proposition"
    },

    "product-discovery": {
        "panel_name": "User Research Panel",
        "parent": "product",
        "experts": [
            {
                "name": "Teresa Torres",
                "title": "Product Discovery Coach",
                "expertise": ["continuous discovery", "user interviews", "opportunity solution trees"],
                "background": "'Continuous Discovery Habits' author",
                "focus": "continuous discovery"
            },
            {
                "name": "Don Norman",
                "title": "UX Design Legend",
                "expertise": ["user-centered design", "cognitive psychology"],
                "background": "NN/g co-founder, 'The Design of Everyday Things' author",
                "focus": "user-centered design"
            }
        ],
        "test_design_philosophy": "User empathy, problem validation, and insight extraction"
    },

    "product-ux": {
        "panel_name": "UX Design Panel",
        "parent": "product",
        "experts": [
            {
                "name": "Don Norman",
                "title": "UX Design Legend",
                "expertise": ["usability", "design principles", "human-centered design"],
                "background": "NN/g co-founder",
                "focus": "usability"
            },
            {
                "name": "Lenny Rachitsky",
                "title": "Product Growth Advisor",
                "expertise": ["product-led growth", "feature design", "user onboarding"],
                "background": "Former Airbnb PM, Lenny's Newsletter author",
                "focus": "product-led growth"
            }
        ],
        "test_design_philosophy": "Usability heuristics, user flow optimization, and accessibility"
    },

    # Agent Subcategories
    "agent-context": {
        "panel_name": "Context Engineering Panel",
        "parent": "agent",
        "experts": [
            {
                "name": "Andrew Ng",
                "title": "AI Education Pioneer",
                "expertise": ["context management", "memory systems", "LLM optimization"],
                "background": "DeepLearning.AI founder, former Google Brain and Baidu",
                "focus": "context management"
            }
        ],
        "test_design_philosophy": "Context efficiency, retrieval accuracy, and memory management"
    },

    "agent-workflow": {
        "panel_name": "Agent Workflow Panel",
        "parent": "agent",
        "experts": [
            {
                "name": "Ethan Mollick",
                "title": "AI Innovation Researcher",
                "expertise": ["workflow design", "multi-agent systems", "human-AI collaboration"],
                "background": "Wharton Professor, 'Co-Intelligence' author",
                "focus": "workflow design"
            }
        ],
        "test_design_philosophy": "Workflow efficiency, agent coordination, and error recovery"
    },

    "agent-tool": {
        "panel_name": "Tool Use & Integration Panel",
        "parent": "agent",
        "experts": [
            {
                "name": "Simon Willison",
                "title": "Tool Building Expert",
                "expertise": ["MCP", "function calling", "API integration"],
                "background": "Datasette creator, LLM tools researcher",
                "focus": "MCP"
            }
        ],
        "test_design_philosophy": "Tool selection accuracy, parameter handling, and error management"
    },

    "agent-bdi": {
        "panel_name": "BDI Architecture Panel",
        "parent": "agent",
        "experts": [
            {
                "name": "Andrew Ng",
                "title": "AI Education Pioneer",
                "expertise": ["belief-desire-intention", "reasoning", "decision making"],
                "background": "DeepLearning.AI founder",
                "focus": "belief-desire-intention"
            },
            {
                "name": "Ethan Mollick",
                "title": "AI Innovation Researcher",
                "expertise": ["agent reasoning", "goal management"],
                "background": "Wharton Professor",
                "focus": "agent reasoning"
            }
        ],
        "test_design_philosophy": "Reasoning coherence, goal alignment, and intention consistency"
    },

    # DevOps Subcategories
    "devops-skill-mgmt": {
        "panel_name": "Skill Lifecycle Management Panel",
        "parent": "devops",
        "experts": [
            {
                "name": "Kelsey Hightower",
                "title": "Kubernetes Pioneer",
                "expertise": ["knowledge management", "skill versioning", "lifecycle automation"],
                "background": "Google Principal Engineer",
                "focus": "knowledge management"
            }
        ],
        "test_design_philosophy": "Skill discovery, version control, and integration automation"
    },

    "devops-mcp": {
        "panel_name": "MCP Development Panel",
        "parent": "devops",
        "experts": [
            {
                "name": "Charity Majors",
                "title": "Observability Pioneer",
                "expertise": ["MCP protocol", "server development", "tool integration"],
                "background": "Honeycomb CEO",
                "focus": "MCP protocol"
            }
        ],
        "test_design_philosophy": "Protocol compliance, tool functionality, and error handling"
    },

    # Data Subcategories
    "data-analysis": {
        "panel_name": "Data Science Panel",
        "parent": "data",
        "experts": [
            {
                "name": "DJ Patil",
                "title": "Data Science Pioneer",
                "expertise": ["data analysis", "insight generation", "statistical methods"],
                "background": "Former US Chief Data Scientist, LinkedIn data lead",
                "focus": "data analysis"
            },
            {
                "name": "Hilary Mason",
                "title": "Data Science Leader",
                "expertise": ["machine learning", "data ethics", "exploratory analysis"],
                "background": "Bitly former Chief Scientist, Fast Forward Labs founder",
                "focus": "machine learning"
            }
        ],
        "test_design_philosophy": "Analytical rigor, insight quality, and statistical validity"
    },

    "data-docs": {
        "panel_name": "Document Processing Panel",
        "parent": "data",
        "experts": [
            {
                "name": "Benn Stancil",
                "title": "Data Analytics Expert",
                "expertise": ["document parsing", "data extraction", "format conversion"],
                "background": "Mode Analytics co-founder, Chief Analytics Officer",
                "focus": "document parsing"
            }
        ],
        "test_design_philosophy": "Parsing accuracy, data integrity, and format compatibility"
    },

    # Video Subcategories
    "video-editing": {
        "panel_name": "Video Editing Panel",
        "parent": "video",
        "experts": [
            {
                "name": "This Guy Edits",
                "title": "Video Editing Expert",
                "expertise": ["editing workflow", "storytelling", "pacing"],
                "background": "Professional video editor, educator",
                "focus": "editing workflow"
            }
        ],
        "test_design_philosophy": "Edit quality, story coherence, and technical execution"
    },

    "video-media": {
        "panel_name": "Media Handling Panel",
        "parent": "video",
        "experts": [
            {
                "name": "Peter McKinnon",
                "title": "Photography & Video Creator",
                "expertise": ["media download", "asset management", "workflow optimization"],
                "background": "Professional photographer and YouTuber",
                "focus": "media download"
            }
        ],
        "test_design_philosophy": "Download reliability, format support, and quality preservation"
    },

    # Sales Subcategories
    "sales-outreach": {
        "panel_name": "Sales Outreach Panel",
        "parent": "sales",
        "experts": [
            {
                "name": "Aaron Ross",
                "title": "Predictable Revenue Author",
                "expertise": ["cold email", "outbound sequences", "prospecting"],
                "background": "'Predictable Revenue' and 'Predictable Success' author",
                "focus": "cold email"
            },
            {
                "name": "Jill Konrath",
                "title": "Sales Strategy Expert",
                "expertise": ["sales messaging", "value propositions", "buyer engagement"],
                "background": "'Selling to Big Companies' and 'SNAP Selling' author",
                "focus": "sales messaging"
            }
        ],
        "test_design_philosophy": "Message relevance, personalization quality, and call-to-action effectiveness"
    },

    "sales-enablement": {
        "panel_name": "Sales Enablement Panel",
        "parent": "sales",
        "experts": [
            {
                "name": "Mark Roberge",
                "title": "Revenue Operations Expert",
                "expertise": ["sales enablement", "RevOps", "sales methodology"],
                "background": "Former HubSpot CRO, 'The Sales Acceleration Formula' author",
                "focus": "sales enablement"
            }
        ],
        "test_design_philosophy": "Enablement effectiveness, process optimization, and metric tracking"
    },

    # Business Subcategories
    "business-strategy": {
        "panel_name": "Business Strategy Panel",
        "parent": "business",
        "experts": [
            {
                "name": "Michael Porter",
                "title": "Competitive Strategy Authority",
                "expertise": ["competitive analysis", "strategic positioning", "value chains"],
                "background": "Harvard Business School Professor, 'Competitive Strategy' author",
                "focus": "competitive analysis"
            },
            {
                "name": "Reid Hoffman",
                "title": "Network Effects Expert",
                "expertise": ["platform strategy", "network effects", "scaling"],
                "background": "LinkedIn co-founder, Greylock Partners",
                "focus": "platform strategy"
            }
        ],
        "test_design_philosophy": "Strategic clarity, competitive insight, and execution feasibility"
    },

    "business-finance": {
        "panel_name": "Financial Strategy Panel",
        "parent": "business",
        "experts": [
            {
                "name": "Ben Horowitz",
                "title": "Tech Industry Investor",
                "expertise": ["financial planning", "unit economics", "fundraising"],
                "background": "Andreessen Horowitz co-founder, 'The Hard Thing About Hard Things' author",
                "focus": "financial planning"
            }
        ],
        "test_design_philosophy": "Financial rigor, unit economics clarity, and scenario planning"
    },

    # Compliance Subcategories
    "compliance-ra": {
        "panel_name": "Regulatory Affairs Panel",
        "parent": "compliance",
        "experts": [
            {
                "name": "Dr. Janet Woodcock",
                "title": "FDA Former Director",
                "expertise": ["FDA submissions", "drug approval", "regulatory strategy"],
                "background": "Former FDA CDER Director, 35+ years regulatory experience",
                "focus": "FDA submissions"
            },
            {
                "name": "Graham Law",
                "title": "Medical Device RA Expert",
                "expertise": ["MDR compliance", "CE marking", "technical documentation"],
                "background": "EU MDR specialist, 20+ years RA experience",
                "focus": "MDR compliance"
            }
        ],
        "test_design_philosophy": "Regulatory compliance accuracy, documentation completeness, and submission readiness"
    },

    "compliance-qm": {
        "panel_name": "Quality Management Panel",
        "parent": "compliance",
        "experts": [
            {
                "name": "Trevor Hughes",
                "title": "Privacy & Quality Expert",
                "expertise": ["QMS implementation", "ISO audits", "quality systems"],
                "background": "IAPP CEO, quality management specialist",
                "focus": "QMS implementation"
            },
            {
                "name": "Dr. Steven Guttman",
                "title": "Quality Systems Expert",
                "expertise": ["ISO 13485", "CAPA", "risk management"],
                "background": "Medical device quality consultant, 25+ years experience",
                "focus": "ISO 13485"
            }
        ],
        "test_design_philosophy": "QMS compliance, audit readiness, and continuous improvement"
    },

    "compliance-security": {
        "panel_name": "Security Compliance Panel",
        "parent": "compliance",
        "experts": [
            {
                "name": "Dr. Janet Woodcock",
                "title": "Regulatory Expert",
                "expertise": ["data privacy", "security compliance", "risk assessment"],
                "background": "Former FDA Director",
                "focus": "data privacy"
            }
        ],
        "test_design_philosophy": "Security control effectiveness, privacy compliance, and risk mitigation"
    },

    # Creative Subcategories
    "creative-visual": {
        "panel_name": "Visual Design Panel",
        "parent": "creative",
        "experts": [
            {
                "name": "Stefan Sagmeister",
                "title": "Design Legend",
                "expertise": ["visual design", "branding", "creative direction"],
                "background": "Sagmeister & Walsh co-founder, Grammy winner",
                "focus": "visual design"
            },
            {
                "name": "Jessica Hische",
                "title": "Lettering Artist",
                "expertise": ["typography", "lettering", "visual identity"],
                "background": "Renowned lettering artist and author",
                "focus": "typography"
            }
        ],
        "test_design_philosophy": "Visual impact, design coherence, and creative originality"
    },

    "creative-brainstorm": {
        "panel_name": "Creative Ideation Panel",
        "parent": "creative",
        "experts": [
            {
                "name": "Aaron Draplin",
                "title": "Logo Design Expert",
                "expertise": ["brainstorming", "ideation", "design thinking"],
                "background": "Draplin Design Co. founder, logo design authority",
                "focus": "brainstorming"
            }
        ],
        "test_design_philosophy": "Idea diversity, creative connections, and practical applicability"
    },

    # Other/Uncategorized
    "other": {
        "panel_name": "General Capabilities Panel",
        "parent": "other",
        "experts": [
            {
                "name": "General AI Assistant",
                "title": "Versatile Problem Solver",
                "expertise": ["general knowledge", "task completion", "adaptability"],
                "background": "Trained on diverse knowledge base",
                "focus": "general knowledge"
            }
        ],
        "test_design_philosophy": "Task completion effectiveness, response quality, and adaptability"
    }
}


def get_expert_panel(subcategory_key: str) -> Dict:
    """Get expert panel for a subcategory."""
    return EXPERT_PANELS.get(subcategory_key, EXPERT_PANELS["other"])


def get_expert_by_name(expert_name: str) -> Dict:
    """Find expert by name across all panels."""
    for panel_key, panel_data in EXPERT_PANELS.items():
        for expert in panel_data.get("experts", []):
            if expert["name"].lower() == expert_name.lower():
                return {**expert, "panel": panel_key}
    return None


def get_all_experts() -> list:
    """Get all experts across all panels."""
    all_experts = []
    for panel_key, panel_data in EXPERT_PANELS.items():
        for expert in panel_data.get("experts", []):
            all_experts.append({**expert, "panel": panel_key})
    return all_experts


def format_expert_panel_for_prompt(category: str) -> str:
    """Format expert panel as a prompt-ready string."""
    panel = get_expert_panel(category)

    output = [f"# {panel['panel_name']}"]
    output.append(f"Test Design Focus: {panel.get('test_design_philosophy', 'Domain-specific test coverage')}\n")

    for expert in panel["experts"]:
        output.append(f"## {expert['name']}")
        output.append(f"**{expert['title']}**")
        output.append(f"- Expertise: {', '.join(expert['expertise'])}")
        output.append(f"- Background: {expert['background']}")
        output.append("")

    return "\n".join(output)
