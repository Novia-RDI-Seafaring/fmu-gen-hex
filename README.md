# fmu-gen-hex
`fmu-gen-hex` is a Python package designed to facilitate the generation of Functional Mock-up Units (FMUs) from heat exchanger datasheets. This package streamlines the process of converting data from PDF documents into FMU models, enabling users to simulate and analyze heat exchanger performance efficiently.

## Technologies Used
...

2. [MERI](https://github.com/Novia-RDI-Seafaring/MERI/tree/main): Parameter extraction from data sheets
3. [Docker](https://www.docker.com/): Containerization
4. [VSC/Cursor Remote - Containers](https://code.visualstudio.com/docs/remote/containers): Development 

## Getting Started

### Prerequisites

- Docker
- VS Code with Remote - Containers extension (for development)

### Development Setup

1. Clone this repository:
   ```
   git clone https://github.com/Novia-RDI-Seafaring/fmu-gen-hex
   cd fmu-gen-hex
   ```

2. Open the project in VS Code/ Cursor:
   ```
   code .
   ```

3. When prompted, click "Reopen in Container" or use the command palette (F1) and select "Remote-Containers: Reopen in Container".

4. VS Code will build the development container and set up the environment. This may take a few minutes the first time.

5. Once the container is ready, you can start developing. 

### Running the Application

To run the application outside of the development container:

1. Ensure you have Docker and Docker Compose installed.

2. Build and run the application (`-d` in background):
   ```
   docker-compose up -d
   ```

3. Access the application at `http://localhost:5012`.


## Project Configuration


### Docker

- `docker/app.Dockerfile`: Production Docker image
- `docker/dev.Dockerfile`: Development Docker image
- `docker-compose.yml`: Defines the service for running the application

### VSC / Cursor Development Container

The `.devcontainer/devcontainer.json` file configures the development container for VS Code, ensuring a consistent development environment.