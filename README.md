# Hi Engineering Interview

Welcome! This is a short, practical interview designed to give you a feel for what day-to-day engineering at Hi looks like. You'll be working in a simplified version of our real codebase, adding features the same way our team does.

Feel free to use AI tools to help you complete the work — we use a lot of Claude Code ourselves. What matters is the end result.

**You will be evaluated on:**

- **Correctness** — Does the feature work as described?
- **Consistency** — Does your code follow the conventions and patterns already in the codebase?
- **Production readiness** — Could we ship your code to production as-is?

When you're finished, see the [Submission](#submission) section at the bottom for how to submit your work.

## Tasks

### Task 1: Client Detail Page

Right now, our advisors can see a list of their clients but can't click into any of them. We need a detail page so that when an advisor clicks on a client in the list, they're taken to a page that shows that client's full information. This will also serve as the foundation for other client-level features (like the notes feature below).

### Task 2: Client Notes

Our advisors frequently need to jot down notes after calls and meetings with their clients — things like action items, personal details to remember, or summaries of what was discussed. Add a notes feature to the client detail page where advisors can leave notes on a client. Each note should show who left it and when, since multiple advisors at a firm may be working with the same client.

### Task 3: Create New Clients

When a new client signs up with an advisor, the advisor needs a way to add them to the system. Right now the only way to create clients is through the database directly. Add a way for advisors to create new clients from the frontend. The new client should appear in the clients list after creation.

## Running the Code

### Database

Start the database:

```bash
cd backend
docker compose up -d
```

Run migrations:

```bash
poetry run alembic upgrade head
```

Insert starter data (test user and clients):

```bash
poetry run python scripts/insert_starter_data.py
```

### Backend

Install dependencies:

```bash
cd backend
poetry install
```

Start the server (runs on port 10001):

```bash
poetry run dev
```

### Frontend

Install dependencies:

```bash
cd frontend
yarn install
```

Start the dev server:

```bash
yarn dev
```

### Creating Migrations

After adding or modifying a model, generate a migration:

```bash
cd backend
poetry run alembic revision --autogenerate -m "describe your change"
```

Then apply it:

```bash
poetry run alembic upgrade head
```

### Testing

```bash
cd backend
poetry run pytest
```

## Submission

When you're done, submit your work by running the submission script from the interview directory:

```bash
./submit.sh
```

The script will prompt you for your name, email, and a short description of the changes you made and your reasoning. It will then zip up your project (including git history) and upload it for review.
