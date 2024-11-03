# Construction Project Quotation Web Application

## Overview

This web application helps a construction company manage project quotations and plans for customers. It replaces the previous method of using Google Sheets with a more efficient Django-based solution, featuring a clean UI with Bootstrap.

## Features

### User Functionality

- **Registration and Login**: Users can create accounts and log in.
- **Project Quotations**: Users can create and view their project quotations, each showing:
  - Project ID
  - Description
  - Location
  - Status (Pending, Approved, Declined, Completed)
- **Project Details**: Users can view detailed information about their projects, including elements and materials with costs.

### Admin Functionality

- **Admin Dashboard**: Admins can view all projects and manage their statuses:
  - Update project details
  - Approve or decline projects
  - Add or remove project elements and materials
- **Real-Time Updates**: Changes to materials and costs update instantly on the admin side.
