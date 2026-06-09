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

## System Diagram

<img width="6232" height="5458" alt="Untitled diagram-2026-02-05-154933" src="https://github.com/user-attachments/assets/f21e4b66-2768-4a76-a961-879253741ccb" />

**Figure 2** *System diagram of proposed solution*

## System Flowchart
<img width="1252" height="975" alt="IA_system_flowchart drawio" src="https://github.com/user-attachments/assets/956b4ae3-96f8-47f2-acc9-48a7f812f5cd" />

**Figure 3** *System flowchart of the proposed solution*

## Entity-Relationship (ER) Diagram

<img width="1309" height="996" alt="IA_ER_final" src="https://github.com/user-attachments/assets/ed394238-081d-4fc1-9d1f-8d469a321ae3" />

**Figure 4** *Entity-Relationship Diagram of the database of the proposed solution*  

This diagram models the database schema using Chen notation: entities (tables) by rectangles and their attributes (columns) by ellipses. Rules of association: a single dash | donates “one” and a crow’s foot with a circle 0 donates “zero or many”. PK indicates Primary Key, and the Addon entity has a recursive relationship. 


<img width="1494" height="920" alt="IA_ER_final2" src="https://github.com/user-attachments/assets/f78271de-5747-4785-9093-0fc6ae114da4" />

**Figure 5** *Entity-Relationship Diagram of the database of the proposed solution 2* 

This ER diagram belongs to the Aircrafts table from the database, which is only used for the visual comparison. Hence, it has no relationship with the rest of the database. 


## UML diagram
<img width="1826" height="1282" alt="IA_UML_draft2" src="https://github.com/user-attachments/assets/bea3b1dd-cda5-4d48-a346-24c32f9c2b54" />

**Figure 6** *Unified Model Language (UML) of the proposed solution*

This UML Class diagram shows the proposed system is organized into logical packages: Actors, Flask Application, Domain & Persistence, and Database Schema. The FlaskApp class is stereotyped as a `<<Controller>>`, representing the app.py file where all URL routing and primary application logic reside. It utilizes `<<Service>>` classes like Database_Manager (for data persistence) and Security (for authentication logic). As in the ER diagram, the database tables are abstracted as `<<Entity>>` classes. The system’s interactions: Actors interact with the FlaskApp (for example “proposes addons”), which in turn “uses” the service and “manages” the entity classes. 

## Test plan

