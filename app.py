from flask import Flask, render_template, request
from datetime import datetime
from google import genai
import os  # Strictly using the genai library

app = Flask(__name__)

# --- CONFIGURATION ---
# Using the genai.Client syntax from your working example
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_ai_explanation(data, rules_results):
    """
    The role of Gemini: Explain the rule-based risk percentage and 
    identify discrepancies or reasons for safety.
    """
    prompt = f"""
    Act as a Medical Insurance Auditor. I have a claim with a Fraud Risk Score of {rules_results['score']}%.
    
    CLAIM DATA:
    - Patient: {data.get('name')}
    - Diagnosis: {data.get('diagnosis')}
    - Treatment: {data.get('treatment_type')}
    - Stay: {rules_results['days']} Days
    - Total Cost: ₹{data.get('total_amount')}
    - Documentation: {'Uploaded' if data.get('docs_uploaded') == 'Yes' else 'Missing'}

    RULE VIOLATIONS FOUND:
    {', '.join(rules_results['flags']) if rules_results['flags'] else 'None'}

    TASK:
    1. If risk is > 0%: Explain why these discrepancies (like cost/stay/treatment) suggest fraud.
    2. If risk is 0%: Explain why this claim appears genuine based on medical standards.
    3. Output: A concise, professional 3-4 sentence explanation.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Reasoning Unavailable: {str(e)}"

def analyze_claim(data):
    score = 0
    flags = []
    
    # 1. DATA EXTRACTION & CLEANING
    try:
        clean_val = lambda x: float(data.get(x, '0').replace('₹', '').replace(',', '').strip())
        room_cost = clean_val('room_charges')
        treat_cost = clean_val('treatment_charges')
        meds_cost = clean_val('medicine_charges')
        total_claim = clean_val('total_amount')
        
        d1 = datetime.strptime(data.get('admission_date'), '%Y-%m-%d')
        d2 = datetime.strptime(data.get('discharge_date'), '%Y-%m-%d')
        days = max((d2 - d1).days, 1)
    except:
        return {"score": 100, "flags": ["Invalid Data Format"], "status": "Error", "days": 0}

    # 2. MEDICAL CONSISTENCY CHECK (Clinical Pairing)
    # Mapping diagnoses to their 'Illegal' or 'High Risk' treatments
    mismatches = {
        "Fever": ["Surgery", "ICU Care", "Physiotherapy", "Minor Procedure"],
        "Viral Infection": ["Surgery", "ICU Care", "Physiotherapy"],
        "Sprain": ["ICU Care", "Surgery", "Emergency Intervention"],
        "Kidney Stone": ["Physiotherapy", "Medication" if total_claim > 50000 else None],
        "Appendicitis": ["Physiotherapy", "Medication" if total_claim > 80000 else None]
    }

    diag = data.get('diagnosis')
    treat = data.get('treatment_type')

    if diag in mismatches and treat in mismatches[diag]:
        score += 50  # Heavy penalty for clinical impossibility
        flags.append(f"Clinical Mismatch: {treat} is medically unjustified for {diag}.")

    # 3. BILLING REASONABLENESS (Cost vs. Duration)
    # Penalty for stay duration exceeding medical norms for 'Normal' urgency
    if data.get('urgency') == "Normal":
        if days > 10:
            score += 20
            flags.append(f"Stay Duration Anomaly: {days} days is excessive for a non-emergency {diag}.")
        
        # Check for 'Cost Padding' (High total for basic diagnosis)
        if diag in ["Fever", "Viral Infection", "Sprain"] and total_claim > 50000:
            score += 25
            flags.append(f"Inflation Alert: Claim amount (₹{total_claim:,.0f}) is 3x above regional average for {diag}.")

    # 4. RATIO ANALYSIS (Internal Cost Logic)
    # Room rent should not realistically be < 5% of a massive 1 Lakh claim (indicates fake billing)
    if total_claim > 80000 and (room_cost / total_claim) < 0.10:
        score += 15
        flags.append("Financial Discrepancy: Disproportionately low room charges vs total claim suggests 'padding' in other areas.")

    # 5. DOCUMENTATION CHECK
    if data.get('docs_uploaded') == "No":
        score += 30
        flags.append("High Risk: Mandatory medical reports missing for a high-value claim.")

    # FINAL STATUS MAPPING
    score = min(score, 100)
    status = "GENUINE" if score < 25 else "FLAGGED FOR REVIEW" if score < 65 else "HIGH RISK"
    
    results = {"score": score, "flags": flags, "status": status, "days": days}
    results["ai_insight"] = get_ai_explanation(data, results)
    
    return results
 
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/apply")
def apply():
    return render_template("form.html")

@app.route('/process_claim', methods=['POST'])
def process():
    data = request.form
    result = analyze_claim(data)
    return render_template('result.html', result=result, data=data)

if __name__ == "__main__":
    app.run(debug=True)