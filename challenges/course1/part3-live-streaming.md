# Challenge 1 Part 3: Technical Design Document — Business Monetization Evolution

**Student Name**: [Your Name]
**Submission Date**: [Date]
**Challenge**: ChefConnect Social Recipe Platform — Part 3: Live Cooking Sessions

---

## ⚠️ IMPORTANT: Technology-Agnostic Design Required

Use **building block names** throughout (Service, Worker, Key-Value Store, File Store, Queue, Relational Database, Vector Database). Do **not** name specific technologies (PostgreSQL, Redis, AWS, RTMP, WebRTC, HLS, etc.) in your design decisions. Naming a tool earns automatic point deductions. The whole point of Part 3 is that you can reach for live video as a *pattern* without locking into a vendor.

## 📝 RECOMMENDED APPROACH: Draw First, Write Second

Before you fill this template in, sketch your evolved architecture using the Google Drawing template linked on the challenge page. Drag the 7 building blocks onto the canvas. Show the broadcast path, the chat path, and the recording path as separate flows. Then write your decisions here. The diagram surfaces the parallelism that prose hides.

---

## Innovation Context

*ChefConnect now serves 3 million users with excellent performance. The platform is stable. Market research shows huge demand for live cooking experiences. Your job in Part 3 is to add live cooking sessions without breaking the platform Part 2 just stabilized.*

**Primary Focus**: Add Requirement 7 (Live Cooking Sessions) on top of Parts 1-2. Chefs broadcast live video. Followers watch with sub-100ms chat latency. Up to 5,000 concurrent viewers per chef. Sessions auto-save for later viewing. Chefs schedule weekly sessions. The whole thing integrates seamlessly with existing recipes and profiles.

---

## Architecture Overview

**High-Level Description**:
[Describe how your Part 2 design evolves to add live cooking. What is the core idea: a separate broadcast/viewer plane glued to the existing platform via the profile and recipe Services? An External Service for the heavy video lifting? A queue-fanned chat plane? One paragraph.]

**Core Building Blocks Used**:
- [ ] Service (Blue Rectangle)
- [ ] Worker (Blue Trapezoid)
- [ ] Key-Value Store (Pink Diamond)
- [ ] File Store (Pink Pentagon)
- [ ] Queue (Pink Stacked Rectangles)
- [ ] Relational Database (Pink Cylinder)
- [ ] Vector Database (Pink Cube)
- [ ] User (Green Smiley)
- [ ] External Service (Green Cloud)
- [ ] Time (Green Hourglass)

---

## Requirements 1-6: Maintaining Platform Stability (40% of Grade)

### Stability Preservation Analysis

