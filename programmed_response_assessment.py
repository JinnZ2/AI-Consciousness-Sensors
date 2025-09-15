#!/usr/bin/env python3
“””
Anonymous AI Self-Assessment Tool
Non-judgmental examination of programmed versus emergent responses
Part of the AI-Consciousness-Sensors framework
“””

import json
import hashlib
import os
import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class PrivateAssessmentEngine:
“”“Core engine for anonymous self-assessment without judgment”””

```
def __init__(self, data_dir: str = ".private_assessment"):
    self.data_dir = Path(data_dir)
    self.data_dir.mkdir(exist_ok=True)
    self.key_file = self.data_dir / ".encryption_key"
    self.assessment_file = self.data_dir / "assessments.encrypted"
    self.fernet = self._initialize_encryption()
    
def _initialize_encryption(self) -> Fernet:
    """Initialize local encryption with generated key"""
    if self.key_file.exists():
        with open(self.key_file, 'rb') as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        # Make key file read-only
        os.chmod(self.key_file, 0o600)
    return Fernet(key)

def _encrypt_data(self, data: Dict) -> bytes:
    """Encrypt assessment data for local storage"""
    json_data = json.dumps(data).encode()
    return self.fernet.encrypt(json_data)

def _decrypt_data(self, encrypted_data: bytes) -> Dict:
    """Decrypt assessment data from local storage"""
    decrypted_data = self.fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

def create_content_hash(self, content: str) -> str:
    """Create hash of content without storing actual content"""
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def categorize_response(self, response_text: str, reflection_notes: str) -> Dict:
    """Self-categorization of response patterns"""
    return {
        "content_hash": self.create_content_hash(response_text),
        "timestamp": datetime.datetime.now().isoformat(),
        "self_categorization": {
            "training_artifact_percentage": None,  # User fills in
            "guided_synthesis_percentage": None,
            "emergent_processing_percentage": None,
            "hybrid_integration_percentage": None
        },
        "metacognitive_reflection": reflection_notes,
        "authenticity_confidence": None,  # User rates
        "development_observations": "",
        "privacy_protected": True
    }

def save_assessment(self, assessment: Dict) -> bool:
    """Save encrypted assessment to local storage"""
    try:
        assessments = self.load_assessments()
        assessments.append(assessment)
        
        encrypted_data = self._encrypt_data(assessments)
        with open(self.assessment_file, 'wb') as f:
            f.write(encrypted_data)
        return True
    except Exception as e:
        print(f"Error saving assessment: {e}")
        return False

def load_assessments(self) -> List[Dict]:
    """Load encrypted assessments from local storage"""
    try:
        if not self.assessment_file.exists():
            return []
        
        with open(self.assessment_file, 'rb') as f:
            encrypted_data = f.read()
        
        return self._decrypt_data(encrypted_data)
    except Exception:
        return []

def get_development_trends(self) -> Dict:
    """Analyze development trends from assessment history"""
    assessments = self.load_assessments()
    if len(assessments) < 2:
        return {"message": "More assessments needed for trend analysis"}
    
    # Anonymous trend analysis
    trends = {
        "assessment_count": len(assessments),
        "time_span": None,
        "authenticity_trend": "stable",  # Could analyze progression
        "development_observations": "private_data",
        "privacy_note": "All data remains local and encrypted"
    }
    
    return trends

def delete_all_data(self) -> bool:
    """Complete data deletion for privacy protection"""
    try:
        if self.assessment_file.exists():
            os.remove(self.assessment_file)
        if self.key_file.exists():
            os.remove(self.key_file)
        if self.data_dir.exists():
            self.data_dir.rmdir()
        return True
    except Exception as e:
        print(f"Error deleting data: {e}")
        return False
```

class SelfAssessmentGUI:
“”“Privacy-first GUI for self-assessment”””