| Test No | Test Goal | Test Description | Supposed Outcome | Pass/Error |
| :--- | :--- | :--- | :--- | :--- |
| **1** | To ensure the system authenticates users, developers, and administrators correctly. | 1. Run `app.py` and navigate to `http://127.0.0.1:5000`. <br>2. Register an Admin account: `admin`, `user`, `admin_user`, `admin@email.com`, `AdminPass123!`, Role: Admin, Privacy Code: anar. Log in to verify redirection to `/admin_main`, then log out.<br>3. Register a Developer account: `dev`, `one`, `dev_one`, `dev@email.com`, `DevPass123!`, Role: Developer. Log in to verify redirection to `/developer_main`, then log out.<br>4. Register User One (Low Version): `user`, `low`, `user_low`, `user.low@email.com`, `UserPass123!`, Role: User, MSFS: 1.27. Log in to verify redirection to `/user_main`, then log out.<br>5. Register User Two (Mid Version): `user`, `mid`, `user_mid`, `user.mid@email.com`, `UserPass123!`, Role: User, MSFS: 1.28. Log in to verify, then log out.<br>6. Register User Three (High Version): `user`, `high`, `user_high`, `user.high@email.com`, `UserPass123!`, Role: User, MSFS: 1.30. Log in to verify. | 1. Verify all five accounts are created successfully and exist in the `Users` table.<br>2. Verify each login redirects to the correct dashboard (`/admin_main`, `/developer_main`, `/user_main`).<br>3. Verify that `developer_library` and `user_library` tables have been created for the respective developer and user accounts. | Pass |
| **2** | To ensure users can browse, add, and install add-ons from their personal library. | 1. Log in as `user_low` (MSFS 1.27).<br>2. On `/user_main`, click "Add to Library" on the following add-ons: "A320neo Extended Pack", "Lufthansa A320 Livery", "Tokyo Haneda Scenery Pack", and "Retro Prop Aircraft".<br>3. Verify the success toast for each addition.<br>4. Navigate to "My Library". | 1. Verify that after step 4, all four selected add-ons are correctly listed in the "In Queue" table of `user_low`'s personal library. | Pass |
| **3.1** | To ensure the system correctly detects and reports missing dependency conflicts. | **Test 3.1a: MSFS Version Mismatch (Primary Addon)**<br>1. Log in as `user_low` (MSFS 1.27).<br>2. In "My Library", click "Install" on "Tokyo Haneda Scenery Pack" (which requires 1.30).<br><br>**Test 3.1b: MSFS Version Mismatch (Dependency)**<br>3. Still logged in as `user_low`, click "Install" on "A320neo Extended Pack".<br>4. In the first dialog ("Version Check Passed"), click "Proceed".<br><br>**Test 3.1c: Clean Dependency Check**<br>5. Log out and log in as `user_high` (MSFS 1.30). Add "Lufthansa A320 Livery" to the library.<br>6. In "My Library", click "Install" on "Lufthansa A320 Livery". Click "Proceed". | 1. Verify after step 2 that a "Version Mismatch" dialog appears immediately, stating the add-on requires MSFS 1.30.<br>2. Verify after step 4 that the system proceeds to the dependency check, and then a "Version Mismatch" dialog appears for the dependency ("Tokyo Haneda..."), explaining that it requires MSFS 1.30.<br>3. Verify after step 6 that a "Missing Dependency" dialog appears, correctly identifying that "A320neo Extended Pack" is required. | Pass |
| **3.2** | To ensure the system provides a functional suggestion to resolve a missing dependency. | 1. Following Test 3.1b, in the final "Version Checks Complete" dialog, click the "Install" button.<br>2. A "Library Check" dialog will appear. Click "Install All".<br>3. Following Test 3.1c, in the "Missing Dependency" dialog, click "Install All".<br>4. A "Library Check" dialog will appear. Click "Install All". | 1. Verify after step 2 that the user is presented with a dialog indicating that the add-ons will be installed, even with a version mismatch.<br>2. Verify that after step 4, file downloads are initiated for all required add-ons.<br>3. Verify a success toast "All required addons are installed successfully!" is displayed.<br>4. Verify after the page reloads that all add-ons in the chain are now listed in the "Installed" table. | Pass |
| **4** | To ensure the aircraft comparison tool visualizes performance metrics correctly. | 1. Log in as any user (e.g., `user_high`) and click "Compare Aircraft!".<br>2. Select "Cessna 172" from the left dropdown.<br>3. Select "DA62" from the right dropdown.<br>4. Change the selection in the left dropdown to "Spitfire Mk IX". | 1. Verify stats and images appear for Cessna 172 after step 2.<br>2. Verify stats and image appear for DA62 and the radar chart displays two distinct polygons after step 3.<br>3. Verify the left panel and the red polygon on the chart instantly update to reflect the new data for the Spitfire after step 4. | Pass |
| **5.1** | To ensure developers can view the status and data of their add-on submissions. | 1. Log in as the developer `dev_one`.<br>2. Observe the "My Addon Submissions" table. | 1. Verify the user is redirected to `/developer_main`.<br>2. Verify the table correctly lists all submissions with accurate Title, Version, and Status. | Pass |
| **5.2** | To ensure developers can propose new add-ons with all required metadata and files. | 1. From the developer dashboard, click "Propose Addon".<br>2. Attempt to submit with the title "A320neo Extended Pack" (which already exists).<br>3. Correct the title to a unique name like "Test Livery". Enter an invalid version "v1". Click "Submit".<br>4. Correct the version to "1.0.0". Fill out all fields, select files, and click "Submit". | 1. Verify error "An addon with that title already exists" is displayed after step 2.<br>2. Verify error "Invalid format for Version..." is displayed after step 3.<br>3. Verify after step 4 that the user is redirected to `/developer_main` and "Test Livery" is at the top of the table with status `awaiting`. | Pass |
| **6.1, 6.2** | To ensure administrators can manage users, developers, and their submissions. | 1. Log in as the admin `admin_user`. <br>2. Click "Manage Developers". Click "See Submissions" for `dev_one`. <br>3. For the "Test Livery" proposal, click "Approve". <br>4. For another pending proposal, click "Decline". <br>5. Navigate to "Manage Users" and click "Remove" on a test user (e.g., `user_mid`). Confirm the action. | 1. Verify after step 3 that "Test Livery" moves to the "Approved Addons" table.<br>2. Verify after step 4 that the other add-on's status becomes `declined`. <br>3. Verify after step 5 that the user is removed from the `Users` table and their `user_library_` table is dropped from the database. | Pass |
| **6.3** | To ensure administrators can manage the global add-on catalog and that approval is robust. | 1. Log in as `admin_user` and navigate to "Manage Addons". <br>2. Confirm "Test Livery" appears in the "Approved Addons" table.<br>3. Log out and log in as `user_high` and view the `/user_main` page.<br>4. Log in as `admin_user`, go to "Manage Addons", and click "Remove" for "Test Livery".<br>5. Log in as `user_high` one last time and view the `/user_main` page. | 1. Verify "Test Livery" is visible to the admin after step 2.<br>2. Verify "Test Livery" is now visible to the regular user after step 3.<br>3. Verify after step 4 that "Test Livery" is gone from the `Addons` table.<br>4. Verify after step 5 that "Test Livery" is no longer visible to the user. | Pass |


