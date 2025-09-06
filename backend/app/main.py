from fastapi import FastAPI
from routers import users
# FastAPI app
app = FastAPI(
    title="Blogging API",
    description="Blogging API that lets users register, login, add blog posts, edit blog posts, delete blog posts, and comment on others' posts."
)

app.include_router(users.router)
