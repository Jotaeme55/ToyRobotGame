# Toy Robot Game

This project is an implementation of the Toy Robot Game, a small technical test proposed by Mott MacDonald. The goal of the game is to simulate the movement of a toy robot on a square tabletop based on a series of text commands that control its position and orientation.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** – [Download Python](https://www.python.org/downloads/)
- **Node.js v20.19.5 or higher** (recommended v20.19.5 or v22.12.0+) – [Download Node.js](https://nodejs.org/)
- **pip** (Python package manager)
- **npm** (included with Node.js)

## Verify installed versions

```bash
python --version
node --version
npm --version
```

### Available Ports

Make sure the following ports are free and available:

- **Port 5000** – Flask backend server
- **Port 5173** – Vue frontend server

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Jotaeme55/ToyRobotGame.git
    cd ToyRobotGame
    ```

2. **Navigate to the backend folder**
    ```bash
    cd backend
    ```

3. **Create a virtual environment (recommended)**
    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment**
    - On **Windows**:
      ```bash
      venv\Scripts\activate
      ```
    - On **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

5. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

6. **Navigate to the frontend folder**
    ```bash
    cd ..
    npm install
    ```

## Execution

After completing the previous steps, you need to open two terminal windows:

1. **Backend terminal**

   Navigate to the backend folder, activate the virtual environment, and run:
   ```bash
   py app.py
   ```
   or  
   ```bash
   python app.py
   ```
   Then you will have an instance of the backend running on **port 5000**.

2. **Frontend terminal**

   Open a new terminal and run:
   ```bash
   npm run dev
   ```
   Then you will have an instance of the frontend running on **port 5173**.

## Running Tests

If you want to execute the tests, just open a new terminal and run:

```bash
pytest
```
or  
```bash
pytest --cov
```

---

# Features & Architecture

## Backend Architecture

The backend follows a layered architecture pattern for better code organization and maintainability.

### Layers Overview

#### Controllers (`controllers/`)

- Handle HTTP requests and responses
- Validate input data
- Call appropriate services
- Return formatted responses
- **Files:** `BoardController.py`, `RobotController.py`

#### Services (`services/`)

- Contain business logic
- Process data and apply business rules
- Coordinate between controllers and repositories
- **Files:** `BoardService.py`, `RobotService.py`

#### Repositories (`repositories/`)

- Data access layer
- Handle data persistence and retrieval
- Abstract database operations
- **Files:** `BoardRepository.py`, `RobotRepository.py`, `IRepository.py`

#### Models (`models/`)

- Define data structures
- Represent domain entities
- **Files:** `Board.py`, `Robot.py`, `Wall.py`

It follows **dependency injection** pattern — all classes are defined in `app.py`, which manages routes, exceptions, and ports.

### SOLID Principles

- **S – Single Responsibility Principle:** Each class has one reason to change (Controllers handle requests, Services handle business logic, Repositories handle data).
- **O – Open/Closed Principle:** Code is open for extension but closed for modification through abstract interfaces.
- **L – Liskov Substitution Principle:** Repository implementations can be substituted without breaking functionality (any repository implementing `IRepository` can replace another).
- **I – Interface Segregation Principle:** `IRepository.py` defines a clean, focused interface with only essential CRUD operations.
- **D – Dependency Inversion Principle:** Services depend on abstractions, not concrete implementations. Example: `BoardService` receives `BoardRepository` via constructor injection, but both depend on the `IRepository` interface contract.

### Design Patterns Used

- **Repository Pattern:** Abstracts data persistence through `IRepository` interface (using Python’s `ABC`). `BoardRepository` and `RobotRepository` implement this interface, handling JSON file storage.
- **Generic Repository:** `IRepository` uses Python generics (`Generic[T]`) to create a reusable interface for any entity type.
- **Service Layer Pattern:** Business logic is encapsulated in services (`BoardService`, `RobotService`) that orchestrate operations between controllers and repositories.
- **Layered Architecture:** Clear separation of concerns across layers (Presentation → Business → Data).
- **Dependency Injection:** Services receive repository instances through constructors (e.g., `BoardService.__init__(self, repository: BoardRepository)`), enabling loose coupling and easier testing.
- **Abstract Base Classes (ABC):** `IRepository` uses Python’s `ABC` module to enforce interface contracts at runtime.
- **Exception Handling:** Custom exceptions (`WallOutOfBoundsException`, `WallAlreadyExistsException`) propagate from models through services to controllers for centralized error handling.

---

## Frontend Architecture

The frontend is built with **Vue 3** using the **Composition API** and follows a component-based architecture with clear separation of concerns.

### Component Responsibilities

#### `Board.vue` – Visual Representation

- Renders the game board as a dynamic grid
- Displays walls (🧱), robot position, and cell coordinates
- Updates robot image based on facing direction (North, South, East, West)
- Responsive design with CSS Grid
- Real-time updates when board or robot state changes

#### `GameSetup.vue` – Game Configuration

- Create board with custom dimensions (3–10 width/height)
- Add walls to specific coordinates
- Reset entire game (board + robot)
- Input validation and error feedback
- Loading states for async operations

#### `RobotControls.vue` – Robot Operations

- Place/reposition robot at specific coordinates
- Movement controls (forward, turn left, turn right)
- Get current robot position report
- Interactive control grid layout
- Conditional rendering based on game state

#### `api.js` – Backend Communication Service

- Centralized **Axios** instance for HTTP requests
- Base URL configuration for Flask backend
- API methods for all board and robot operations
- Error handling and response parsing