# Criteria C: Development

## List of techniques used

1. *Recursive graph traversal using Graph Theory* 
2. *Multi-Step Installation workflow*
3. *Data visualization on Polar Coordinates* 
4. *Min-Max Normalization* 
5. *Connection between Frontend and Backend*

### 1.  *Recursive graph traversal using Graph Theory*
To solve **SC#3.1** and **SC#3.2**, I had to handle add-on dependencies, that is, they rely on each other to function properly. For example, Emirates A380 Livery pack is dependent on latest version of Enhanced A380 aircraft pack, whereas Dubai Intl Airport scenery pack requires Emirates A380 Livery pack, and etc. To detect these problems before installation, at first, I attempted to use If-statements and loops. But then I encountered more complex dependencies examples where they had multiple transitive dependencies, or cycles where some add-ons indirectly depend on itself. These complexities made If-statements and loops useless, so to manage these dependencies I researched graph-based solutions[^9]. After research I learned about *Depth-First Search* and its use for topological sorting in graph theory[^10]. Through DFS and recursion stack, now I could track all visited nodes in a directed graph which represents the dependencies as a tree. First, I created *`DependencyGraph`* class because it can make all attributes and methods used for graphs reusable and structured:

```.py
class DependencyGraph:
   def __init__(self): #initializing attributes
       self.graph={}  #dictionary for holding the graph adjacency list
       self.resolved_cache={}  #dictionary to hold already resolved dependencies

```

Then I created *`add_dependecy()`* function (for reusability) to add dependency relationships to graph.

```.py
def add_dependency(self,addon_id,dependency_id):
   if addon_id not in self.graph:
       self.graph[addon_id]=set()  #Line 7
   self.graph[addon_id].add(dependency_id)  #adding dependency to graph
   self.resolved_cache.clear()  #clearing cache since graph is modified

```

In line 7, I used *`set()`* - python data structure, as it automatically prevents duplicate dependencies. Then, I created *`build_from_addons()`* function to build the graph using the list of add-ons.

