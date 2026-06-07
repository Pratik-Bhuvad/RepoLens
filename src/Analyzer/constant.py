"""
content/constants.py
"""

README_WEIGHTS = {
    "has_purpose": 0.35,
    "has_installation": 0.30,
    "has_features": 0.25,
    "is_live_deployed": 0.10,
}

TREE_WEIGHTS = {
    "has_src": 0.25,
    "has_tests": 0.20,
    "has_docs": 0.15,
    "has_config": 0.15,
    "has_ci": 0.15,
    "depth": 0.10,
}


PURPOSE_PATTERNS = [
    "this project",
    "this application",
    "this app",
    "this platform",
    "this system",
    "allows users",
    "enables users",
    "built to",
    "designed to",
    "created to",
]

INSTALLATION_PATTERNS = [
    "installation",
    "setup",
    "getting started",
    "quick start",
    "run locally",
    "git clone",
    "npm install",
    "yarn install",
    "pnpm install",
    "pip install",
    "docker compose",
]

FEATURE_PATTERNS = [
    "features",
    "key features",
    "capabilities",
    "functionality",
]

LIVE_PATTERNS = [
    "live demo",
    "demo",
    "deployed",
    "production",
]

DEPLOYED_DOMAINS = [
    "vercel.app",
    "netlify.app",
    "render.com",
    "railway.app",
    "herokuapp.com",
]