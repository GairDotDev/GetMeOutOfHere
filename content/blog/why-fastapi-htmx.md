---
title: "Why I chose FastAPI + HTMX for my portfolio"
date: 2025-10-15
summary: "Server-rendered pages, tiny JS, and fast iteration without the SPA tax."
tags: fastapi, htmx, python, portfolio
---

# Why FastAPI + HTMX

I wanted to ship a clean, fast, accessible portfolio. FastAPI gives me a great developer experience and performance. HTMX lets me sprinkle interactivity without a front-end framework.

## Priorities

- Keep HTML small and accessible.
- Avoid heavy client-side state.
- Reuse Python skills end-to-end.

## What worked well

- Jinja2 templates for clear, semantic markup.
- HTMX for small enhancements (filters, forms).
- Simple JSON storage with a path to SQLite/SQLModel.

## What’s next

Move to SQLite (SQLModel), add richer admin, and keep the UI pragmatic.