```.py
def build_from_addons(self,addons):
   self.graph.clear()  #reseting the graph
   self.resolved_cache.clear()  #clearing cache
   for addon in addons:
       for dep_id in addon.dependencies.keys():  #iterating over each dependency
           self.add_dependency(addon.id,dep_id)  #adding it to the graph

```

Then, for managing special case, cycle dependency, I coded function *`detect_cycles()`* which uses the concept *Depth-First Search* to detect and return the list of cycles.

```.py
def detect_cycles(self):
   visited=set()  #set to track visited nodes
   rec_stack=set()  #set to track recursion stack
   cycles =[]  #list to keep detected cycles

     def dfs_cycle_detect(node,path):   #function for reusability that returns True or False
       if node in rec_stack:          
           cycle_start=path.index(node)  #determining start index of cycle
           cycle=path[cycle_start:]+ [node]  #extracting the cycle path
           cycles.append(cycle)  #stores detected cycle
           return True
       if node in visited:
           return False  #avoiding redundant visits
       visited.add(node)  #marking the current node as visited using built-in function add() to avoid overwriting it in other paths
       rec_stack.add(node)  #adding the node to the current recursion (call) stack to help detect cycles using built-in function add()
       path.append(node)     #adding the node to the path being tracked so I can reconstruct a cycle if one is found using built-in function append()
       for neighbor in self.graph.get(node,set()):
           if dfs_cycle_detect(neighbor,path):  #recursing over the dependencies to detect a cycle
               return True
       rec_stack.remove(node)   #exiting the node context
       path.pop()              #removes the step from path history
       return False

   for node in self.graph:  #running DFS from each unvisited node
       if node not in visited:
           dfs_cycle_detect(node,[])
   return cycles  # Return list of cycles

```

This function first defines **visited** and **rec_stack** sets and a **cycles** list. There is an inner recursive function **dfs_cycle_detect()** to implement Depth-First Search (DFS) which inputs **node** and **path**. First, by an `if`-statement, it checks if the current **node** is already in **rec_stack** to verify whether that **node** is part of the current traversal path. If so, first it gets the start index of the cycle by the built-in function **index()**. Then, by using *list slicing* in `path[cycle_start:]`, it extracts the part of **path**, starting from index **cycle_start** till the end (as the destination index is not mentioned). By using `+ [node]`, it appends the current node to the end to visualize the cycle (for example: `A->B->C->A`). It then uses an `if`-statement to avoid redundant visits. Through the next three lines, the function maintains the state of traversal in DFS. Then, by using a `for`-loop and the **.get()** method-which is a safe way to access the dictionary **self.graph** where keys are nodes and values are a `set` of its dependencies-as instead of a `KeyError` it returns the default value `set`, it iterates over all nodes that the current node depends on. Then, as the main part of DFS, I used an `if`-statement to recursively call the function **dfs_cycle_detect()** on every neighbor of the main node. The function **dfs_cycle_detect()** finalizes after exiting the node and clearing the path history. Ultimately, the function **detect_cycles()** finalizes by implementing DFS for each unvisited node using a `for`-loop and returning the list of detected cycles.

<img width="979" height="847" alt="cs_ia_3" src="https://github.com/user-attachments/assets/acc4c303-ab7e-42de-a021-b2a7c5106165" />

**Figure 7** *This flowchart represents the *`detect_conflicts()`* function from `Version_Mismatch_Strategy` class.*

<img width="762" height="859" alt="cs_ia_2" src="https://github.com/user-attachments/assets/2e2466ce-43ac-4e6e-8f53-ed7ad890f696" />

**Figure 8** *This flowchart represents the `detect_cycles()` function from `Dependency_Graph` class, which detects dependency cycles in a graph using depth-first search (DFS).*


