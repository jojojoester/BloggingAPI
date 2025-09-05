from fastapi import FastAPI


# FastAPI app
app = FastAPI(
    title="Blogging API",
    description="Blogging API that lets users register, login, add blog posts, edit blog posts, delete blog posts, and comment on others' posts."
)
