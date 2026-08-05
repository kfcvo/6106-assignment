# ChainBank — Blockchain Banking System

> A Flask-based web application that integrates Ethereum smart contracts to simulate a secure banking management system with on-chain transfer and deposit capabilities.

---

## Overview

**ChainBank** is a full-stack blockchain banking application built as an academic assignment (course 6106). It combines a traditional Flask web server with Ethereum smart contracts, allowing users to log in, navigate a banking dashboard, and perform real on-chain transactions — including money transfers and deposits — through their browser wallet (e.g. MetaMask).

The system also maintains an off-chain audit log in SQLite, recording every user login with a timestamp for security tracking.

---

## Features

| Feature | Description |
|---|---|
| User Login | Users enter a username to log in; each login is recorded in a SQLite database with a timestamp. |
| Banking Dashboard | A sidebar-based dashboard providing navigation to all banking features. |
| Transfer Money | Perform on-chain ETH transfers between payer and payee addresses via a Solidity smart contract. |
| Deposit Money | Deposit funds on-chain to a customer address via a separate smart contract. |
| View Transaction | Query the last recorded transfer/deposit from the smart contract. |
| View Logs | Audit user login history stored in the local SQLite database. |
| Clear Logs | Admin function to wipe all login logs from the database. |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Flask (Python) |
| Database | SQLite |
| Blockchain Interaction | Web3.js (v1.5.2) |
| Smart Contracts | Solidity (Ethereum) |
| Frontend | HTML5, CSS3, Jinja2 Templates |
| WSGI Server | Gunicorn |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Browser (Client)                   │
│                                                       │
│   ┌───────────┐  ┌───────────┐  ┌───────────────┐  │
│   │  Login     │  │ Dashboard │  │ Transfer/     │  │
│   │  Page      │  │  (Main)   │  │ Deposit Page  │  │
│   └─────┬─────┘  └─────┬─────┘  └───────┬───────┘  │
│         │              │                 │            │
│         │   MetaMask   │        Web3.js  │            │
│         │   (wallet)   │     (blockchain RPC)        │
└─────────┼──────────────┼─────────────────┼──────────┘
          │              │                 │
          ▼              ▼                 ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────────┐
│   Flask     │  │   SQLite    │  │   Ethereum       │
│  Web Server │  │  (user.db)  │  │  Smart Contracts  │
│  (app.py)   │  │             │  │                   │
└─────────────┘  └─────────────┘  └─────────────────┘
```

- **Flask** serves all web pages and handles login logging.
- **SQLite** stores login audit records (username + timestamp).
- **Web3.js** runs entirely client-side, connecting the user's browser wallet (MetaMask) directly to deployed smart contracts on the Ethereum blockchain.

---

## Smart Contracts

The application interacts with two deployed Solidity smart contracts:

### 1. Transfer Contract

- **Address:** `0xAaA94E5c4A283B5f9D4689fac6C5042D4CB2dEe5`
- **Functions:**

| Function | Type | Parameters | Description |
|---|---|---|---|
| `transfer_money` | `nonpayable` | `address payer, address payee, uint256 amount` | Execute a transfer between two addresses |
| `check_transaction` | `view` | none | Returns the last transfer's payer, payee, and amount |

### 2. Deposit Contract

- **Address:** `0x1efdf55131c1ce2a2a5b25f54280b75d51b95555`
- **Functions:**

| Function | Type | Parameters | Description |
|---|---|---|---|
| `deposit_money` | `nonpayable` | `address customer, uint256 amount` | Deposit funds to a customer address |
| `deposit_view` | `view` | none | Returns the last deposit's depositor address and amount |

---

## Project Structure

```
6106-assignment/
├── app.py                 # Flask application (routes, SQLite logic)
├── requirements.txt       # Python dependencies
├── user.db                # SQLite database (login audit log)
├── static/
│   └── styles.css         # Shared CSS styles
├── templates/
│   ├── index.html         # Login page (username input)
│   ├── main.html         # Banking dashboard (sidebar navigation)
│   ├── paynow.html        # Transfer money page (Web3.js + smart contract)
│   ├── deposit.html       # Deposit money page (Web3.js + smart contract)
│   └── result.html        # Generic result page (logs view, notifications)
└── .vscode/               # VS Code workspace settings
```

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- [MetaMask](https://metamask.io/) browser extension (or any Web3-compatible wallet)
- An Ethereum wallet funded with test ETH (use a testnet like Sepolia or Goerli)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/kfcvo/6106-assignment.git
   cd 6106-assignment
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Flask application**

   ```bash
   python app.py
   # or for production:
   # gunicorn app:app
   ```

4. **Open the application**

   Navigate to `http://127.0.0.1:5000` in your browser.

5. **Connect your wallet**

   Ensure MetaMask is installed and connected to the same network where the smart contracts are deployed. The Transfer and Deposit pages require wallet interaction to execute on-chain transactions.

---

## Application Flow

```
[Login] ──► [Dashboard] ──┬──► [Transfer] ──► Smart Contract ──► On-chain Tx
                          ├──► [Deposit]  ──► Smart Contract ──► On-chain Tx
                          ├──► [View Logs] ──► SQLite Query
                          └──► [Clear Logs] ──► SQLite Delete
```

1. User enters a username on the login page → Flask records it in SQLite with a timestamp.
2. User arrives at the banking dashboard with a sidebar navigation.
3. User can:
   - **Transfer** — enter payer address, payee address, and amount → confirm via MetaMask → on-chain transaction executes.
   - **Deposit** — enter depositor address and amount → confirm via MetaMask → on-chain transaction executes.
   - **View Logs** — see all recorded login entries.
   - **Clear Logs** — wipe the login database.
4. User can log out to return to the login page.

---

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET, POST | Login page — prompts for username |
| `/main` | GET, POST | Banking dashboard — sidebar navigation |
| `/paynow` | GET, POST | Transfer money page (on-chain) |
| `/deposit` | GET, POST | Deposit money page (on-chain) |
| `/userlog` | GET, POST | View all login audit logs |
| `/deleteuserlog` | GET, POST | Clear all login audit logs |

---

## Dependencies

```
gunicorn      # Production WSGI HTTP Server
flask         # Web framework
pysqlite3     # SQLite driver (Python)
```

> Web3.js is loaded via CDN (`https://cdn.jsdelivr.net/npm/web3@1.5.2/dist/web3.min.js`) on the client side — no npm installation required.

---

## Notes

- The smart contract addresses are hardcoded in `paynow.html` and `deposit.html`. If the contracts are redeployed, update the `contractAddress` constant in both files.
- The SQLite database (`user.db`) is created automatically on first run via `CREATE TABLE IF NOT EXISTS`.
- A global `flag` variable in `app.py` prevents duplicate login records from repeated `/main` access.
- This project is an academic assignment and is **not** intended for production use. Smart contract security, authentication, and error handling are minimal by design.