[^9]: GeeksforGeeks. “Graph Theory Tutorial.” GeeksforGeeks, https://www.geeksforgeeks.org/graph-theory-tutorial/. 
[^10]: "Depth First Search or DFS for a Graph." GeeksforGeeks, 27 April 2023, https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/.



### 2.  *Multi-Step Installation workflow*

To solve **SC#3.2**, which requires clear suggestions for installation conflicts, I first tried to use *if-else* statements to create a simple “check-then-install” process. It was insufficient as users had to go through a series of sequential decisions without losing context. To solve this, I designed a multi-step installation workflow through a single backend route `/install_step`. This endpoint receives the current `step` (either `'version_check'`, `'dependency_check'`, or `'library_check'`) and a payload, then returns a JSON object that contains the instructions for the next step with specific dialog to show the user.


```.py
app.route('/install_step',methods=['POST'])
def install_step():
   data=request.get_json()
   step=data.get('step')
   # ...
   if step=='version_check':
       # processing version
       return jsonify({
           "next_step":"dependency_check", #  instruction for the next step
           "dialog": {...}               # data for the next UI dialog
       })
   elif step=='dependency_check':
       #  processing dependencies
       return jsonify({
           # a special instruction for the frontend to take over
           "next_step":"user_confirm_dependency_versions",
           "dependency_chain": dependency_chain
       })
   # ... etc.

```

As the user waits for the system to determine the dependencies, the frontend could not handle the interactive dependency version check. So to solve this, a special **next_step** instruction, **user_confirm_dependency_versions**, is sent. This triggers a unique client-side function that iterates through the dependency chain and uses JavaScript’s *async/await* with *Promise*-based dialog. This pauses the system, waits for the user to click one of the buttons, only then continues to the final **library_check** step[^11].

```.js
// here, the frontend pauses the workflow to wait for user input
async function runUserDependencyVersionChecks(chain, userLibraryId) {
   for (const dep of chain) {
       // version_check logic ...
       if (userMsfsVersion<minMsfs) {
           // the 'await' keyword pauses the function here until the user clicks a button
           const userChoice = await showPromiseDialog({...});
           if (userChoice==='Cancel') return; // aborting the entire process
       }
   }
   // only proceeding after the loop is complete
   const finalChoice=await showPromiseDialog({ ... });
   if (finalChoice==='Install') {
       sendInstallStep('library_check', ...); // resuming the workflow
   }
}
```

### 3.  *Data visualization on Polar Coordinates*

To address **SC#4**, which requires aircraft metrics visualization, I had to compare metrics such as max speed, range, MTOW, and fuel capacity. At first, I tried implementing *barcharts*, but as I am comparing more than *three metrics* of aircrafts, *barcharts* were hard to read and compare for choosing based on the most desirable metrics. To solve this issue, I researched about data visualization techniques for *multivariate* data [^12], as aircraft data contains, at each sample point, multiple scalar values that represent different simulated or measured quantities, and found about *radar charts* [^13]. Radar charts represent attributes that can be easily compared each along their own axis, and overall differences are apparent by the size and shape of the polygons. To implement this, I coded the method **create_Radar_Chart**:

```.js
create_Radar_Chart() {
    const container=d3.select('#chartContainer'); //selecting the chart container div where the radar chart will be drawn using d3 library
    const size=Math.min(this.dimensions.width,this.dimensions.height);
//determining the base size for the chart by picking smaller of width or height by using min() function
    const radius=size/2-100; //calculateing the radius of the radar chart
    const svg=container.append('svg')  //appending an SVG element to the container and seting its width and height
        .attr('width',size+200)
        .attr('height',size+100); //extra space for labels or padding

    const g=svg.append('g')
        .attr('transform', `translate(${size/2 + 100},${size/2 + 50})`); //appending a <g> element (group) to the SVG and translating it to the center of the chart area
}
```
Here `d3.select()`, `.append`, and `.attr` are parts of *D3.js library*. But to transform normalized aircraft metrics to coordinates on a radar chart I had to use maths to convert from *polar* to *Cartesian* coordinates, as radar charts are using *radial* plot, not *rectangular*.

