# Course 1 Supplement — Systems Thinking in the AI Era

Code, labs, and challenge templates that accompany **Course I: The Seven Building Blocks** at [systemthinkinglab.ai](https://systemthinkinglab.ai).

You do not need this repo to take the course. The course site walks you through everything. This repo exists so you can:

- Run the discovery labs locally on your machine.
- Download the challenge submission templates as plain markdown.
- Read the canonical Python implementations of the 7 building blocks and 3 external entities.

## Repository structure

```
course1-supplement/
├── building_blocks/
│   ├── building_blocks.py     # The 7 universal building blocks
│   ├── external_entities.py   # The 3 external entities
│   └── __init__.py
│
├── labs/course1/
│   ├── lab1_queue_worker.py   # Lab 1: Queue + Worker discovery
│   └── lab2_time_worker.py    # Lab 2: Time + Worker discovery
│
├── challenges/course1/
│   ├── part1-mvp-foundation.md   # Challenge 1, Part 1: MVP Foundation
│   ├── part2-viral-growth.md     # Challenge 1, Part 2: Viral Growth Evolution
│   └── part3-live-streaming.md   # Challenge 1, Part 3: Live Cooking Sessions
│
├── requirements.txt
└── LICENSE
```

## The 7 building blocks

| Type | Block | Description |
|------|-------|-------------|
| Task | **Service** | Synchronous request/response processing |
| Task | **Worker** | Asynchronous background processing |
| Storage | **Queue** | Message passing and task hand-off |
| Storage | **Key-Value Store** | Caching and fast lookups |
| Storage | **File Store** | Media and large blob storage |
| Storage | **Relational Database** | Structured data with relationships |
| Storage | **Vector Database** | AI embeddings and similarity search |

## The 3 external entities

| Entity | Description |
|--------|-------------|
| **User** | Human interactions with the system |
| **External Service** | Third-party APIs and integrations |
| **Time** | Scheduled triggers and time-based events |

## Running the labs

### Prerequisites

- Python 3.8 or newer

### Setup

```bash
git clone https://github.com/systemthinkinglab/course1-supplement.git
cd course1-supplement

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run a lab

```bash
python labs/course1/lab1_queue_worker.py
python labs/course1/lab2_time_worker.py
```

Each lab is self-contained, prints a typewriter-style narrative, and asks 3 multiple-choice questions per experiment. Read the prompts and answer at your own pace.

## The challenge templates

`challenges/course1/` contains the technical design document templates for the 3-part Course 1 challenge: **ChefConnect, a social recipe platform.**

| Part | Title | What you design |
|------|-------|-----------------|
| 1 | **MVP Foundation** | The initial 5-requirement architecture: recipes, search, user profiles, photo upload, social feed. |
| 2 | **Viral Growth Evolution** | The platform jumps from 10K to 2M users in 3 months. Add caching, optimization, and scale recovery without adding features. |
| 3 | **Live Cooking Sessions** | Add live video broadcasting with sub-100ms chat for up to 5,000 concurrent viewers per chef, on top of your Part 2 design. |

Each part is a separate submission. The course site grades your design with AI-powered feedback; the templates here mirror the structure the grader expects.

## Course series

This is Course I of a 4-course series:

- **Course I:** The Seven Building Blocks (you are here)
- **Course II:** Content Systems (Instagram, Netflix, YouTube)
- **Course III:** Real-Time Systems (Slack, Discord, WhatsApp)
- **Course IV:** Business Integration Systems (Stripe, Shopify, Salesforce)

[systemthinkinglab.ai](https://systemthinkinglab.ai)

## License

See [LICENSE](LICENSE).

## Author

Kay Ashaolu — [UC Berkeley School of Information](https://www.ischool.berkeley.edu/people/kay-ashaolu)
