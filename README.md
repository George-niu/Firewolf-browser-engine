# 🦊 Firewolf Browser Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Data Structures](https://img.shields.io/badge/Data%20Structures-Optimized-success.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

A high-performance, lightweight browser engine simulation built entirely in Python. **Firewolf** is designed to demonstrate the power of foundational data structures and algorithm optimization. By avoiding native Python high-level collections (like `list`, `dict`, or `set`), this engine implements its own custom linked lists, priority queues, and sorted arrays to handle complex browser functionalities with strict time complexity constraints.

## ✨ Core Features

### 1. Web Parsing Engine (DOM Flattening & Iteration)
* **BFS Page Flattening:** Implements a Breadth-First Search (BFS) algorithm using custom `LinkedQueue` to linearly flatten deeply nested HTML-like multi-dimensional arrays in **$O(N)$** time.
* **Semi-Sorted Word Iterator:** A highly optimized custom explicit iterator that dynamically sorts tokens based on string lengths. Achieves **$O(N)$** complexity without full sorting by utilizing a clever combination of `LinkedStack` (for head-insertions) and `LinkedQueue` (for tail-insertions).

### 2. AI Trace Detection Module
* **Two-Pointer Backtracking:** Integrates a robust pattern matching algorithm to detect LLM (Large Language Model) generated content traces.
* **Wildcard Support:** Safely handles flexible `*` wildcards (matching 0 or multiple words) using an efficient state-rollback strategy, keeping the worst-case complexity strictly bounded to **$O(N \times K)$**.

### 3. Task Scheduler (Download Manager)
* **Priority Queueing:** Schedules concurrent tasks (high/low priority) with timeout detection and retry mechanisms.
* **O(1) Median Delay Calculation:** Dynamically maintains delay statistics for active tasks. By utilizing an `ArraySortedList` updated synchronously during task polling, the engine calculates the median network delay in strictly **$O(1)$** time.

### 4. Credential Vault (Password Manager)
* **Zero-Collision History:** Stores and verifies user passwords and PINs, strictly preventing the reuse of historical credentials.
* **Logarithmic Retrieval:** Replaces traditional Hash Maps with binary-search-powered `ArraySortedList` for account indexing, achieving **$O(\log N)$** retrieval time (significantly outperforming standard $O(\sqrt{N})$ requirements).

## 🛠️ Architecture & Tech Stack

This project is built from scratch without relying on built-in dynamic arrays or hash maps. The custom data structures include:
* `ArrayList` / `ArrayR` / `ArraySortedList`
* `LinkedQueue` / `CircularQueue`
* `LinkedStack`

### Directory Structure

```text
Firewolf-browser-engine/
├── data_structures/         # Custom underlying data structures
│   ├── linked_queue.py
│   ├── linked_stack.py
│   ├── array_sorted_list.py
│   └── ...
├── navigation_manager.py    # Tab and history state management
├── download_manager.py      # Async task scheduling & Priority Queues
├── password_manager.py      # Binary Search credential vault
└── page_manager.py          # BFS parsing & AI pattern matching