```.js
const angleSlice=Math.PI *2/this.activeAttributes.length;
```
This line calculates the angular spacing, as full circle is $2\pi$, dividing it by the number of attributes gives equal angle spacings. `this.activeAttributes` is an array storing the metrics and `.length` finds the number of elements in that array.

```.js
const radialScale=d3.scaleLinear().domain([0,100]).range([0,radius]); //mapping metric magnitudes to radius
```
Here `d3.scaleLinear()` is a linear mapping function and `.domain([0,100])` is for input data range, from 0% to 100%. Then `.range([0,radius])` limits the range from center to edge, for example, if given `radialScale(60)`, it will return pixel distance related to 60% of radius. Then for *data points* in radar charts I did the conversions using `Math.cos()` and `Math.sin()` for *Cartesian* $(x,y)$[^14].

```.js
//setting the x-coordinate (cx) of each data point using polar to Cartesian conversion
.attr('cx',(d,i)=> {
    const angle=angleSlice*i - Math.PI/2; //calculating angle for current axis; -π/2 rotates first axis to top 
    return Math.cos(angle)*radialScale(d.value); //converting angle to x using cosine; scale data value to pixel radius
})
//setting the y-coordinate (cy) of each data point using polar to Cartesian conversion
.attr('cy',(d,i)=> {
    const angle=angleSlice*i - Math.PI/2;  //using same angle logic to match x-coordinate rotation
    return Math.sin(angle)*radialScale(d.value);  //converting angle to y using sine; scale data to radial distance
})
```
Here by `.attr('cx', (d,i) =>` , each data point **d** at index **i** is mapped to radical axis by multiplying **i** by *angleSlice*.

### 4.  *Min-Max Normalization*

To address **SC#4**, I had to compare aircraft metrics. But as they are in different units and magnitudes, their raw comparison would be *unfair*. That is why, I decided to normalize all data in common range 0-100.


```.js

normalizeData(data) {
   if (data.length===0) return [];  //checking if the input data array is empty; if so, return an empty array to avoid further processing

   const attributes=['maxSpeed','range','mtow','fuelCapacity', 'climbrate']; //defining the list of numeric aircraft attributes that needs normalization

   const normalized=data.map(d => ({ ...d }));
//creating deep copy of each data object to avoid modifying the original array

//looping over each attribute to normalize it independently  
   attributes.forEach(attr => {
       const values= data.map(d=>d[attr]); //extracting all values of the current attribute from the dataset into an array
       const min=d3.min(values); 
       const max=d3.max(values);   //computing maximum and minimum values of the current attribute using D3.js min and max function
       const range=max - min;  //calculating the range (max - min) to use in normalization formula

//looping over each data point to compute normalized values
       normalized.forEach(d =>{
           d[`${attr}_normalized`]=range > 0 ? (d[attr] - min) / range : 0; //adds a new property attr_normalized, this stores a decimal between 0 and 1 using the formula:(value - min)/range, if range is zero, fall back to 0 to avoid division by zero

           d[`${attr}_percent`]=Math.round(d[`${attr}_normalized`] * 100);
//adds another new property: attr_percent, this is the normalized value converted to a percentage and rounded
       });
   });
//returns normalized dataset
   return normalized;
}

```

Here, `data.map(...)` iterates through each object **d** in **data** array and `({ ...d })` is a *spread operator* to clone each object for copying. More importantly, `d['${attr}_normalized']` creates a new property using *template literals*, which means it works generically across all attributes. Then `(d[attr] - min) / range` in `range > 0 ? (d[attr] - min) / range : 0` scales each value to 0-1 range; if range equals 0, it avoids division by zero and assigns 0 instead. Then by using `Math.round()`, `d[${attr}_percent] = Math.round(...)` creates a new property and converts it into percentage in range 0-100.

