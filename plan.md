# Blog Platform with LLM and Scraping Integration - Product Requirements Document (PRD)

## Overview

A blog platform where users can log in, create, read, update, and delete
blogs.\
Enhanced with LLM-powered keyword-based topic suggestions and optional
scraping features for content inspiration and metadata enrichment.\
Backend built with **FastAPI**, **Groq LLM**, and **Supabase** as the
database.\
Authentication handled via **JWT**.

------------------------------------------------------------------------

## Core Features

### 1. Authentication (JWT)

-   **Login**: Username & password, returns JWT access token.\
-   **Register**: User creation (if backend supports).\
-   **Logout**: Clears JWT from local storage.\
-   **Token Validation**: Middleware to protect API routes.

------------------------------------------------------------------------

### 2. Blog CRUD

-   **Create Blog**
    -   Endpoint: `POST /blogs`\
    -   Inputs: title, content\
    -   Optional: prefill from suggested topics\
-   **List Blogs**
    -   Endpoint: `GET /blogs`\
    -   Returns all blogs for user\
-   **Edit Blog**
    -   Endpoint: `PUT /blogs/{id}`\
    -   Update title & content\
-   **Delete Blog**
    -   Endpoint: `DELETE /blogs/{id}`

------------------------------------------------------------------------

### 3. LLM-Assisted Topic Suggestions

-   **Endpoint**: `POST /suggest_topics`\

-   **Input**: List of keywords (strings)\

-   **Process**: Groq LLM generates 3 topics, each with 3 points,
    incorporating keywords\

-   **Output (JSON)**:

    ``` json
    [
      {
        "topic": "Topic 1",
        "points": ["Point 1", "Point 2", "Point 3"]
      },
      {
        "topic": "Topic 2",
        "points": ["Point 1", "Point 2", "Point 3"]
      },
      {
        "topic": "Topic 3",
        "points": ["Point 1", "Point 2", "Point 3"]
      }
    ]
    ```

-   **Frontend**: Suggestions shown in cards, option to "use this
    suggestion" → prefill blog creation form.

------------------------------------------------------------------------

### 4. Database (Supabase)

-   **Users Table**: user_id, username, password_hash, created_at\
-   **Blogs Table**: blog_id, user_id (FK), title, content, created_at,
    updated_at\
-   **Relations**: one user → many blogs

------------------------------------------------------------------------

### 5. Optional Scraping Features

-   **/scrape/articles** → Get article summaries based on keywords\
-   **/scrape/metadata** → Fetch link preview (title, description,
    image)\
-   **/scrape/tags** → Suggest SEO-friendly tags for blog drafts\
-   **/scrape/trending** → Fetch trending blog topics

------------------------------------------------------------------------

## Frontend Features

-   Built with React + TypeScript + Vite\
-   **Pages**:
    -   `/login` → login form\
    -   `/blogs` → list of blogs\
    -   `/blogs/create` → form with optional LLM prefill\
    -   `/blogs/:id/edit` → edit existing blog\
    -   `/blogs/suggest` → keyword input + topic suggestions
-   **Token Handling**: JWT stored in localStorage, added to axios
    headers.\
-   **UI**: Minimal, developer-focused, plain textarea inputs (Tailwind
    optional).

------------------------------------------------------------------------

## Deliverables Checklist

-   [ ] JWT authentication implemented\
-   [ ] Supabase integrated as database\
-   [ ] CRUD blog endpoints live\
-   [ ] LLM topic suggestion endpoint live\
-   [ ] Optional scraping endpoints (articles, metadata, tags,
    trending)\
-   [ ] React frontend with login, blog list, create/edit, suggest
    pages\
-   [ ] Deployment via Vercel/Netlify (frontend) + FastAPI backend
