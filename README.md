# 🎵 Music Streaming App - MAD1 Project

![Project Banner](https://img.shields.io/badge/Project-MusicStreamingApp-blueviolet?style=for-the-badge)  
*A Flask-based Multi-User Music Streaming and Management Platform*

---

## 👨‍💻 Author:

**Kisalay Pan**  
Roll No: 22f2001094  
📧 Email: [22f2001094@ds.study.iitm.ac.in](mailto:22f2001094@ds.study.iitm.ac.in)

---

## 📌 Project Description:

This project is a **multi-user Music Streaming Web Application** built using **Flask**. It offers users the ability to **stream music**, **rate songs**, **create playlists**, and for **creators** to **upload new albums and songs**. Additionally, **admins** can monitor platform statistics, flag content violating policies, and manage user privileges like blacklisting creators.

---

## 🎯 Key Features:

- 🔑 **Role-based Login System:**
  - **Users**: Play, rate, and create playlists.
  - **Creators**: Upload and manage songs & albums.
  - **Admins**: Manage users, content flags, app statistics, and blacklists.

- 🎶 **Song Management:**
  - View, play, read lyrics, and rate songs.

- 📂 **Playlist Management:**
  - Users and Creators can create and manage personal playlists.

- 🎤 **Content Creation (Creators):**
  - Add, edit, or delete albums and songs.

- 🔍 **Search Functionality:**
  - Search songs or albums by **Name**, **Artist**, or **Genre**.

- 📊 **Admin Dashboard:**
  - View statistics like total users, creators, albums, and ratings.
  - Flag/unflag songs or albums.
  - Blacklist/whitelist creators.

---

## 🛠️ Technology Stack:

| Component           | Technology                      |
|-------------------- |-------------------------------- |
| **Backend**         | Flask, Flask_SQLAlchemy, Flask_Login |
| **Templating**      | Jinja2 |
| **Database**        | SQLite |
| **Alerts/Flash**    | Flask-Flash |
| **Authentication**  | Flask_Login |
| **Architecture**    | MVC (Model-View-Controller) |

---

## 🗃️ Database Schema Overview:

- **User Class:** Basic user details and playlists.
- **Admin Class:** Admin login details.
- **Creator Class:** Creators with ability to upload content.
- **Album Class:** Albums linked to multiple songs.
- **Song Class:** Song details with lyrics, ratings, and flags.
- **Playlist Class:** User/Creator playlists with many songs.
- **Rating Class:** User ratings for songs.
- **Blacklist Class:** Blacklisted user/creator data.

---

## 🧱 Project Architecture:

| Folder            | Description                                      |
|------------------ |------------------------------------------------ |
| **static/**       | Images and uploaded song files |
| **templates/**    | HTML files using Jinja2 templating |
| **instance/**     | Holds the database file (`database.db`) after app runs |

---

## 🚪 Authentication & Access Control:

- User signup and login.
- Creators can register after becoming users.
- Admin has default credentials for dashboard access.

---

## ✅ App Functionalities Summary:

| Feature                  | User | Creator | Admin |
|------------------------- |---- |---- |---- |
| Stream & Rate Songs       | ✅ | ✅ | ❌ |
| Create Playlists          | ✅ | ✅ | ❌ |
| Add/Edit Songs/Albums     | ❌ | ✅ | ❌ |
| View App Statistics       | ❌ | ❌ | ✅ |
| Flag/Unflag Content       | ❌ | ❌ | ✅ |
| Blacklist/Whitelist Users | ❌ | ❌ | ✅ |

---

## 🚩 Challenges Solved:

- **Role-based Login & Access** using Flask-Login and Flask decorators.
- **Dynamic Search Queries** for flexible song/album search.
- **Efficient Data Management** using SQLAlchemy ORM.
- **UI Rendering** with Jinja2 templates and Flask Flash messages.

---

## 🎥 Project Demonstration Video:

[![Watch Demo](https://img.shields.io/badge/Project_Demo-YouTube-red?style=for-the-badge)](https://drive.google.com/file/d/1kbomvdXvVGIdFoBtXMANjv1iklybWts6/view?usp=sharing)

---

## 🌱 Future Improvements:

- 🎧 Audio streaming optimization
- 🌐 Responsive UI for mobile devices
- 🔎 Advanced song/album filtering and recommendations
- 📈 User listening analytics for creators

---

## 🌟 Thank You for Visiting!  
*Feel free to fork, star ⭐, or contribute!*

