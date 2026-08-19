# Fun fastapi rss reader project(learning only,not prod ready in any way)

## goal:
i mainly used this for fun and learning fullstack webdevelopment,the only complete parts of it are the database and rss ingestion

i learnt:
  - database handling
  - vite+jinja+tailwindcss+some small js
  - fastapi basics

## what would i do differently?
  - nowdays for my webapps i usually stick to fastapi and jinja,with no bundler like vite at all to reduce complexity
    - it caused me to need to add CORS so fastapi reloads aswell for HMR

## Run:
  `cd backend && uvicorn main:app --reload`
  and in another terminal:
  `cd frontend && npm run dev`
it'll then be available on localhost:8000