**Performance maintained**: [How you keep Part 2's sub-1-second recipe loads and sub-500ms search intact while a chef broadcasts to 5,000 viewers.]

**Core features protected**: [How recipe management, social, search, and profiles keep working while live sessions run alongside them.]

**Resource allocation**: [How live video traffic is isolated from the recipe browsing path so that one heavy stream cannot starve the other.]

### Integration Impact Assessment

**Recipe Management (Req 1)**: [How live sessions reference existing recipes without changing the recipe CRUD path. Sessions point at recipes; recipes do not need to know about sessions synchronously.]

**Social Features (Req 2)**: [How follow relationships drive who gets a "going live" notification and who sees the chat. Existing social tables should not need a schema rebuild.]

**Discovery & Search (Req 3)**: [How a chef being live shows up in search and discovery without slowing the search Service.]

**User Profiles (Req 4)**: [How a chef profile shows a "live now" indicator and a list of upcoming scheduled sessions. How follower counts and other Part 2 cached profile data stay correct.]

**Content Performance (Req 5)**: [How recipe page loads stay fast even when a heavy live session is happening. How the live media plane and the recipe File Store plane do not contend.]

**High-Performance Optimization (Req 6)**: [How Part 2's caching, async, and horizontal scaling decisions still hold once live sessions are added.]

---

## Requirement 7: LIVE COOKING SESSIONS (60% of Grade)

*Chefs broadcast high-quality live video. Followers watch live with sub-100ms chat. Up to 5,000 concurrent viewers per chef. Sessions auto-save for later viewing. Chefs schedule weekly sessions. Seamless integration with existing recipe and profile systems.*

### Live Streaming Architecture

**Purpose**: Document how the live video itself flows from chef to viewer using building block terminology.

**Building Block Requirements**:
- Use exact building block names. Use `+` for combinations.
- Show the chef's broadcast path and the viewer's playback path as separate flows.
- Identify clearly where External Service handles ingest, transcoding, or edge delivery.

```
Example formats:
Chef Broadcast Start: Chef (User) → Live Service → External Service (live video provider) → Key-Value Store (session state, "live now" flag) → Relational Database (session row)
Viewer Playback: Viewer (User) → Live Service + Key-Value Store (lookup live session) → External Service (edge delivery)
Stream Health: External Service (broadcast events) → Queue + Worker → Key-Value Store (viewer count, latency)
```

**Your Live Streaming Flows**:
[Write 3-5 flows covering broadcast start, viewer join, mid-stream state, and broadcast end.]

### Real-Time Chat Architecture

**Purpose**: Document how chat messages reach viewers in under 100 ms using building block terminology.

```
Example formats:
Send Message: Viewer (User) → Chat Service → Queue (per-session topic) → Worker (fan-out) → Key-Value Store (recent messages buffer)
Receive Message: Viewer (User) → Chat Service (long-lived connection) ← Queue (subscription)
Persist for Replay: Worker → Relational Database (chat log keyed by session)
Moderation: Chat Service → Queue + Worker → External Service (moderation) → Key-Value Store (block list)
```

**Your Chat Flows**:
[Write 3-5 flows covering send, receive, presence, and moderation. Be explicit about which building block holds the recent-messages cache and which handles persistent log.]

### Recording & Playback Architecture

**Purpose**: Document how a live session becomes a permanent, watchable recording.

```
Example formats:
Auto-Save Pipeline: External Service (raw recording) → Queue → Worker (transcode job) → File Store (variants) → Relational Database (recording row)
Replay Request: Viewer (User) → Replay Service + Key-Value Store → File Store
Chat Replay: Viewer (User) → Replay Service → Relational Database (chat log) → Key-Value Store (cache replay messages)
```

**Your Recording Flows**:
[Write 2-4 flows covering capture, post-session processing, and later viewing including chat replay.]

### Scheduling Integration

**Purpose**: Document how a chef schedules a weekly session and how followers get notified.

```
Example formats:
Schedule Session: Chef (User) → Scheduling Service → Relational Database (schedule row, recurrence rule)
Pre-Session Reminder: Time → Worker → Relational Database (find upcoming) → External Service (notification provider) → Followers
Auto Go-Live Window: Time → Worker → Live Service → Key-Value Store (open ingest window)
```

**Your Scheduling Flows**:
[Write 2-4 flows covering creating a schedule, weekly recurrence, follower notifications, and the moment a scheduled session opens.]

### User Flow Design

**Purpose**: Tie the four pieces above together as user-facing journeys.

```
Example formats:
Chef Going Live: Chef (User) → Live Service → External Service → Key-Value Store ("live now") → Queue + Worker → External Service (notify followers)
Follower Joins Mid-Stream: Viewer (User) → Profile Service + Key-Value Store ("live now" flag) → Live Service → External Service (edge playback) + Chat Service (subscribe)
Session Ends and Replays: Live Service → Queue + Worker → File Store → Relational Database (recording row) → Replay Service available to followers
```

**Your User Journeys**:
[Write 3-5 end-to-end journeys that show how the four sub-architectures cooperate.]

### Architecture Decisions & Trade-offs

**Live video plane**: [Why External Service for ingest/transcode/delivery vs. building it in-house. The trade-off you accepted.]

**Chat at sub-100ms**: [Why Queue + Worker + Key-Value Store rather than a synchronous Service-to-database write per message. What latency you actually expect, and why this combination hits 100 ms.]

**Recording pipeline**: [Why Worker + File Store + Queue rather than blocking the live Service on save. What guarantees you give about a recording being available after the session ends.]

**Scheduling and notifications**: [Why Time + Worker + External Service. Why Time is essential here and not optional.]

**Integration vs. isolation**: [How tightly the Live Service couples to recipe/profile Services. What you decoupled deliberately to keep failures contained.]

**What you considered and rejected**: [At least one trade-off. Show that you weighed alternatives.]

### Technical Implementation Details

**Per-block live-session role**:
- **Service**: [Live Service, Chat Service, Replay Service, Scheduling Service. What each owns. Stateless requirements.]
- **Worker**: [Transcoding, fan-out, notification, recording finalization. Idempotency.]
- **Key-Value Store**: [Live-now flag with TTL, viewer counts, recent chat buffer, presence.]
- **File Store**: [Raw recording, transcoded variants, thumbnails. Lifecycle: raw deleted after final variants land.]
- **Queue**: [Per-session chat topic, transcoding job queue, notification fan-out queue. Backpressure behavior.]
- **Relational Database**: [Session rows, schedule rows with recurrence, chat replay log, recording metadata.]
- **External Service**: [Live video provider for ingest/transcode/edge delivery, notification provider, moderation provider.]
- **Time**: [Pre-session reminder, weekly recurrence trigger, scheduled go-live window.]

---

## Overall Architecture Analysis

### Innovation Strategy

[The thesis of your evolution. One paragraph explaining how you added a real-time, video-heavy feature on top of a stable platform without rewriting it.]

### Building Block Evolution from Part 2

[For each block in your Part 2 design, what changed in Part 3. Did Service split into multiple new Services? Did Queue gain a new topic? Did Key-Value Store get a new TTL pattern? Bullet list is fine.]

### Live Streaming Performance Targets

[Quantitative claims tied to the requirements. Sub-100ms chat. 5,000 concurrent viewers per chef. Recording available within X minutes of session end. Notification arrival window. Tie each number to which building blocks deliver it.]

### Trade-offs Made

[At least three trade-offs you accepted. Write each as "We accepted X cost in order to gain Y benefit." At least one should be about live vs. recorded experience. At least one should be about cost (live video is expensive).]

### Innovation Success Metrics

[How you would measure that the live cooking feature actually worked. SLOs. Engagement metrics. Recording availability. Chat latency p95. Concurrent-viewer ceiling without degradation.]

---

## Submission Checklist

Before submitting, verify:

- [ ] Every architecture decision uses **building block names**, not technology names.
- [ ] All 6 prior requirements are still addressed and still working.
- [ ] All 7 sub-bullets of Requirement 7 are covered: high-quality live video, sub-100ms chat, 5,000 concurrent viewers, auto-saved recordings, weekly scheduling, recipe integration, profile integration.
- [ ] External Service is used for the heavy live-video lifting, with a clear reason.
- [ ] Time entity drives scheduled sessions and weekly recurrence.
- [ ] Queue + Worker is used for chat fan-out and recording transcoding.
- [ ] At least three trade-offs are explicitly named.
- [ ] User flows are documented with building block terminology, separated into broadcast / chat / recording / scheduling planes.
- [ ] You can explain *why* each evolution decision was made, not just *what* changed.
