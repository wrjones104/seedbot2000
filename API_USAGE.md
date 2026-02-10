# FF6WorldsCollide Seed Generation API

The Seed Generation API allows users to generate Final Fantasy 6 Worlds Collide randomizer seeds programmatically.

## Authentication

All API requests require an API Key. You can generate an API Key from your profile page on the website.

Include the API Key in the `Authorization` HTTP header with the `Bearer` scheme for every request.

```bash
Authorization: Bearer YOUR_API_KEY_HERE
```

## Endpoints

### 1. Generate Seed

Initiates the seed generation process. This is an asynchronous operation.

*   **URL:** `https://seedbot.net/api/v1/seed/generate`
*   **Method:** `POST`
*   **Content-Type:** `application/json`

**Parameters:**

*   `type` (string, required): The type of seed to generate. Options:
    *   `preset`: Use an existing preset.
    *   `standard`: Use the standard racing flags.
    *   `chaos`: Use chaos flags.
    *   `true_chaos`: Use true chaos flags.
    *   `custom` (or `flagset`, `flags`): Use a custom flag string.
*   `preset` (string, optional): Required if `type` is `preset`. The name of the preset to use (e.g., "Ultros League", "SotW").
*   `flags` (string, optional): Required if `type` is `custom`. The full flag string.
*   `args` (array of strings, optional): Additional arguments to modify the seed (e.g., `["paint", "tunes"]`). Note: Hyphens will be automatically prepended if omitted.

**Example Request:**

```json
{
    "type": "preset",
    "preset": "Ultros League",
    "args": ["paint"]
}
```

**Example Response:**

```json
{
    "task_id": "c8f5e2d1-4b6a-4f8c-9d3e-1a2b3c4d5e6f",
    "status_url": "https://seedbot.net/api/v1/seed/status/c8f5e2d1-4b6a-4f8c-9d3e-1a2b3c4d5e6f/"
}
```

### 2. Check Status

Checks the progress of a seed generation task.

*   **URL:** `https://seedbot.net/api/v1/seed/status/<task_id>/`
*   **Method:** `GET`

**Example Response (In Progress):**

```json
{
    "task_id": "c8f5e2d1-4b6a-4f8c-9d3e-1a2b3c4d5e6f",
    "status": "PROGRESS",
    "progress": "Generating Seed..."
}
```

**Example Response (Success):**

```json
{
    "task_id": "c8f5e2d1-4b6a-4f8c-9d3e-1a2b3c4d5e6f",
    "status": "SUCCESS",
    "result_url": "https://seedbot.net/media/preset_Ultros_League.zip",
    "download_url": "https://seedbot.net/api/v1/seed/c8f5e2d1-4b6a-4f8c-9d3e-1a2b3c4d5e6f/download"
}
```

**Example Response (Failure):**

```json
{
    "task_id": "c8f5e2d1-4b6a-4f8c-9d3e-1a2b3c4d5e6f",
    "status": "FAILURE",
    "error": "An unexpected error occurred..."
}
```

### 3. Download Seed

Downloads the generated seed zip file directly.

*   **URL:** `https://seedbot.net/api/v1/seed/<task_id>/download`
*   **Method:** `GET`

**Response:**
*   A binary stream of the ZIP file.

## Example Workflow (curl)

1.  **Generate Seed:**
    ```bash
    curl -X POST https://seedbot.net/api/v1/seed/generate \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer YOUR_KEY" \
         -d '{"type": "standard", "args": ["paint"]}'
    ```
    Response: `{"task_id": "..."}`

2.  **Poll Status:**
    ```bash
    curl -H "Authorization: Bearer YOUR_KEY" https://seedbot.net/api/v1/seed/status/<TASK_ID>/
    ```
    Repeat until `status` is `SUCCESS`.

3.  **Download:**
    ```bash
    curl -H "Authorization: Bearer YOUR_KEY" -O -J https://seedbot.net/api/v1/seed/<TASK_ID>/download
    ```
