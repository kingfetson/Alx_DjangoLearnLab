# Django Blog - CRUD Operations Documentation

## Overview
The Django Blog platform implements complete CRUD (Create, Read, Update, Delete) operations for blog posts using Django's class-based views. This provides a clean, efficient, and secure way to manage blog content.

## Features

### 1. List Posts (Read)
- **URL:** `/` or `/posts/`
- **View:** `PostListView`
- **Template:** `blog/home.html`
- **Access:** Public (no login required)
- **Features:**
  - Displays all posts in reverse chronological order
  - Shows post title, author, date, and excerpt
  - Includes search functionality
  - Pagination (10 posts per page)
  - Links to individual post pages
  - Edit/Delete buttons for post authors

### 2. View Single Post (Read)
- **URL:** `/post/<int:pk>/`
- **View:** `PostDetailView`
- **Template:** `blog/post_detail.html`
- **Access:** Public (no login required)
- **Features:**
  - Displays full post content
  - Shows author information and publication date
  - Indicates if post was edited
  - Edit/Delete buttons for post authors
  - Navigation back to home

### 3. Create Post
- **URL:** `/post/new/`
- **View:** `PostCreateView`
- **Template:** `blog/post_form.html`
- **Access:** Authenticated users only (`LoginRequiredMixin`)
- **Features:**
  - Form with title and content fields
  - Automatic author assignment (logged-in user)
  - Form validation:
    - Title minimum 5 characters
    - Content minimum 20 characters
  - Success message on creation
  - Redirect to post detail page

### 4. Update Post
- **URL:** `/post/<int:pk>/edit/`
- **View:** `PostUpdateView`
- **Template:** `blog/post_form.html`
- **Access:** Only post author (`UserPassesTestMixin`)
- **Features:**
  - Pre-filled form with existing post data
  - Same validation as creation
  - Success message on update
  - Redirect to post detail page
  - Author verification before allowing edit

### 5. Delete Post
- **URL:** `/post/<int:pk>/delete/`
- **View:** `PostDeleteView`
- **Template:** `blog/post_confirm_delete.html`
- **Access:** Only post author (`UserPassesTestMixin`)
- **Features:**
  - Confirmation page before deletion
  - Warning message about irreversibility
  - Post preview for verification
  - Success message after deletion
  - Redirect to home page

## Class-Based Views Implementation

### View Classes Used

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin