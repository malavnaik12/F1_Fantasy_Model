# F1 Fantasy Team Builder
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">App Usage</a></li>
    <li><a href="#overall-tech-stack">Tech Stack</a></li>
    <li><a href="#genetic-algorithm-details">GA Details</a></li>
    <li><a href="#notes-for-future-evelopment">App Notes</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact-info">Contact</a></li>
  </ol>
</details>


## About the Project
The following repository uses a Genetic Algorithm (GA) to create a F1 Fantasy Team optimized for maximum performance within a given budget. 

The teams are developed using F1 driver and constructors prices, along with the weekly budget constraints, given on the F1 Fanstasy [website](https://fantasy.formula1.com/en/create-team).

The prices for each driver and constructor are static at the start of the season and dynamically evolve as the season goes on depending on their respective performance. Similarly, a budget of 100 million is set out at the season and the amount grows and contracts as the season progresses depending on performance.

## Getting Started
`[Insert pic here]`

The gif shows at a high-level how the user can interact with the UI, above UI is hosted [here](https://f1-fantasy-model.onrender.com/).
- The highest degree of user interaction will be on the Prices page
  - Here, the user will have to input the prices of drivers and constructors for the given week based on the F1 Fantasy Game website

## Overall Tech Stack
![tech_stack_image](readme_images/tech_stack_image.png)

- Python
  - All scripts to handle:
    - FastAPI routes to and from frontend
    - Processing frontend inputs
    - Populating frontend with default, queryed, or computed items
    - Using [FastF1](https://github.com/theOehrly/Fast-F1) to access F1 session results
    - Files to interface with "database"

- FastAPI
  - Handles the routes between the backend and frontend for the UI pages outlined in the Vue section 

- Vue
  - Frontend pages of interest
    - Main page: Nothing too exciting, just tells the user to navigate to the Positions tab
    - Positions: Uses FastF1 to populate the positions of drivers for user-specified race weekend
    - Prices: User inputs for driver and constructor prices for a given user-specified race weekened
    - Optimizer Inputs: Parameters used in GA execution to create the optimal team, more details provided in the <a href="#genetic-algorithm-details">GA Details</a> Section
    - Generate Team: The optimal team generation process is initiated here and the team is displayed

- Render
  - Used for hosting the repository
    - [Frontend](https://f1-fantasy-model.onrender.com/): The application UI
    - [Backend](https://f1-fantasy-model-backend.onrender.com/docs): Here, the FastAPI routes can be visualized and tinkered with

- Note that a database service isn't listed here. I started making this app before I understood what a database was or how a database was used so I implemented a local .json file based "database".
  - I **am** planning on a SQLite integration for this app but I'm busy working on other side-projects at the moment. :)

## Optimizer Details
![ga_image](readme_images/ga_image.png)
```mermaid
flowchart TD
  A[GA Inputs from UI] --> B[Pull Driver & Constructor Data from database.json];
  B -- For each generation --> C[Initialize Population: Teams of 5 Drivers and 2 Constructors];
  C --> D[Calulate Fitness Score];
  D --> E[Evolve Population Individuals];
  E --> F{Final Generation?};
  F -- Yes --> G[Optimal Team Metrics to UI];
  F -- No --> B;
```

Intra-Generation iteration employs the following mechanisms, and the following chart outlines what goes on within each generation
- Elitism: For Generation > 1, keep the team with the best fitness within population set 
- Crossover: Select 2 parent teams and create 2 corresponding child teams and keep the best child team if it is better than both parents, keep best parent team otherwise
  - [Tournament Selection](https://www.baeldung.com/cs/ga-tournament-selection) used to select the parent teams for Crossover
- Mutation: If invoked, mutate the team until a team with better fitness value is created
```mermaid
flowchart TD
  A[For Ind. in Pop. Set] --> B{Perform Crossover?};
  B -- Yes --> C[Select 2 Parent Teams];
  C --> D[Create New Team from Parents];
  B -- No --> E[Keep Original Team];
  D --> F[Perform Mutation];
  E --> F[Perform Mutation];
  F --> G{New team > old team?};
  G -- Yes --> H[Keep New Team];
  G -- No --> I[Keep Old Team];
  H --> J[Save team];
  I --> J[Save team];
  J --> K{End of Pop. Set?};
  K -- No --> A;
  K -- Yes --> L[On to Next Generation];
```

## Notes for Future Development
1) Future version will include a way to account for the various perks in the F1 Fantasy Game (see Picking a Team section [here](https://fantasy.formula1.com/en/faqs))
2) I am actively working on a SQLite-based integration and a deployment on AWS, both things I wasnt to learn!
3) I am also learning and working on unit tests, to make the app a bit more fault-tolerant.
4) I am learning about setting up microservices, and will have a way for user to create accounts and generate optimal teams for their own inputs!

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.


## Contact Info
Malav Naik \
Email: malavnaik12@gmail.com \
To learn more about myself and other projects I have contributed to, visit my [website.](https://sites.google.com/view/malavnaik) :)