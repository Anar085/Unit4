# Project 4: 

## Criteria A: Planning

## Problem definition
  My client, S.S, is head of the Aviation club using Microsoft Flight Simulator, which is one of the most advanced flight simulators ever made[^1]. As this club has a substantial variety of users, it is quite challenging to manage its community-created content, which limits the user experience. 
  Firstly, there is no centralized and unified system for managing and consuming add-ons such as scenery packs, aircraft mods, liveries. Currently, external platforms are used to browse and discover new mods, in which it is hardly possible to review mods before installation and to track already installed ones. Secondly, there is no direct access to the features of all aircrafts used in the simulator, making aircraft selection harder. Thirdly,  developers also do not have a structured way to manage their uploaded content for their mods, limiting quality content. Additionally, there is not a chance to examine and verify the uploaded content, which leads users to feel unsafe about the addon they desire. Lastly, installed mods cause crashes or do not work properly due to version mismatches or missing dependencies as users have to first research and then manually check for conflicts between add-ons. 

***See the evidence of the consultation in the Appendix***.


## Proposed Solution
  To address the issues the Aviation club reported, I propose to develop a web-based MSFS Add-on Management Platform. 
  In my proposed platform, each user will have their own “My Add-on Library” page, where they can see all the add-ons they added from the library, install them, and see the list of installed ones. A key part of the system is the Conflict Checker. Before installing anything, the system will check if the add-on works with the user’s MSFS version and whether it needs other add-ons to function. If there is a problem, the system will show simple suggestions on how to fix it. There will also be an Aircraft Comparison Tool that lets users compare aircraft stats in a simple side-by-side graph to help them decide which one to install. Overall, instead of members downloading mods from random websites, the platform will let them browse add-ons, compare aircrafts by some basic metrics, install them though their libraries, and keep their add-on conflicts resolved.
  The platform also helps developers and admins. Developers will get a page where they can upload their add-ons, with its metadata, version and dependency info, and see the details of all their submissions. Admins get a dashboard of three choices of managing either users, developers, or addons. They will be able to  manage users and developers, install proposed add-ons, approve or deny them, and keep the system organized. Admin approval is required for any add-on to become visible to users to make sure everything added is safe and high quality.
  Overall, this project turns the messy MSFS modding process into a single website where members can install add-ons without conflicts, developers can submit their work properly, and admins can control what gets published to the users.

## Success Criterions


[^1]: “Microsoft Flight Simulator 2024.” Microsoft Flight Simulator, www.flightsimulator.com/microsoft-flight-simulator-2024/. 


### 1. Authentication
1. Authenticates users, developers, and administrators, allowing sign-ups and logins. 
* **[ISSUE TACKLED]**: `Unauthenticated access`

### 2. Add-on Browsing
1. Allows users to browse a categorized add-on library (aircraft, liveries, and sceneries), add desired items to their personal library, and install them.
* **[ISSUE TACKLED]**: `Fragmentation in mod discovery`

### 3. Conflict Detection & Resolution
1. The system detects potential installation conflicts: missing dependencies, version mismatches, or cyclic dependencies. 
2. The system provides actionable suggestions for detected conflicts. 
* **[ISSUE TACKLED]**: `Crashes and malfunctioning caused by conflicted installation`

### 4. Aircraft Comparison
1. Compares aircraft performance metrics (max speed, range, MTOW, fuel capacity, climb rate) using visual comparison graphs.
* **[ISSUE TACKLED]**: `Guesswork in aircraft selection`

### 5. Developer Submission
1. The system allows developers to view data analytics regarding their add-on submissions.
2. The system enables developers to propose add-ons by uploading them along with their metadata. 
* **[ISSUE TACKLED]**: `Decentralized add-on submission`

### 6. Administrator Management
1. The system allows administrators to manage users.
2. The system allows administrators to manage developers and their submissions (approving or declining add-on proposals).
3. The system allows administrators to manage all active add-ons in the database. 
* **[ISSUE TACKLED]**: `Fragmented management, Unverified addons`

# Criteria B: Design

## Proposed Design
  I proposed to my client to develop a full-stack web application using Python Flask for backend, using HTML, CSS, and JavaScript for frontend, and using SQLite for database. And here is why:
	Firstly, for backend, I proposed to use Flask over its alternatives Django and Node.js. Django is powerful and “batteries-included” framework that is used for advanced structured projects, and it has many built-in tools that are unnecessarily complex for our proposed system[^2]. On the other hand, Node.js is also mostly used in high-concurrency application development[^3]. Thus, Flask is a great choice for small, simple projects and it offers flexibility and is easy to get started with[^2]. As Flask is in Python, the proposed solution also benefits from it: Python is one of the most versatile languages for backend development because of its clean syntax and it supports prototyping, which is essential for add-on website[^4]. 
	Secondly, for frontend, I proposed to use HTML, CSS, and JavaScript. This triad is compatible with almost all modern web apps and improves layouts and interactiveness. There are alternatives like Flutter and React Native, but my proposed ones offer faster load times and broader accessibility. Hence this triad lets developers efficiently structure and script these kind of tasks[^5]. For CSS, I took the template from this source[^6], and I made changes on.  
Lastly, I decided that the system needs a database for data storage. Because a database is an organized repository of related information stored in a manner that enables it to be easily accessed, managed, and updated[^7], which are essential for an add-on website. I proposed to use SQLite over its alternatives MySQL and PostgreSQL. The others offer better  under high concurrency. But as shown in this article[^8], SQLite is often a better choice for applications with lower concurrency, simple setups, and embedded use cases, which works for proposed solution.

[^2]: Software Testing Help. “Django vs Flask vs Node: Which One Is Better?” SoftwareTestingHelp, 17 Feb. 2024, www.softwaretestinghelp.com/django-vs-flask-vs-node/.
[^3]: “Node.js Introduction.” GeeksforGeeks, 20 Oct. 2021, www.geeksforgeeks.org/node-js-introduction/.
[^4]: “Why Python Is the Best Choice for Web Development.” STX Next, www.stxnext.com/blog/python-for-web-development.
[^5]: Bliss Drive. “Why Do Web Developers Use HTML, CSS, and JavaScript?” Bliss Drive, https://www.blissdrive.com/seo/why-do-web-developers-use-html-css-and-javascript/#:~:text=HTML%2C%20CSS%2C%20and%20JavaScript%20are,perform%20various%20client%2Dside%20tasks.
[^6]: Ludiflex. “How to Create a Website with Modern Login and Register Form - HTML, CSS, JavaScript.” Ludiflex, 30 Mar. 2023, www.ludiflex.com/how-to-create-a-website-with-modern-login-and-register-form-html-css-javascript/. 
[^7]: Ramakrishnan, Manasa. “What Is a Database: How Does It Store & Manage Data Effectively.” Emeritus, 13 May 2024, https://emeritus.org/blog/data-science-and-analytics-what-is-a-database/. 
[^8]: DigitalOcean. “SQLite vs MySQL vs PostgreSQL: A Comparison of Relational Database Management Systems.” DigitalOcean Community Tutorials, 24 Mar. 2021, https://www.digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems.







