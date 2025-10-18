# Portfolio Upgrade - Key Changes

## 📄 main.py

```diff
+ """
+ Tom Gair Portfolio - FastAPI Backend
+ A clean, professional portfolio site with admin functionality.
+ Built with FastAPI, Jinja2, HTMX, and Tailwind CSS.
+ """

- from fastapi import FastAPI, Request, Form, HTTPException, Header, Cookie, Response
+ from fastapi import FastAPI, Request, Form, HTTPException, Header, Cookie

- import hashlib
- from datetime import timedelta

- app = FastAPI(title="Tom Gair — Backend-Focused Developer (Python/FastAPI)")
+ app = FastAPI(title="Tom Gair — Python/FastAPI Developer")
```

**Result:** Cleaner imports, added docstring, simplified title

---

## 🏠 templates/home.html

### Hero Section
```diff
- <h1>Tom Gair - Backend Developer</h1>
- <p>I build pragmatic Python/FastAPI backends and ship end-to-end features fast.</p>

+ <div class="badge">Open to Employment, Freelance, and Collaboration</div>
+ <h1>I build reliable software<br/>and simple systems.</h1>
+ <p>FastAPI, Python, and AI-assisted tools for clean, practical development.</p>
```

### New About Section
```diff
+ <section class="py-20 bg-white dark:bg-gray-800">
+   <h2>About Me</h2>
+   <p>I'm Tom Gair — a self-taught Python developer who builds small, 
+      practical tools and automation systems.</p>
+   <p>I focus on FastAPI backends, data handling, and 
+      ethical, privacy-aware design.</p>
+   
+   <h3>Skills & Technologies</h3>
+   <!-- Skill Cards -->
+   - Python
+   - FastAPI
+   - SQLite
+   - HTMX/Jinja
+   - Docker
+   - GitHub
+   - AI-assisted Dev
+ </section>
```

### Removed Old Sections
```diff
- <!-- Tech Stack Section with 4 detailed cards -->
- <!-- Recent Work Preview with placeholder projects -->
- <!-- Call to Action section -->

+ <!-- Simple Featured Projects link -->
```

---

## 📁 templates/projects.html

```diff
- <div class="space-y-8">
-   <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
-     <h1>Projects</h1>

+ <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
+   <div class="text-center mb-12">
+     <h1 class="text-4xl">Projects</h1>
+     <p>A collection of tools and systems built with clean code...</p>
+   </div>
+   
+   <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-8">
```

**Tag Filters:**
```diff
- <button class="px-3 py-1 rounded border text-sm">
+ <button class="px-4 py-2 rounded-lg text-sm font-medium 
+               bg-neon-600 text-white hover-scale">
```

**Projects Grid:**
```diff
- <div id="projects-list" class="space-y-4">
+ <div id="projects-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

---

## 🎨 templates/project_item.html

**Complete redesign:**
```diff
- <div class="border border-gray-200 rounded-lg p-4">
-   <h3><a href="/projects/{{slug}}">{{title}}</a></h3>
-   <p>{{summary}}</p>
-   <div>Tags...</div>
-   <a>Case Study →</a>
- </div>

+ <div class="hover-lift bg-white dark:bg-gray-700 rounded-xl 
+            overflow-hidden shadow-lg border">
+   <div class="p-6">
+     <h3 class="text-xl font-semibold">{{title}}</h3>
+     <p class="text-gray-600 leading-relaxed">{{summary}}</p>
+     
+     <!-- Stack badges -->
+     <div class="flex flex-wrap gap-2">
+       <span class="px-3 py-1 bg-gray-100 rounded-lg">FastAPI</span>
+     </div>
+     
+     <!-- Links -->
+     <div class="flex gap-3 pt-4 border-t">
+       <a href="{{site}}">Visit Site →</a>
+       <a href="{{repo}}">GitHub</a>
+     </div>
+   </div>
+ </div>
```

---

## 💌 templates/contact.html

```diff
- <section class="max-w-3xl mx-auto bg-white rounded-lg shadow-sm p-8">
-   <h1>Contact</h1>
-   <p>Have a project in mind or want to connect?</p>

