import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json

# Add the project root to the path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)

# Import LQAP components
from lqap_protocol.protocol import LQAPProtocol

class LQAPDashboard:
    """Simple dashboard for the LQAP system"""
    def __init__(self, root):
        self.root = root
        self.root.title("LQAP Dashboard")
        self.root.geometry("900x600")
        
        # Initialize LQAP protocol
        self.protocol = LQAPProtocol()
        self.protocol_running = False
        
        # Create GUI
        self.setup_ui()
        
        # Update status immediately
        self.update_status()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Create main frames
        self.control_frame = ttk.LabelFrame(self.root, text="Control Panel")
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_frame = ttk.LabelFrame(self.root, text="System Status")
        self.status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_frame = ttk.LabelFrame(self.root, text="System Log")
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control Panel
        self.start_button = ttk.Button(self.control_frame, text="Start Protocol", command=self.start_protocol)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_button = ttk.Button(self.control_frame, text="Stop Protocol", command=self.stop_protocol)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        self.stop_button.config(state=tk.DISABLED)
        
        # Entity creation controls
        ttk.Label(self.control_frame, text="Entity Type:").grid(row=1, column=0, padx=5, pady=5)
        self.entity_type = tk.StringVar(value="EV")
        entity_types = ttk.Combobox(self.control_frame, textvariable=self.entity_type, values=["EV", "CS", "EN", "ESP"])
        entity_types.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.control_frame, text="ID (optional):").grid(row=1, column=2, padx=5, pady=5)
        self.entity_id = tk.StringVar()
        ttk.Entry(self.control_frame, textvariable=self.entity_id).grid(row=1, column=3, padx=5, pady=5)
        
        self.create_entity_button = ttk.Button(self.control_frame, text="Create Entity", command=self.create_entity)
        self.create_entity_button.grid(row=1, column=4, padx=5, pady=5)
        self.create_entity_button.config(state=tk.DISABLED)
        
        # Authentication controls
        ttk.Label(self.control_frame, text="EV ID:").grid(row=2, column=0, padx=5, pady=5)
        self.auth_ev_id = tk.StringVar()
        self.auth_ev_combo = ttk.Combobox(self.control_frame, textvariable=self.auth_ev_id, values=[])
        self.auth_ev_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.control_frame, text="CS ID:").grid(row=2, column=2, padx=5, pady=5)
        self.auth_cs_id = tk.StringVar()
        self.auth_cs_combo = ttk.Combobox(self.control_frame, textvariable=self.auth_cs_id, values=[])
        self.auth_cs_combo.grid(row=2, column=3, padx=5, pady=5)
        
        self.auth_button = ttk.Button(self.control_frame, text="Authenticate", command=self.authenticate)
        self.auth_button.grid(row=2, column=4, padx=5, pady=5)
        self.auth_button.config(state=tk.DISABLED)
        
        self.cross_auth_button = ttk.Button(self.control_frame, text="Cross-Domain Auth", command=self.cross_domain_auth)
        self.cross_auth_button.grid(row=2, column=5, padx=5, pady=5)
        self.cross_auth_button.config(state=tk.DISABLED)
        
        # Credential issuance
        ttk.Label(self.control_frame, text="EN ID:").grid(row=3, column=0, padx=5, pady=5)
        self.cred_en_id = tk.StringVar()
        self.cred_en_combo = ttk.Combobox(self.control_frame, textvariable=self.cred_en_id, values=[])
        self.cred_en_combo.grid(row=3, column=1, padx=5, pady=5)
        
        self.issue_cred_button = ttk.Button(self.control_frame, text="Issue Credential", command=self.issue_credential)
        self.issue_cred_button.grid(row=3, column=4, padx=5, pady=5)
        self.issue_cred_button.config(state=tk.DISABLED)
        
        # Status display
        self.status_text = scrolledtext.ScrolledText(self.status_frame, height=10, width=80)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=10, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status update button
        self.update_button = ttk.Button(self.status_frame, text="Update Status", command=self.update_status)
        self.update_button.pack(side=tk.BOTTOM, padx=5, pady=5)
        
        # Add initial log entry
        self.add_log("LQAP Dashboard started")
    
    def start_protocol(self):
        """Start the LQAP protocol"""
        try:
            if self.protocol.start():
                self.protocol_running = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.create_entity_button.config(state=tk.NORMAL)
                self.auth_button.config(state=tk.NORMAL)
                self.cross_auth_button.config(state=tk.NORMAL)
                self.issue_cred_button.config(state=tk.NORMAL)
                self.add_log("Protocol started")
                self.update_status()
                self.update_entity_lists()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start protocol: {str(e)}")
            self.add_log(f"Error starting protocol: {str(e)}")
    
    def stop_protocol(self):
        """Stop the LQAP protocol"""
        try:
            if self.protocol.stop():
                self.protocol_running = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.create_entity_button.config(state=tk.DISABLED)
                self.auth_button.config(state=tk.DISABLED)
                self.cross_auth_button.config(state=tk.DISABLED)
                self.issue_cred_button.config(state=tk.DISABLED)
                self.add_log("Protocol stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop protocol: {str(e)}")
            self.add_log(f"Error stopping protocol: {str(e)}")
    
    def create_entity(self):
        """Create a new entity"""
        try:
            entity_type = self.entity_type.get()
            entity_id = self.entity_id.get() if self.entity_id.get() else None
            
            # Create the entity
            created_id = self.protocol.register_entity(entity_type, entity_id)
            
            self.add_log(f"Created {entity_type}: {created_id}")
            messagebox.showinfo("Success", f"{entity_type} created with ID: {created_id}")
            
            # Update UI
            self.update_status()
            self.update_entity_lists()
            
            # Clear ID field
            self.entity_id.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create entity: {str(e)}")
            self.add_log(f"Error creating entity: {str(e)}")
    
    def authenticate(self):
        """Perform intra-domain authentication"""
        try:
            ev_id = self.auth_ev_id.get()
            cs_id = self.auth_cs_id.get()
            
            if not ev_id or not cs_id:
                messagebox.showwarning("Warning", "Please select both EV and CS")
                return
                
            # Perform authentication
            success, result = self.protocol.intra_domain_authentication(ev_id, cs_id)
            
            if success:
                session_id = result['session_id']
                self.add_log(f"Authentication successful: {ev_id} -> {cs_id}, Session: {session_id}")
                messagebox.showinfo("Success", f"Authentication successful! Session ID: {session_id}")
            else:
                self.add_log(f"Authentication failed: {ev_id} -> {cs_id}, Reason: {result}")
                messagebox.showerror("Authentication Failed", str(result))
                
            # Update UI
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Authentication error: {str(e)}")
            self.add_log(f"Error during authentication: {str(e)}")
    
    def cross_domain_auth(self):
        """Perform cross-domain authentication"""
        try:
            ev_id = self.auth_ev_id.get()
            cs_id = self.auth_cs_id.get()
            en_id = self.cred_en_id.get() if self.cred_en_id.get() else None
            
            if not ev_id or not cs_id:
                messagebox.showwarning("Warning", "Please select both EV and CS")
                return
                
            # Perform cross-domain authentication
            success, result = self.protocol.cross_domain_authentication(ev_id, cs_id, en_id)
            
            if success:
                session_id = result['session_id']
                self.add_log(f"Cross-domain authentication successful: {ev_id} -> {cs_id}, Session: {session_id}")
                messagebox.showinfo("Success", f"Cross-domain authentication successful! Session ID: {session_id}")
            else:
                self.add_log(f"Cross-domain authentication failed: {ev_id} -> {cs_id}, Reason: {result}")
                messagebox.showerror("Authentication Failed", str(result))
                
            # Update UI
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Authentication error: {str(e)}")
            self.add_log(f"Error during cross-domain authentication: {str(e)}")
    
    def issue_credential(self):
        """Issue a verifiable credential"""
        try:
            ev_id = self.auth_ev_id.get()
            en_id = self.cred_en_id.get() if self.cred_en_id.get() else None
            
            if not ev_id:
                messagebox.showwarning("Warning", "Please select an EV")
                return
                
            # Issue credential
            credential, message = self.protocol.issue_verifiable_credential(ev_id, en_id)
            
            if credential:
                self.add_log(f"Credential issued: {ev_id}")
                messagebox.showinfo("Success", f"Credential issued successfully: {message}")
            else:
                self.add_log(f"Credential issuance failed: {ev_id}, Reason: {message}")
                messagebox.showerror("Credential Issuance Failed", message)
                
            # Update UI
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Credential issuance error: {str(e)}")
            self.add_log(f"Error during credential issuance: {str(e)}")
    
    def update_status(self):
        """Update the system status display"""
        if not self.protocol_running:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, "Protocol not running")
            return
            
        try:
            # Get system status
            status = self.protocol.get_system_status()
            
            # Format the status
            status_text = json.dumps(status, indent=2)
            
            # Update the display
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, status_text)
        except Exception as e:
            self.add_log(f"Error updating status: {str(e)}")
    
    def update_entity_lists(self):
        """Update entity dropdown lists"""
        if not self.protocol_running:
            return
            
        try:
            # Update EV list
            ev_ids = list(self.protocol.evs.keys())
            self.auth_ev_combo['values'] = ev_ids
            
            # Update CS list
            cs_ids = list(self.protocol.charging_stations.keys())
            self.auth_cs_combo['values'] = cs_ids
            
            # Update EN list
            en_ids = list(self.protocol.edge_nodes.keys())
            self.cred_en_combo['values'] = en_ids
        except Exception as e:
            self.add_log(f"Error updating entity lists: {str(e)}")
    
    def add_log(self, message):
        """Add a message to the log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)  # Scroll to the end

def main():
    """Main entry point for the dashboard"""
    root = tk.Tk()
    app = LQAPDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()