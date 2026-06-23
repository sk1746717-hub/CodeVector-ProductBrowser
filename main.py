from sqlalchemy import and_, or_
from datetime import datetime
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import engine, get_db
from models import Product

app = FastAPI()


@app.get("/")
def home():
    return {"message": "CodeVector Product Browser API"}


@app.get("/test-db")
def test_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        return {"database": "connected"}


@app.get("/products")
def get_products(
    limit: int = Query(default=20, le=100),
    category: str | None = None,
    cursor_created_at: str | None = None,
    cursor_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    if cursor_created_at and cursor_id:

        cursor_dt = datetime.fromisoformat(
    cursor_created_at.strip().replace('"', '')
)

        query = query.filter(
            or_(
                Product.created_at < cursor_dt,
                and_(
                    Product.created_at == cursor_dt,
                    Product.id < cursor_id
                )
            )
        )

    products = (
        query
        .order_by(
            Product.created_at.desc(),
            Product.id.desc()
        )
        .limit(limit)
        .all()
    )

    next_cursor = None

    if products:
        last = products[-1]

        next_cursor = {
            "cursor_created_at": last.created_at.isoformat(),
            "cursor_id": last.id
        }

    return {
        "items": products,
        "next_cursor": next_cursor
    }