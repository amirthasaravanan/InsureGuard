# 🛡️ InsureGuard: AI-Powered Fraud Insurance Claim Detection Engine

- **InsureGuard** is a insurance claim analysis platform designed to detect medical insurance fraud in real-time. 

- By combining a Deterministic Engine with the reasoning capabilities of Generative AI, it helps auditors identify the inconsistencies instantly.
## 👨‍💼 Targeted User: The Claims Auditor
Unlike patient-facing portals, **InsureGuard** is a specialized internal tool designed for **Insurance Claims Officers** and **Analysts**. 

### The Workflow:
1. **Physical Review**: The analyst receives a formal insurance claim application (the hard copy or digital PDF).
2. **Data Extraction**: The analyst identifies key parameters—such as diagnosis codes, specific treatments, hospitalization dates, and exact billing figures.
3. **System Entry**: These verified parameters are entered into the InsureGuard portal.
4. **Instant Audit**: The system processes the manual input to provide an immediate risk assessment, allowing the officer to approve genuine claims faster or investigate flagged frauds with AI-backed reasoning.

## ⚖️ Strategic Design: Why Deterministic Engine for Prediction?

A key architectural decision in **InsureGuard** is the separation of **Prediction** and **Explanation**:

* **Non-Generative Prediction**: We do **not** use Generative AI (LLMs) to determine the fraud risk score or decide the claim's status.
* **Accuracy & Reliability**: Generative AI can occasionally suffer from "hallucinations" or inconsistent reasoning, which is unacceptable when dealing with financial payouts and people's health coverage. 
* **Fairness for Genuine Claimants**: To protect honest users from being wrongly flagged by a "black box" algorithm, all fraud detection is handled by a transparent, **Deterministic Engine**.
* **The Role of Generative AI**: Generative AI is used strictly for **Audit Assistance**—it interprets the *already detected* values and uses the input parameters to provide a human-readable, point-by-point clinical explanation stating why an application is detected as fraud claim or genuine claim for the analyst.

## 🚀 Features
* **Hybrid Risk Scoring**: Uses a weighted logic engine to calculate fraud probability along with percentage risk
* **Clinical Reasoning**: Integrated with **Gemini 1.5 Flash** to provide point-by-point explanations of discrepancies present in the report.
* **Automated Audit**: Instantly flags issues like duration-treatment mismatches and financial anomalies.
* **Modern Interface**: A clean, responsive UI built with Tailwind CSS for high-speed auditing workflows.

## 🛠️ Tech Stack
* **Backend**: Python / Flask
* **AI**: Google Gemini AI (genai SDK)
* **Frontend**: HTML5, Tailwind CSS, JavaScript
* **Deployment**: Render

## 📋 Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/amirthasaravanan/InsureGuard.git](https://github.com/amirthasaravanan/InsureGuard.git)
   cd InsureGuard