+ <div class="max-w-7xl mx-auto px-4 py-12">
+   <div class="text-center mb-12">
+     <h1 class="text-4xl">Get In Touch</h1>
+     <p>Open to employment, freelance work, and collaboration opportunities.</p>
+   </div>
+   
+   <section class="max-w-3xl mx-auto bg-white rounded-xl shadow-sm p-8">
+     <h2>Send a Message</h2>
```

**Direct Contact:**
```diff
- <h2>Prefer direct contact?</h2>
- <a href="mailto:tom@gair.dev">tom@gair.dev</a>
- <a href="https://github.com/GairDotDev">GitHub</a>

+ <h3>Prefer direct contact?</h3>
+ <div class="flex flex-col sm:flex-row gap-4">
+   <a href="mailto:tom@gair.dev" 
+      class="px-6 py-3 rounded-lg bg-gray-100 font-medium">
+     tom@gair.dev
+   </a>
+   <a href="https://github.com/GairDotDev"
+      class="px-6 py-3 rounded-lg bg-gray-100 font-medium">
+     GitHub
+   </a>
+ </div>
```

---

## 🦶 templates/base.html (Footer)

```diff
  <footer>
    <div class="text-center">
-     <div class="text-2xl font-bold gradient-text mb-4">
-       Tom Gair
-     </div>
      <div class="flex justify-center space-x-6 mb-6">
        <!-- Social icons -->
      </div>
      <div class="text-gray-500 text-sm">
-       <p>&copy; 2025 Tom Gair — Backend-Focused Developer</p>
-       <p class="mt-2">No tracking. Simple visit count only.</p>
+       <p>&copy; 2025 Tom Gair.</p>
+       <p>Built with FastAPI, Jinja2, and AI-assisted design.</p>
      </div>
    </div>
  </footer>
```

---

## 📊 data/projects.json

**New Projects:**
```json
[
  {
    "id": 1,
    "slug": "runelight",
    "title": "Runelight",
    "summary": "Local-first camera stack for privacy-focused image capture and processing.",
    "tags": ["python", "opencv", "privacy", "local-first"],
    "stack": ["Python", "OpenCV", "Local Storage"]
  },
  {
    "id": 2,
    "slug": "normal-is-an-illusion",
    "title": "Normal Is An Illusion",
    "summary": "Emotional journaling platform with privacy-aware design (alpha).",
    "tags": ["fastapi", "docker", "journaling", "alpha"],
    "stack": ["FastAPI", "Docker", "HTMX", "SQLite"],
    "links": { "site": "https://normalisanillusion.com" }
  },
  {
    "id": 3,
    "slug": "jobscraper",
    "title": "JobScraper",
    "summary": "Job automation and data cleaner for efficient job search workflows.",
    "tags": ["python", "automation", "data-processing", "scheduler"],
    "stack": ["Python", "FastAPI", "Scheduler", "CSV/JSON"]
  }
]
```

---

## 🎨 Design Improvements

### Color Palette
- **Base:** White/gray neutral backgrounds
- **Primary:** Soft blue accents (#0ea5e9)
- **Accent:** Neon green for CTAs (#84cc16)
- **Dark Mode:** Full support with proper contrasts

### Typography
- **Headings:** Bold, clear hierarchy
- **Body:** Relaxed line-height (1.75)
- **Buttons:** Medium font-weight, proper padding

### Spacing
- **Sections:** 80px (py-20) vertical spacing
- **Cards:** 24px (p-6) internal padding
- **Grid gaps:** 24px (gap-6) between items

### Animations
- **Hover lift:** translateY(-8px) on cards
- **Hover scale:** scale(1.05) on buttons
- **Icon bounce:** translateX(4px) on arrows
- **Transitions:** 0.2-0.3s ease timing

---

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## ✅ Verification

- ✅ No Python syntax errors
- ✅ No linter errors
- ✅ All templates valid
- ✅ JSON properly formatted
- ✅ Static assets linked
- ✅ Dark mode functional
- ✅ Responsive design implemented
- ✅ SEO elements preserved (robots.txt, sitemap)

---

## 📝 Summary

**Files Modified:** 7
**Lines Changed:** ~300+
**New Projects:** 3
**Design Updates:** Complete refresh
**Time to Review:** 15 minutes
**Time to Deploy:** 5 minutes

**Overall Impact:** 
Portfolio transformed from basic project list to professional, hire-ready site with clear positioning, modern design, and excellent user experience.


