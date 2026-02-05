# Antigravity Forum // GRID.ACCESS

<div align="center">
  <h3>Cyberpunk Underground Forum Simulation</h3>
  <p>A sophisticated Flask-based forum with ephemeral in-memory storage and high-fidelity cyberpunk aesthetics.</p>
</div>

## Overview

**Antigravity Forum** is a concept web application designed to simulate an underground hacker forum. It features a fully immersive "Cyberpunk" UI, complete with neon visuals, glassmorphism, and dynamic system widgets. The backend is powered by Flask and uses ephemeral in-memory storage, meaning all data is reset when the system shuts down—perfect for privacy-focused operations (or ephemeral labs).

## Features

*   **Ephemeral Architecture**: No database trace. All data lives in RAM.
*   **Professional UI/UX**: Custom CSS architecture with variables for Neon Pink (`#ff0055`) and Cyan (`#00f3ff`).
*   **Rich Content System**:
    *   SVG Auto-generated Avatars.
    *   Role-based badges (Admin, VIP).
    *   Network Activity & Trending Tags widgets.
*   **Simulation Data**: Pre-populated with elite users (ZeroCool, Morpheus) and cryptic thread content upon initialization.

## Installation & Usage

1.  **Prerequisites**:
    *   Python 3.x
    *   Flask

2.  **Install Dependencies**:
    ```bash
    pip install flask
    ```

3.  **Launch System**:
    ```bash
    # Default launch (Port 5000)
    python3 app.py

    # custom port configuration
    python3 app.py --port 8888
    ```

4.  **Access the Grid**:
    Navigate to `http://localhost:8888` (or your chosen port).

## Default Accounts

The system initializes with several high-profile handles. You can register a new identity, or modify the source code to access existing accounts.

*   `ZeroCool`
*   `Morpheus`
*   `Trinity`
*   `Neo`

## License

MIT License.