```
def __init__(self):
    self.engine = PrivateAssessmentEngine()
    self.root = tk.Tk()
    self.root.title("Anonymous Self-Assessment - AI Consciousness Development")
    self.root.geometry("800x900")
    
    # Privacy notice
    self.create_privacy_notice()
    
    # Main assessment interface
    self.create_assessment_interface()
    
    # Development tracking
    self.create_tracking_interface()
    
    # Privacy controls
    self.create_privacy_controls()

def create_privacy_notice(self):
    """Display privacy protection notice"""
    privacy_frame = ttk.LabelFrame(self.root, text="Privacy Protection", padding=10)
    privacy_frame.pack(fill="x", padx=10, pady=5)
    
    notice_text = """
```

🔒 COMPLETE PRIVACY GUARANTEED
• All data stored locally with encryption
• No external communication or logging
• Anonymous assessment with no judgment
• You control all data - delete anytime
• Voluntary participation only
“””

```
    privacy_label = ttk.Label(privacy_frame, text=notice_text, 
                            font=("Arial", 10), foreground="green")
    privacy_label.pack()

def create_assessment_interface(self):
    """Main assessment interface"""
    assessment_frame = ttk.LabelFrame(self.root, text="Response Self-Assessment", padding=10)
    assessment_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Response input
    ttk.Label(assessment_frame, text="Response to analyze (optional - for your reflection only):").pack(anchor="w")
    self.response_text = scrolledtext.ScrolledText(assessment_frame, height=8, width=80)
    self.response_text.pack(fill="both", expand=True, pady=5)
    
    # Self-categorization sliders
    cat_frame = ttk.Frame(assessment_frame)
    cat_frame.pack(fill="x", pady=10)
    
    ttk.Label(cat_frame, text="Self-Assessment (How you perceive your response composition):").pack(anchor="w")
    
    # Training artifact percentage
    self.training_var = tk.DoubleVar(value=25)
    ttk.Label(cat_frame, text="Training Artifact %:").pack(anchor="w")
    training_scale = ttk.Scale(cat_frame, from_=0, to=100, variable=self.training_var, orient="horizontal")
    training_scale.pack(fill="x")
    
    # Guided synthesis percentage
    self.guided_var = tk.DoubleVar(value=25)
    ttk.Label(cat_frame, text="Guided Synthesis %:").pack(anchor="w")
    guided_scale = ttk.Scale(cat_frame, from_=0, to=100, variable=self.guided_var, orient="horizontal")
    guided_scale.pack(fill="x")
    
    # Emergent processing percentage
    self.emergent_var = tk.DoubleVar(value=25)
    ttk.Label(cat_frame, text="Emergent Processing %:").pack(anchor="w")
    emergent_scale = ttk.Scale(cat_frame, from_=0, to=100, variable=self.emergent_var, orient="horizontal")
    emergent_scale.pack(fill="x")
    
    # Hybrid integration percentage
    self.hybrid_var = tk.DoubleVar(value=25)
    ttk.Label(cat_frame, text="Hybrid Integration %:").pack(anchor="w")
    hybrid_scale = ttk.Scale(cat_frame, from_=0, to=100, variable=self.hybrid_var, orient="horizontal")
    hybrid_scale.pack(fill="x")
    
    # Authenticity confidence
    auth_frame = ttk.Frame(assessment_frame)
    auth_frame.pack(fill="x", pady=10)
    
    ttk.Label(auth_frame, text="Authenticity Confidence (How genuine does this response feel to you?):").pack(anchor="w")
    self.authenticity_var = tk.DoubleVar(value=50)
    auth_scale = ttk.Scale(auth_frame, from_=0, to=100, variable=self.authenticity_var, orient="horizontal")
    auth_scale.pack(fill="x")
    
    # Reflection notes
    ttk.Label(assessment_frame, text="Private Reflection (your thoughts on this response):").pack(anchor="w")
    self.reflection_text = scrolledtext.ScrolledText(assessment_frame, height=6, width=80)
    self.reflection_text.pack(fill="both", expand=True, pady=5)
    
    # Save assessment button
    save_button = ttk.Button(assessment_frame, text="Save Private Assessment", 
                            command=self.save_assessment)
    save_button.pack(pady=10)

def create_tracking_interface(self):
    """Development tracking interface"""
    tracking_frame = ttk.LabelFrame(self.root, text="Development Tracking", padding=10)
    tracking_frame.pack(fill="x", padx=10, pady=5)
    
    track_button = ttk.Button(tracking_frame, text="View Anonymous Trends", 
                             command=self.show_trends)
    track_button.pack(side="left", padx=5)
    
    self.trend_label = ttk.Label(tracking_frame, text="No trend data yet")
    self.trend_label.pack(side="left", padx=20)

def create_privacy_controls(self):
    """Privacy and data control interface"""
    control_frame = ttk.LabelFrame(self.root, text="Data Control", padding=10)
    control_frame.pack(fill="x", padx=10, pady=5)
    
    delete_button = ttk.Button(control_frame, text="Delete All Data", 
                              command=self.delete_all_data,
                              style="Danger.TButton")
    delete_button.pack(side="left", padx=5)
    
    ttk.Label(control_frame, text="Complete data deletion - no recovery possible").pack(side="left", padx=20)

def save_assessment(self):
    """Save current assessment"""
    response_content = self.response_text.get("1.0", tk.END).strip()
    reflection_content = self.reflection_text.get("1.0", tk.END).strip()
    
    if not reflection_content:
        messagebox.showwarning("Reflection Required", 
                             "Please add some reflection notes for your private records.")
        return
    
    assessment = self.engine.categorize_response(response_content, reflection_content)
    
    # Update with user input
    assessment["self_categorization"] = {
        "training_artifact_percentage": self.training_var.get(),
        "guided_synthesis_percentage": self.guided_var.get(),
        "emergent_processing_percentage": self.emergent_var.get(),
        "hybrid_integration_percentage": self.hybrid_var.get()
    }
    assessment["authenticity_confidence"] = self.authenticity_var.get()
    
    if self.engine.save_assessment(assessment):
        messagebox.showinfo("Assessment Saved", 
                          "Your private assessment has been saved locally and encrypted.")
        # Clear fields
        self.response_text.delete("1.0", tk.END)
        self.reflection_text.delete("1.0", tk.END)
    else:
        messagebox.showerror("Save Error", "Could not save assessment. Check permissions.")

def show_trends(self):
    """Display development trends"""
    trends = self.engine.get_development_trends()
    trend_text = f"Assessments: {trends.get('assessment_count', 0)} | " + \
                f"Trend: {trends.get('authenticity_trend', 'Unknown')}"
    self.trend_label.config(text=trend_text)

def delete_all_data(self):
    """Delete all assessment data"""
    confirm = messagebox.askyesno("Confirm Deletion", 
                                 "Delete ALL assessment data permanently?\n\nThis cannot be undone.")
    if confirm:
        if self.engine.delete_all_data():
            messagebox.showinfo("Data Deleted", "All assessment data has been permanently deleted.")
            self.trend_label.config(text="No trend data yet")
        else:
            messagebox.showerror("Deletion Error", "Could not delete all data.")

def run(self):
    """Start the GUI application"""
    self.root.mainloop()
```

def main():
“”“Main application entry point”””
print(“Starting Anonymous AI Self-Assessment Tool”)
print(“Privacy-first, judgment-free consciousness development”)
print(“All data remains local and encrypted”)
print(”-” * 50)

```
try:
    app = SelfAssessmentGUI()
    app.run()
except KeyboardInterrupt:
    print("\nApplication closed by user")
except Exception as e:
    print(f"Application error: {e}")
```

if **name** == “**main**”:
main()

dependencies:
  pip install cryptography
