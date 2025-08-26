import customtkinter as ctk

class GuardioDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.appearance_mode = "dark"
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("blue")
        
        self.title("Guardio — Adaptive Anomaly Detection")
        self.geometry("1200x720")
        self.minsize(1100, 650)
        
        self.colors = {
            "dark": {
                "primary": "#0D1117",
                "secondary": "#161B22",
                "surface": "#21262D",
                "accent": "#1F6FEB",
                "success": "#238636",
                "warning": "#D29922",
                "danger": "#DA3633",
                "text": "#F0F6FC",
                "text_secondary": "#8B949E",
                "border": "#30363D",
                "disabled": "#484F58"
            },
            "light": {
                "primary": "#FFFFFF",
                "secondary": "#F6F8FA",
                "surface": "#FFFFFF",
                "accent": "#0969DA",
                "success": "#1A7F37",
                "warning": "#BF8700",
                "danger": "#CF222E",
                "text": "#24292F",
                "text_secondary": "#656D76",
                "border": "#D0D7DE",
                "disabled": "#8C959F"
            }
        }
        
        self.typography = {
            "display": ("Arial", 28, "bold"),
            "headline": ("Arial", 20, "bold"),
            "title": ("Arial", 18, "bold"),
            "body_large": ("Arial", 16, "normal"),
            "body": ("Arial", 14, "normal"),
            "body_bold": ("Arial", 14, "bold"),
            "caption": ("Arial", 12, "normal"),
            "button": ("Arial", 14, "bold"),
            "monospace": ("Courier New", 11, "normal")
        }
        
        self.current_colors = self.colors[self.appearance_mode]
        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        """Build Samsung One UI interface"""
        
        # Header
        self.header = ctk.CTkFrame(self, corner_radius=16, height=85)
        self.header.pack(fill="x", padx=24, pady=24)
        self.header.pack_propagate(False)

        header_content = ctk.CTkFrame(self.header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=32, pady=18)

        # Title section
        title_section = ctk.CTkFrame(header_content, fg_color="transparent")
        title_section.pack(side="left", fill="y")

        self.title_label = ctk.CTkLabel(
            title_section,
            text="Guardio",
            font=self.typography["display"]
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            title_section,
            text="Adaptive Anomaly Detection System",
            font=self.typography["body_large"]
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        # Theme toggle
        self.theme_toggle = ctk.CTkSwitch(
            header_content,
            text="Dark Theme",
            command=self.toggle_theme,
            font=self.typography["body_bold"],
            width=130,
            height=32
        )
        self.theme_toggle.pack(side="right", anchor="e", pady=16)
        self.theme_toggle.select()

        # Control panel
        self.control_panel = ctk.CTkFrame(self, corner_radius=16)
        self.control_panel.pack(fill="x", padx=24, pady=(0, 24))

        control_content = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        control_content.pack(fill="x", padx=32, pady=24)

        # Status section
        status_section = ctk.CTkFrame(control_content, fg_color="transparent")
        status_section.pack(side="left")

        ctk.CTkLabel(
            status_section,
            text="System Status",
            font=self.typography["body_bold"]
        ).pack(anchor="w")

        self.status_indicator = ctk.CTkLabel(
            status_section,
            text="STOPPED",
            font=self.typography["button"],
            corner_radius=8,
            width=140,
            height=36
        )
        self.status_indicator.pack(anchor="w", pady=(6, 0))

        # Controls section
        controls_section = ctk.CTkFrame(control_content, fg_color="transparent")
        controls_section.pack(side="right", fill="x", expand=True, padx=(48, 0))

        # Sensitivity control
        sensitivity_row = ctk.CTkFrame(controls_section, fg_color="transparent")
        sensitivity_row.pack(fill="x", pady=(0, 16))

        sens_label_frame = ctk.CTkFrame(sensitivity_row, fg_color="transparent")
        sens_label_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            sens_label_frame,
            text="Detection Sensitivity",
            font=self.typography["body_bold"]
        ).pack(side="left")

        self.sens_value = ctk.CTkLabel(
            sens_label_frame,
            text="3.0σ",
            font=self.typography["caption"]
        )
        self.sens_value.pack(side="left", padx=(12, 0))

        self.sensitivity_scale = ctk.CTkSlider(
            sensitivity_row,
            from_=1.0,
            to=6.0,
            number_of_steps=50,
            width=220,
            height=24,
            command=self._update_sensitivity_display
        )
        self.sensitivity_scale.set(3.0)
        self.sensitivity_scale.pack(side="right")

        # Cooldown control
        cooldown_row = ctk.CTkFrame(controls_section, fg_color="transparent")
        cooldown_row.pack(fill="x")

        cool_label_frame = ctk.CTkFrame(cooldown_row, fg_color="transparent")
        cool_label_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            cool_label_frame,
            text="Alert Cooldown Period",
            font=self.typography["body_bold"]
        ).pack(side="left")

        self.cool_value = ctk.CTkLabel(
            cool_label_frame,
            text="3.0s",
            font=self.typography["caption"]
        )
        self.cool_value.pack(side="left", padx=(12, 0))

        self.cooldown_scale = ctk.CTkSlider(
            cooldown_row,
            from_=0,
            to=10,
            number_of_steps=50,
            width=220,
            height=24,
            command=self._update_cooldown_display
        )
        self.cooldown_scale.set(3.0)
        self.cooldown_scale.pack(side="right")

        # Action buttons
        self.action_panel = ctk.CTkFrame(self, corner_radius=16)
        self.action_panel.pack(fill="x", padx=24, pady=(0, 24))

        button_container = ctk.CTkFrame(self.action_panel, fg_color="transparent")
        button_container.pack(pady=28)

        self.start_button = ctk.CTkButton(
            button_container,
            text="START MONITORING",
            font=self.typography["button"],
            corner_radius=12,
            width=170,
            height=48
        )
        self.start_button.pack(side="left", padx=12)

        self.stop_button = ctk.CTkButton(
            button_container,
            text="STOP MONITORING",
            font=self.typography["button"],
            corner_radius=12,
            width=170,
            height=48,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=12)

        self.reset_button = ctk.CTkButton(
            button_container,
            text="RESET SYSTEM",
            font=self.typography["button"],
            corner_radius=12,
            width=150,
            height=48,
            state="disabled"
        )
        self.reset_button.pack(side="left", padx=12)

        self.clear_button = ctk.CTkButton(
            button_container,
            text="CLEAR LOG",
            font=self.typography["button"],
            corner_radius=12,
            width=130,
            height=48
        )
        self.clear_button.pack(side="left", padx=12)

        # Main content
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        # Left panel - metrics (INCREASED WIDTH)
        self.metrics_panel = ctk.CTkFrame(self.main_content, corner_radius=16, width=500)
        self.metrics_panel.pack(side="left", fill="y", padx=(0, 24))
        self.metrics_panel.pack_propagate(False)

        # Risk section
        risk_section = ctk.CTkFrame(self.metrics_panel, fg_color="transparent")
        risk_section.pack(fill="x", padx=28, pady=28)

        ctk.CTkLabel(
            risk_section,
            text="Security Risk Assessment",
            font=self.typography["title"]
        ).pack(anchor="w")

        # Risk display
        risk_display = ctk.CTkFrame(risk_section, fg_color="transparent")
        risk_display.pack(fill="x", pady=(16, 0))

        self.risk_score_label = ctk.CTkLabel(
            risk_display,
            text="0",
            font=("Arial", 42, "bold")
        )
        self.risk_score_label.pack(side="left")

        risk_info = ctk.CTkFrame(risk_display, fg_color="transparent")
        risk_info.pack(side="left", fill="x", expand=True, padx=(20, 0))

        self.risk_level_label = ctk.CTkLabel(
            risk_info,
            text="SECURE",
            font=self.typography["body_bold"]
        )
        self.risk_level_label.pack(anchor="w")

        self.risk_description = ctk.CTkLabel(
            risk_info,
            text="No anomalies detected",
            font=self.typography["caption"]
        )
        self.risk_description.pack(anchor="w", pady=(2, 0))

        # Progress bar (INCREASED WIDTH)
        self.risk_progress = ctk.CTkProgressBar(
            risk_section,
            width=420,
            height=14,
            corner_radius=7
        )
        self.risk_progress.set(0)
        self.risk_progress.pack(fill="x", pady=(20, 16))

        # Typing speed
        self.typing_metrics = ctk.CTkLabel(
            risk_section,
            text="Typing Speed: -- WPM",
            font=self.typography["body"]
        )
        self.typing_metrics.pack(anchor="w")

        # Agent status (IMPROVED SPACING)
        ctk.CTkLabel(
            self.metrics_panel,
            text="Detection Agents",
            font=self.typography["title"]
        ).pack(anchor="w", padx=28, pady=(20, 12))

        self.agent_status = {}
        agents_config = [
            ("Movement", "Mouse movement pattern analysis"),
            ("Typing", "Keystroke dynamics monitoring"),
            ("AppUsage", "Application focus behavior")
        ]
        
        for agent_name, description in agents_config:
            agent_card = ctk.CTkFrame(
                self.metrics_panel,
                corner_radius=12,
                height=82  # Optimized height
            )
            agent_card.pack(fill="x", padx=28, pady=6)
            agent_card.pack_propagate(False)

            card_content = ctk.CTkFrame(agent_card, fg_color="transparent")
            card_content.pack(fill="both", expand=True, padx=20, pady=12)

            # Agent header
            agent_header = ctk.CTkFrame(card_content, fg_color="transparent")
            agent_header.pack(fill="x")

            agent_title = ctk.CTkLabel(
                agent_header,
                text=f"{agent_name} Agent",
                font=self.typography["body_bold"]
            )
            agent_title.pack(side="left")

            status_badge = ctk.CTkLabel(
                agent_header,
                text="IDLE",
                font=self.typography["caption"],
                corner_radius=6,
                width=70,
                height=22
            )
            status_badge.pack(side="right")

            # Description
            desc_label = ctk.CTkLabel(
                card_content,
                text=description,
                font=self.typography["caption"]
            )
            desc_label.pack(anchor="w", pady=(3, 0))

            # Statistics
            stats_label = ctk.CTkLabel(
                card_content,
                text="Mean: --, Std: --, Z-Score: --",
                font=self.typography["caption"]
            )
            stats_label.pack(anchor="w", pady=(1, 0))

            self.agent_status[agent_name] = {
                "status": status_badge,
                "description": desc_label,
                "stats": stats_label
            }

        # Right panel - log
        self.activity_panel = ctk.CTkFrame(self.main_content, corner_radius=16)
        self.activity_panel.pack(fill="both", expand=True)

        # Log header
        log_header = ctk.CTkFrame(self.activity_panel, fg_color="transparent")
        log_header.pack(fill="x", padx=28, pady=(28, 0))

        ctk.CTkLabel(
            log_header,
            text="System Activity Log",
            font=self.typography["title"]
        ).pack(side="left")

        log_status = ctk.CTkLabel(
            log_header,
            text="Real-time monitoring",
            font=self.typography["caption"]
        )
        log_status.pack(side="right", pady=4)

        # Log display
        self.log_display = ctk.CTkTextbox(
            self.activity_panel,
            corner_radius=12,
            font=self.typography["monospace"],
            border_width=1,
            wrap="word"
        )
        self.log_display.pack(fill="both", expand=True, padx=28, pady=(16, 28))
        self.log_display.configure(state="disabled")

    def _update_sensitivity_display(self, value):
        """Update sensitivity value display"""
        self.sens_value.configure(text=f"{float(value):.1f}σ")

    def _update_cooldown_display(self, value):
        """Update cooldown value display"""
        self.cool_value.configure(text=f"{float(value):.1f}s")

    def toggle_theme(self):
        """Theme toggle with smooth transitions"""
        self.appearance_mode = "light" if self.appearance_mode == "dark" else "dark"
        ctk.set_appearance_mode(self.appearance_mode)
        self.current_colors = self.colors[self.appearance_mode]
        
        theme_text = "Dark Theme" if self.appearance_mode == "dark" else "Light Theme"
        self.theme_toggle.configure(text=theme_text)
        
        self._apply_theme()

    def _apply_theme(self):
        """Apply Samsung One UI colors"""
        c = self.current_colors
        
        # Main elements
        self.configure(fg_color=c["primary"])
        
        frames_with_borders = [
            (self.header, c["secondary"]),
            (self.control_panel, c["secondary"]),
            (self.action_panel, c["secondary"]),
            (self.metrics_panel, c["secondary"]),
            (self.activity_panel, c["secondary"])
        ]
        
        for frame, bg_color in frames_with_borders:
            frame.configure(
                fg_color=bg_color,
                border_color=c["border"],
                border_width=1
            )
        
        # Text elements
        text_elements = [
            (self.title_label, c["text"]),
            (self.subtitle_label, c["text_secondary"]),
            (self.theme_toggle, c["text"]),
            (self.sens_value, c["text_secondary"]),
            (self.cool_value, c["text_secondary"]),
            (self.typing_metrics, c["text"]),
            (self.risk_description, c["text_secondary"])
        ]
        
        for element, color in text_elements:
            element.configure(text_color=color)
        
        # Buttons
        self.start_button.configure(fg_color=c["success"], hover_color=c["success"], text_color="white")
        self.stop_button.configure(fg_color=c["danger"], hover_color=c["danger"], text_color="white")
        self.reset_button.configure(fg_color=c["warning"], hover_color=c["warning"], text_color="white")
        self.clear_button.configure(fg_color=c["text_secondary"], hover_color=c["disabled"], text_color="white")
        
        # Sliders
        self.sensitivity_scale.configure(progress_color=c["accent"], button_color=c["accent"], fg_color=c["surface"])
        self.cooldown_scale.configure(progress_color=c["warning"], button_color=c["warning"], fg_color=c["surface"])
        
        # Risk display
        self.risk_score_label.configure(text_color=c["success"])
        self.risk_level_label.configure(text_color=c["success"])
        self.risk_progress.configure(progress_color=c["success"], fg_color=c["surface"])
        
        # Log display
        self.log_display.configure(fg_color=c["surface"], text_color=c["text"], border_color=c["border"])

    # Public API methods
    def set_state(self, state):
        """Update system status"""
        c = self.current_colors
        status_config = {
            "Stopped": ("STOPPED", c["text_secondary"], c["surface"]),
            "Monitoring": ("ACTIVE", "white", c["success"]),
            "Learning": ("LEARNING", "white", c["warning"])
        }
        
        text, text_color, bg_color = status_config.get(state, ("UNKNOWN", c["text"], c["surface"]))
        self.status_indicator.configure(text=text, text_color=text_color, fg_color=bg_color)

    def set_agent_status(self, agent_name, status):
        """Update agent status"""
        if agent_name not in self.agent_status:
            return
            
        c = self.current_colors
        status_config = {
            "Idle": ("IDLE", c["text_secondary"], c["surface"]),
            "Running": ("ACTIVE", "white", c["success"]),
            "Stable": ("STABLE", "white", c["success"]),
            "Adapting": ("LEARNING", "white", c["warning"]),
            "NoSignal": ("NO DATA", "white", c["warning"]),
            "Error": ("ERROR", "white", c["danger"])
        }
        
        text, text_color, bg_color = status_config.get(status, (status.upper(), c["text"], c["surface"]))
        self.agent_status[agent_name]["status"].configure(text=text, text_color=text_color, fg_color=bg_color)

    def update_agent_stats(self, agent_name, stats):
        """Update agent statistics"""
        if agent_name not in self.agent_status:
            return
            
        try:
            if all(stats.get(k) is not None for k in ["mean", "std", "z"]):
                stats_text = f"Mean: {stats['mean']:.3f}, Std: {stats['std']:.3f}, Z-Score: {stats['z']:.2f}"
            else:
                stats_text = "Mean: --, Std: --, Z-Score: --"
        except:
            stats_text = "Mean: --, Std: --, Z-Score: --"
        
        self.agent_status[agent_name]["stats"].configure(text=stats_text, text_color=self.current_colors["text_secondary"])
        
        if stats.get("note"):
            self.set_agent_status(agent_name, stats["note"])

    def update_risk_score(self, risk_score):
        """Update risk assessment"""
        c = self.current_colors
        
        self.risk_score_label.configure(text=str(risk_score))
        progress = min(risk_score / 15.0, 1.0)
        self.risk_progress.set(progress)
        
        if risk_score >= 12:
            level, desc, color = "CRITICAL", "Immediate attention required", c["danger"]
        elif risk_score >= 8:
            level, desc, color = "HIGH RISK", "Multiple anomalies detected", c["danger"]
        elif risk_score >= 4:
            level, desc, color = "ELEVATED", "Unusual activity detected", c["warning"]
        elif risk_score >= 1:
            level, desc, color = "MODERATE", "Minor anomalies present", c["warning"]
        else:
            level, desc, color = "SECURE", "No anomalies detected", c["success"]
        
        self.risk_score_label.configure(text_color=color)
        self.risk_level_label.configure(text=level, text_color=color)
        self.risk_description.configure(text=desc, text_color=self.current_colors["text_secondary"])
        self.risk_progress.configure(progress_color=color)

    def update_typing_speed(self, wpm):
        """Update typing speed (FIXED TYPO)"""
        if wpm > 0:
            if wpm >= 70:
                status = " (Fast)"
            elif wpm >= 40:
                status = " (Average)"
            elif wpm >= 20:
                status = " (Slow)"
            else:
                status = " (Very Slow)"
            text = f"Typing Speed: {wpm:.0f} WPM{status}"
        else:
            text = "Typing Speed: -- WPM"
        
        self.typing_metrics.configure(text=text)

    def add_log_message(self, message):
        """Add timestamped message to log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.log_display.configure(state="normal")
        self.log_display.insert("end", formatted_message + "\n")
        self.log_display.see("end")
        self.log_display.configure(state="disabled")

    def _clear_log(self):
        """Clear activity log"""
        self.log_display.configure(state="normal")
        self.log_display.delete("1.0", "end")
        self.log_display.configure(state="disabled")
        self.add_log_message("[System] Activity log cleared")
