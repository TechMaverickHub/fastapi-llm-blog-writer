# Blog Platform with LLM and Supabase

A developer-focused blog platform with **FastAPI**, **Groq LLM**, and
**Supabase**.\
Users can log in, create, read, update, and delete blogs, and get
**AI-powered topic suggestions** before writing.

------------------------------------------------------------------------

## Features 🚀

-   **JWT Authentication** (secure login/logout)\
-   **Blog CRUD** (create, read, update, delete blogs)\
-   **LLM Topic Suggestions** via **Groq LLM**\
-   **Supabase Database** for user and blog storage\
-   **React + TypeScript Frontend** (planned)\
-   Optional **Scraping Integration** for trending topics & metadata
    (future roadmap)

------------------------------------------------------------------------

## API Endpoints

### Auth

-   `POST /auth/register` → register a new user\
-   `POST /auth/login` → login, returns JWT\
-   `POST /auth/logout` → logout user

### Blogs

-   `POST /blogs` → create blog\
-   `GET /blogs` → list blogs\
-   `PUT /blogs/{id}` → edit blog\
-   `DELETE /blogs/{id}` → delete blog

### LLM Suggestions

-   `POST /suggest_topics`\
    **Input:**

    ``` json
    { "keywords": ["python", "fastapi", "router"] }
    ```

    **Output:**

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

### Future Scraping APIs

-   `/scrape/articles` → fetch article summaries\
-   `/scrape/metadata` → link preview metadata\
-   `/scrape/tags` → SEO tags for drafts\
-   `/scrape/trending` → trending topics

------------------------------------------------------------------------

## Tech Stack 🛠️

-   **Backend**: FastAPI, Groq LLM, Supabase\
-   **Auth**: JWT tokens\
-   **Frontend**: React + TypeScript (planned)\
-   **Deployment**: FastAPI backend + Vercel/Netlify frontend

------------------------------------------------------------------------

## Roadmap 📌

-   [x] JWT authentication\
-   [x] CRUD blog API\
-   [x] LLM-powered topic suggestion\
-   [ ] Supabase integration\
-   [ ] Frontend (React + TypeScript)\
-   [ ] Optional scraping APIs

------------------------------------------------------------------------

## Getting Started

### Backend

``` bash
# Clone repo
git clone https://github.com/yourusername/blog-llm-api.git
cd blog-llm-api

# Install deps
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

### Frontend (Planned)

``` bash
cd frontend
npm install
npm run dev
```

------------------------------------------------------------------------

## License

MIT License © 2025 Your Name
