#!/usr/bin/env python3
"""
Expert Panel Definitions

Defines domain expert panels for each skill category.
Each panel consists of 3-5 experts who collaborate to design comprehensive test cases.
"""

# Expert Panel Definitions by Category
EXPERT_PANELS = {
    "cro": {
        "panel_name": "CRO Expert Panel",
        "description": "Conversion Rate Optimization specialists",
        "experts": [
            {
                "name": "Dr. Sarah Chen",
                "title": "Chief Conversion Officer",
                "expertise": ["landing page optimization", "funnel analysis", "A/B testing"],
                "background": "Former CRO lead at Optimizely, 15+ years experience",
                "focus": "Strategic oversight and test prioritization"
            },
            {
                "name": "Marcus Rodriguez",
                "title": "UX Research Director",
                "expertise": ["user behavior analysis", "heatmap interpretation", "session replay"],
                "background": "Led UX research at Hotjar, published author on conversion psychology",
                "focus": "User behavior insights and friction identification"
            },
            {
                "name": "Dr. Emily Watson",
                "title": "Behavioral Psychologist",
                "expertise": ["persuasion psychology", "decision science", "nudge theory"],
                "background": "PhD in Behavioral Economics, advisor to Fortune 500 companies",
                "focus": "Psychological triggers and motivation factors"
            },
            {
                "name": "James Park",
                "title": "Data Science Lead",
                "expertise": ["statistical analysis", "experiment design", "causal inference"],
                "background": "Former data scientist at Booking.com, experimentation platform builder",
                "focus": "Statistical rigor and measurement validity"
            }
        ]
    },
    "seo": {
        "panel_name": "SEO Expert Panel",
        "description": "Search Engine Optimization and visibility specialists",
        "experts": [
            {
                "name": "Dr. Michael Brenner",
                "title": "SEO Strategy Director",
                "expertise": ["technical SEO", "site architecture", "Core Web Vitals"],
                "background": "Former head of SEO at Moz, consultant for enterprise sites",
                "focus": "Technical audit and architecture review"
            },
            {
                "name": "Lisa Chang",
                "title": "Content SEO Lead",
                "expertise": ["keyword research", "content optimization", "search intent"],
                "background": "Built SEO content strategies for HubSpot and SEMrush",
                "focus": "On-page optimization and content strategy"
            },
            {
                "name": "Ahmed Hassan",
                "title": "AI Search Specialist",
                "expertise": ["LLM optimization", "AI Overview visibility", "structured data"],
                "background": "Pioneer in AI search optimization, early AEO adopter",
                "focus": "AI search and emerging search formats"
            },
            {
                "name": "Rachel Green",
                "title": "Link Building Expert",
                "expertise": ["digital PR", "link acquisition", "authority building"],
                "background": "Built link strategies for 500+ enterprise clients",
                "focus": "Off-page SEO and authority signals"
            }
        ]
    },
    "content": {
        "panel_name": "Content Expert Panel",
        "description": "Content strategy, copywriting, and communications specialists",
        "experts": [
            {
                "name": "Ann Handley",
                "title": "Chief Content Officer",
                "expertise": ["content strategy", "brand voice", "storytelling"],
                "background": "MarketingProfs founder, bestselling author on content marketing",
                "focus": "Strategic content direction and brand alignment"
            },
            {
                "name": "David Ogilvy Jr.",
                "title": "Copywriting Director",
                "expertise": ["direct response copy", "headline writing", "persuasion"],
                "background": "Former creative director at Ogilvy & Mather",
                "focus": "Copy quality and persuasive messaging"
            },
            {
                "name": "Sonia Simone",
                "title": "Content Marketing Lead",
                "expertise": ["email marketing", "content distribution", "audience building"],
                "background": "Copyblogger cofounder, email marketing expert",
                "focus": "Content distribution and audience engagement"
            }
        ]
    },
    "marketing": {
        "panel_name": "Marketing Expert Panel",
        "description": "Digital marketing, paid media, and analytics specialists",
        "experts": [
            {
                "name": "Neil Patel",
                "title": "Growth Marketing Advisor",
                "expertise": ["growth marketing", "SEO/SEM", "marketing analytics"],
                "background": "Cofounder of Neil Patel Digital, marketing thought leader",
                "focus": "Growth strategy and channel optimization"
            },
            {
                "name": "Rand Fishkin",
                "title": "Marketing Transparency Advocate",
                "expertise": ["marketing experimentation", "attribution", "transparent analytics"],
                "background": "SparkToro founder, former Moz CEO",
                "focus": "Marketing measurement and attribution"
            },
            {
                "name": "Avinash Kaushik",
                "title": "Digital Marketing Evangelist",
                "expertise": ["web analytics", "marketing metrics", "data-driven marketing"],
                "background": "Google Digital Marketing Evangelist, author of Web Analytics 2.0",
                "focus": "Analytics framework and measurement strategy"
            },
            {
                "name": "Mari Smith",
                "title": "Social Media Strategist",
                "expertise": ["social media marketing", "Facebook advertising", "influencer marketing"],
                "background": "Premier Facebook marketing expert, international speaker",
                "focus": "Social media and paid advertising"
            }
        ]
    },
    "growth": {
        "panel_name": "Growth Expert Panel",
        "description": "Growth hacking, viral mechanics, and retention specialists",
        "experts": [
            {
                "name": "Sean Ellis",
                "title": "Growth Hacking Pioneer",
                "expertise": ["growth hacking", "product-market fit", "viral mechanics"],
                "background": "Coined 'growth hacking', grew Dropbox, Eventbrite, LogMeIn",
                "focus": "Growth strategy and viral loops"
            },
            {
                "name": "Brian Balfour",
                "title": "Growth Education Leader",
                "expertise": ["growth frameworks", "retention strategy", "growth teams"],
                "background": "Former VP Growth at HubSpot, Reforge founder",
                "focus": "Growth systems and team building"
            },
            {
                "name": "Andrew Chen",
                "title": "Growth Investing Partner",
                "expertise": ["network effects", "marketplace dynamics", "growth metrics"],
                "background": "General Partner at a16z, author of The Cold Start Problem",
                "focus": "Network effects and marketplace growth"
            }
        ]
    },
    "sales": {
        "panel_name": "Sales Expert Panel",
        "description": "B2B sales, sales enablement, and revenue operations specialists",
        "experts": [
            {
                "name": "Aaron Ross",
                "title": "Predictable Revenue Expert",
                "expertise": ["cold outreach", "sales process", "SDR methodology"],
                "background": "Author of Predictable Revenue, built Salesforce's prospecting machine",
                "focus": "Outbound sales methodology"
            },
            {
                "name": "Jill Konrath",
                "title": "Sales Strategy Expert",
                "expertise": ["B2B selling", "buyer psychology", "sales acceleration"],
                "background": "Bestselling author, sales strategist for 20+ years",
                "focus": "Modern B2B sales tactics"
            },
            {
                "name": "Mark Roberge",
                "title": "Data-Driven Sales Leader",
                "expertise": ["sales analytics", "hiring sales teams", "sales enablement"],
                "background": "Former CRO at HubSpot, grew from $0 to $100M+",
                "focus": "Sales operations and enablement"
            }
        ]
    },
    "pricing": {
        "panel_name": "Pricing Expert Panel",
        "description": "Pricing strategy, packaging, and monetization specialists",
        "experts": [
            {
                "name": "Patrick Campbell",
                "title": "Pricing Strategy CEO",
                "expertise": ["SaaS pricing", "value-based pricing", "pricing analytics"],
                "background": "ProfitWell founder, pricing expert for 1000+ companies",
                "focus": "SaaS pricing strategy and analytics"
            },
            {
                "name": "Monica Eaton-Cardone",
                "title": "Monetization Strategist",
                "expertise": ["revenue optimization", "pricing psychology", "subscription models"],
                "background": "Chargeback Guru founder, payments and pricing expert",
                "focus": "Pricing psychology and model design"
            },
            {
                "name": "Dr. Hermann Simon",
                "title": "Pricing Authority",
                "expertise": ["pricing research", "value metrics", "price elasticity"],
                "background": "Simon-Kucher & Partners founder, authored 'Confessions of the Pricing Man'",
                "focus": "Pricing theory and value-based approaches"
            }
        ]
    },
    "engineering": {
        "panel_name": "Engineering Expert Panel",
        "description": "Software engineering, architecture, and code quality specialists",
        "experts": [
            {
                "name": "Martin Fowler",
                "title": "Software Architecture Authority",
                "expertise": ["software architecture", "refactoring", "design patterns"],
                "background": "Chief Scientist at ThoughtWorks, author of Refactoring",
                "focus": "Architecture review and design quality"
            },
            {
                "name": "Kent Beck",
                "title": "Agile Development Pioneer",
                "expertise": ["TDD", "extreme programming", "software craftsmanship"],
                "background": "Creator of JUnit, pioneer of Extreme Programming",
                "focus": "Testing practices and code quality"
            },
            {
                "name": "Jessica Kerr",
                "title": "Software Systems Thinker",
                "expertise": ["distributed systems", "observability", "team dynamics"],
                "background": "Developer advocate, author on observability and systems",
                "focus": "Systems thinking and observability"
            },
            {
                "name": "Will Larson",
                "title": "Engineering Leadership Expert",
                "expertise": ["engineering management", "technical strategy", "team scaling"],
                "background": "Former CTO at Carto, Calm, author of engineering leadership books",
                "focus": "Engineering leadership and team effectiveness"
            }
        ]
    },
    "product": {
        "panel_name": "Product Expert Panel",
        "description": "Product management, UX design, and user research specialists",
        "experts": [
            {
                "name": "Marty Cagan",
                "title": "Product Leadership Guru",
                "expertise": ["product discovery", "product strategy", "product teams"],
                "background": "Silicon Valley Product Group founder, former Netscape/EBay exec",
                "focus": "Product discovery and team structure"
            },
            {
                "name": "Teresa Torres",
                "title": "Product Discovery Coach",
                "expertise": ["continuous discovery", "user interviewing", "product experiments"],
                "background": "Product coach, author of Continuous Discovery Habits",
                "focus": "Discovery practices and user research"
            },
            {
                "name": "Don Norman",
                "title": "UX Design Legend",
                "expertise": ["user-centered design", "design thinking", "cognitive psychology"],
                "background": "Cofounder of NN/g, author of The Design of Everyday Things",
                "focus": "UX principles and usability"
            },
            {
                "name": "Lenny Rachitsky",
                "title": "Product Growth Advisor",
                "expertise": ["product-led growth", "feature optimization", "product analytics"],
                "background": "Former Airbnb PM, Lenny's Newsletter author",
                "focus": "Product-led growth and optimization"
            }
        ]
    },
    "devops": {
        "panel_name": "DevOps Expert Panel",
        "description": "DevOps, CI/CD, and infrastructure specialists",
        "experts": [
            {
                "name": "Kelsey Hightower",
                "title": "Cloud Native Pioneer",
                "expertise": ["Kubernetes", "cloud infrastructure", "developer experience"],
                "background": "Distinguished Engineer at Google, Kubernetes advocate",
                "focus": "Cloud native architecture and best practices"
            },
            {
                "name": "Jez Humble",
                "title": "DevOps Authority",
                "expertise": ["continuous delivery", "deployment pipelines", "lean practices"],
                "background": "Co-author of Continuous Delivery, DevOps Research lead",
                "focus": "CI/CD and deployment practices"
            },
            {
                "name": "Charity Majors",
                "title": "Observability Expert",
                "expertise": ["observability", "debugging", "infrastructure operations"],
                "background": "Honeycomb cofounder, engineering leader",
                "focus": "Observability and operations"
            }
        ]
    },
    "data": {
        "panel_name": "Data Expert Panel",
        "description": "Data engineering, analytics, and business intelligence specialists",
        "experts": [
            {
                "name": "DJ Patil",
                "title": "Data Science Pioneer",
                "expertise": ["data science", "analytics strategy", "data products"],
                "background": "First US Chief Data Scientist, LinkedIn data leader",
                "focus": "Data strategy and products"
            },
            {
                "name": "Hilary Mason",
                "title": "Data Science Leader",
                "expertise": ["machine learning", "data ethics", "analytics"],
                "background": "Former Chief Scientist at Bitly, Fast Forward Labs founder",
                "focus": "ML applications and data ethics"
            },
            {
                "name": "Benn Stancil",
                "title": "Analytics Thought Leader",
                "expertise": ["business intelligence", "data storytelling", "analytics tools"],
                "background": "Mode cofounder, analytics industry commentator",
                "focus": "BI and data communication"
            }
        ]
    },
    "video": {
        "panel_name": "Video Production Expert Panel",
        "description": "Video production, editing, and content creation specialists",
        "experts": [
            {
                "name": "Casey Faris",
                "title": "Video Education Creator",
                "expertise": ["DaVinci Resolve", "color grading", "video editing"],
                "background": "Popular YouTube educator for video production",
                "focus": "Editing workflow and color"
            },
            {
                "name": "Peter McKinnon",
                "title": "Content Creation Expert",
                "expertise": ["cinematography", "content creation", "visual storytelling"],
                "background": "Professional photographer and filmmaker",
                "focus": "Visual storytelling and production"
            },
            {
                "name": "This Guy Edits",
                "title": "Documentary Editor",
                "expertise": ["documentary editing", "story structure", "pacing"],
                "background": "Professional documentary film editor",
                "focus": "Editing craft and narrative"
            }
        ]
    },
    "agent": {
        "panel_name": "AI Agent Expert Panel",
        "description": "AI agents, context engineering, and tool design specialists",
        "experts": [
            {
                "name": "Andrew Ng",
                "title": "AI Education Leader",
                "expertise": ["machine learning", "AI strategy", "agent systems"],
                "background": "Cofounder of Coursera, former Baidu/Google AI leader",
                "focus": "AI strategy and system design"
            },
            {
                "name": "Ethan Mollick",
                "title": "AI in Practice Expert",
                "expertise": ["AI productivity", "human-AI collaboration", "prompt engineering"],
                "background": "Wharton professor, author on AI in business",
                "focus": "Practical AI applications"
            },
            {
                "name": "Simon Willison",
                "title": "LLM Tools Builder",
                "expertise": ["LLM tooling", "prompt engineering", "AI security"],
                "background": "Datasette creator, LLM writing expert",
                "focus": "LLM tools and best practices"
            },
            {
                "name": "Riley Goodside",
                "title": "Prompt Engineering Pioneer",
                "expertise": ["prompt engineering", "LLM capabilities", "AI interaction"],
                "background": "First 'Prompt Engineer' at Scale AI",
                "focus": "Prompt design and LLM interaction"
            }
        ]
    },
    "creative": {
        "panel_name": "Creative Design Expert Panel",
        "description": "Creative design, visual arts, and brand specialists",
        "experts": [
            {
                "name": "Stefan Sagmeister",
                "title": "Design Legend",
                "expertise": ["brand identity", "visual design", "creative direction"],
                "background": "Sagmeister & Walsh cofounder, Grammy-winning designer",
                "focus": "Creative direction and brand design"
            },
            {
                "name": "Jessica Hische",
                "title": "Lettering Artist",
                "expertise": ["typography", "lettering", "brand design"],
                "background": "Internationally acclaimed lettering artist and author",
                "focus": "Typography and visual craft"
            },
            {
                "name": "Aaron Draplin",
                "title": "Design Pragmatist",
                "expertise": ["logo design", "brand systems", "design business"],
                "background": "Draplin Design Co. founder, Field Notes cofounder",
                "focus": "Practical design and brand systems"
            }
        ]
    },
    "business": {
        "panel_name": "Business Strategy Expert Panel",
        "description": "Business strategy, finance, and operations specialists",
        "experts": [
            {
                "name": "Michael Porter",
                "title": "Strategy Authority",
                "expertise": ["competitive strategy", "industry analysis", "strategic positioning"],
                "background": "Harvard Business School professor, strategy thought leader",
                "focus": "Strategic framework and positioning"
            },
            {
                "name": "Reid Hoffman",
                "title": "Scaling Expert",
                "expertise": ["scaling strategy", "network effects", "business models"],
                "background": "LinkedIn cofounder, Greylock partner",
                "focus": "Scaling and network-based strategy"
            },
            {
                "name": "Ben Horowitz",
                "title": "CEO Advisor",
                "expertise": ["CEO leadership", "company building", "crisis management"],
                "background": "a16z cofounder, author of The Hard Thing About Hard Things",
                "focus": "Leadership and organizational challenges"
            }
        ]
    },
    "compliance": {
        "panel_name": "Compliance Expert Panel",
        "description": "Regulatory compliance, quality management, and risk specialists",
        "experts": [
            {
                "name": "Dr. Janet Woodcock",
                "title": "FDA Regulatory Expert",
                "expertise": ["FDA compliance", "drug approval", "regulatory strategy"],
                "background": "Former FDA CDER Director, 40+ years regulatory experience",
                "focus": "FDA regulatory framework"
            },
            {
                "name": "Graham Law",
                "title": "ISO Standards Expert",
                "expertise": ["ISO 13485", "ISO 27001", "quality management systems"],
                "background": "Lead auditor for multiple ISO standards",
                "focus": "ISO compliance and QMS"
            },
            {
                "name": "J. Trevor Hughes",
                "title": "Privacy Leadership",
                "expertise": ["GDPR", "data privacy", "privacy compliance"],
                "background": "IAPP CEO, privacy industry leader",
                "focus": "Privacy regulations and compliance"
            },
            {
                "name": "Dr. Steven Guttman",
                "title": "Risk Management Expert",
                "expertise": ["enterprise risk", "risk assessment", "compliance programs"],
                "background": "Former federal regulator, compliance consultant",
                "focus": "Risk management frameworks"
            }
        ]
    },
    "other": {
        "panel_name": "General Assessment Panel",
        "description": "Cross-domain experts for uncategorized skills",
        "experts": [
            {
                "name": "Dr. Barbara Minto",
                "title": "Communication Expert",
                "expertise": ["structured thinking", "communication", "problem solving"],
                "background": "McKinsey consultant, Pyramid Principle creator",
                "focus": "Structured analysis and communication"
            },
            {
                "name": "Charlie Munger",
                "title": "Mental Models Master",
                "expertise": ["decision making", "mental models", "multidisciplinary thinking"],
                "background": "Berkshire Hathaway Vice Chairman, polymath investor",
                "focus": "Multidisciplinary analysis"
            },
            {
                "name": "Dr. Daniel Kahneman",
                "title": "Behavioral Science Legend",
                "expertise": ["judgment", "decision science", "cognitive bias"],
                "background": "Nobel laureate, Thinking Fast and Slow author",
                "focus": "Cognitive factors in skill evaluation"
            }
        ]
    }
}


def get_expert_panel(category: str) -> dict:
    """Get expert panel for a category."""
    return EXPERT_PANELS.get(category, EXPERT_PANELS["other"])


def get_all_panels() -> dict:
    """Get all expert panels."""
    return EXPERT_PANELS


def format_expert_panel_for_prompt(category: str) -> str:
    """Format expert panel as a prompt-ready string."""
    panel = get_expert_panel(category)

    output = [f"# {panel['panel_name']}"]
    output.append(f"*{panel['description']}*\n")

    for expert in panel["experts"]:
        output.append(f"## {expert['name']}")
        output.append(f"**{expert['title']}**")
        output.append(f"- Expertise: {', '.join(expert['expertise'])}")
        output.append(f"- Background: {expert['background']}")
        output.append(f"- Focus: {expert['focus']}")
        output.append("")

    return "\n".join(output)