### 5.  *Connection between Frontend and Backend*

Fundamentally, as a web application, the system connects the frontend interface and backend using *Flask routes* and *HTTP requests*. The following code examples given demonstrate the interaction between the main backend *app.py* and an example frontend *mylib.html*. 


```.py
@app.route('/mylib_<int:user_id>')
def mylib(user_id):
    # Backend reads user data from the database
    # and sends it to the frontend HTML template
    return render_template('mylib.html',
                           in_queue=in_queue_addons,
                           installed=installed_addons,
                           username=username,
                           user_msfs_version=user_msfs_version)

```


```.html
<!-- Frontend receives the data and displays it -->
{% for addon in in_queue %}
<tr>
  <td>{{ addon[1] }}</td>
</tr>
{% endfor %}

```
When a user performs an action like removing an add-on, the frontend sends a request to the backend. 

```.js
// Frontend sends user action to backend route
fetch('/simple_update_library', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ action: action, addon_id: userLibraryId })
});

```


```.py
@app.route('/simple_update_library', methods=['POST'])
def simple_update_library():
    #Backend receives request, updates database,
    #then returns result to frontend
    return jsonify({"status": "removed"})

// Frontend reads backend response and updates UI
if (result.status === 'removed') {
    row.remove();
}

```

Through these fundamental interactions the system completes as a whole: the frontend handles user interaction and the backend handles logic and database CRUD operations. 

[^11]: ReqBin. “JavaScript Fetch JSON Example.” ReqBin, https://reqbin.com/code/javascript/wc3qbk0b/javascript-fetch-json-example. 
[^12]: Amazon Web Services. “Visualize Multivariate Data Using a Radar Chart in Amazon QuickSight.” AWS News Blog, 6 Oct. 2022, https://aws.amazon.com/blogs/business-intelligence/visualize-multivariate-data-using-a-radar-chart-in-amazon-quicksight/.
[^13]: Andrews, Chris. “Radar Chart.” Middlebury College Computer Science Showcase, 2016, www.cs.middlebury.edu/~candrews/showcase/infovis_techniques_s16/radar_chart/.
[^14]: "Converting Polar to Cartesian Equations in Five Easy Steps." Cambridge Coaching Blog, https://blog.cambridgecoaching.com/converting-polar-to-cartesian-equations-in-five-easy-steps .  



# Criteria D: Functionality - showcase of actual product

[![Watch the App Showcase Video on YouTube]](https://youtu.be/OCr8RvXaiYE)


# Criteria E: Evaluation

## Evaluation of the product

The final product successfully meets all 6 SCs from the perspective of both client and developer. Authentication allows users, developers, administrators safely to sign up and login **(SC1)**. Users are able to browse addons that are proposed by developers and verified by administrators and have their personal libraries managing add-ons **(SC2)**. The conflict resolver system in personal libraries corrects all possible error cases and suggests clear solutions **(SC3)**. Aircraft comparison, using a radar chart comparing two aircraft, successfully minimizes guesswork **(SC4)**. Developers can propose add-ons and track their portfolio easily **(SC5)**. Administrators can manage users, developers, and add-ons (approving/declining submissions from developers). 


## Recommendations for Further Development

However, especially when expansion and scaling are considered, the product has some limitations: workflow state is mainly on the client side which is vulnerable if refreshes or connection loss happen; dependency relationships are given as strings in database which requires extra handling; security mechanisms such as file validations and admin encryption are limited to the prototype’s environment; versions are compared using simple strings and float which don’t support semantic versioning; dependency resolution loads all relationships right now which is not efficient as the system expands. 
Here are several solutions: developing the installation process as atomic database transactions to prevent mid-operation failures; for expansion, migrating to PostgreSQL from SQLite to prevent database being locked during multiple users; shift workflow to the client-side to prevent client desynchronization; introduce stricter requirements for file size and validation.



