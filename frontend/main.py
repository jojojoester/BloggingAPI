import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Blogging App", page_icon="📝", layout="wide")

# Initialize session state
if "posts" not in st.session_state:
    st.session_state.posts = []  # list of posts

st.title("📝 Blogging News Feed")

# ------------------ CREATE NEW POST ------------------
st.subheader("➕ Create a New Post")

author = st.text_input("Your Name")
title = st.text_input("Post Title")
content = st.text_area("Write your blog post here...")

if st.button("Publish Post"):
    if title and content and author:
        new_post = {
            "author": author,
            "title": title,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        st.session_state.posts.insert(0, new_post)  # add at top
        st.success("✅ Post published successfully!")
    else:
        st.warning("Please fill in all fields before publishing.")

st.divider()

# ------------------ DISPLAY POSTS ------------------
st.subheader("📌 Blog Feed")

if st.session_state.posts:
    for i, post in enumerate(st.session_state.posts):
        with st.container():
            st.markdown(f"### {post['title']}")
            st.write(post["content"])
            st.caption()
