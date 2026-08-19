from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from sqlalchemy import select, or_, desc
from sqlalchemy.orm import Session, joinedload
from typing import Dict, Annotated, Any, List
from fastapi.templating import Jinja2Templates
from database_handling import engine, get_db
from models import Feeds, Base, Entry
from schema import NewFeed
import feedparser
from datetime import datetime
from dateutil import parser as date_parser


app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/public/"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="../frontend/templates")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)


@app.get("/test")
def test():
    return {"status": "ok"}


@app.get("/", name="index", response_class=HTMLResponse)
async def page(request: Request, db: Session = Depends(get_db)):
    excluded = {
        "index",
        "test",
        "static",
        "favicon",
        "openapi",
        "swagger_ui_html",
        "swagger_ui_redirect",
        "redoc_html",
        None,
    }
    pages = [
        {"name": route.name}
        for route in app.routes
        if hasattr(route, "name")
        and hasattr(route, "methods")
        and "GET" in route.methods
        and route.name not in excluded
        and "{" not in route.path
        and route.path.count("/") == 1
    ]
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "pages": pages, "top_articles": get_top_articles(db)},
    )


def get_top_articles(db: Session, limit: int = 5) -> List[Entry]:
    feeds = db.query(Entry).order_by(desc(Entry.published)).limit(limit).all()
    return feeds


@app.get("/rss", name="rss", response_class=HTMLResponse)
def see_rss(request: Request, db: Session = Depends(get_db)):
    update_stored_feeds(db)
    fetched_feeds = (
        db.query(Feeds)
        .filter(Feeds.success == True)
        .options(joinedload(Feeds.entries))
        .all()
    )
    return templates.TemplateResponse(
        "rss.html",
        {
            "request": request,
            "feeds": fetched_feeds,
            "top_articles": get_top_articles(db),
        },
    )


@app.post("/rss/add_rss", name="add_rss", response_class=HTMLResponse)
def add_rss(
    new_feed: Annotated[NewFeed, Form()],
    request: Request,
    db: Session = Depends(get_db),
):
    new_feed = Feeds(link=new_feed.link, title=new_feed.name)
    db.add(new_feed)
    try:
        db.commit()
        db.refresh()
    except Exception as e:
        print(e)
    return RedirectResponse(url="/rss", status_code=303)


@app.get("/idfk", name="idfk", response_class=HTMLResponse)
def rando_page(request: Request):
    return templates.TemplateResponse(
        "idfk.html",
        {
            "request": request,
        },
    )


def update_stored_feeds(db: Session):
    unfetched_feeds = db.query(Feeds).where(Feeds.success.isnot(True))
    for i in unfetched_feeds:
        feed_data = fetch_feed(i.link)
        i.title = feed_data.get("title", "Unknown Title")
        i.description = feed_data.get("description", "No description available")
        i.success = feed_data.get("success", False)
        for e in feed_data["entries"]:
            published = None
            if e.get("published"):
                try:
                    published = date_parser.parse(e["published"])
                except (ValueError, TypeError):
                    published = datetime.now()
            new_entry = Entry(
                title=e["title"],
                author=e["author"],
                summary=e["summary"],
                published=published,
                link=e["link"],
            )
            db.add(new_entry)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"db commit errr : {e}")


def fetch_feed(feed_url: str, max_entries: int = 10) -> Dict[str, Any]:
    try:
        feed = feedparser.parse(feed_url)
        entries = []
        for entry in feed.entries[:max_entries]:
            entries.append(
                {
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", "#"),
                    "summary": entry.get("summary", "No summary available"),
                    "published": entry.get("published", "No date"),
                    "author": entry.get("author", "Unknown"),
                }
            )
        if not entries and (feed.get("bozo") or not feed.feed):
            return {
                "entries": [],
                "success": False,
                "error": str("malformed input data"),
            }
        return {
            "title": feed.feed.get("title", "Unknown Feed"),
            "description": feed.feed.get("description", ""),
            "link": feed.feed.get("link", "#"),
            "entries": entries,
            "success": True,
            "error": None,
        }
    except Exception as e:
        return {"entries": [], "success": False, "error": str(e)}
