import os
import shutil
import pyttsx3
import speech_recognition as sr
import pywhatkit
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import time
import pyaudio
import numpy as np
import re
import pyautogui
from datetime import datetime
import random

# Generate a large list of casual conversation responses (sample set)
casual_responses = [
    "That's interesting! Tell me more.",
    "Haha, I see what you did there.",
    "Really? That sounds cool!",
    "I'm always here to chat.",
    "Life's full of surprises, huh?",
    "So, what's new with you?",
    "Sounds like you're having a good day!",
    "I like your energy!",
    "You’ve got great vibes!",
    "Wanna hear a fun fact?",
    "Sometimes, it's just one of those days.",
    "I’m not human, but I totally get it.",
    "Let's talk about something random.",
    "That made me smile!",
    "Do you like music?",
    "What’s your favorite way to relax?",
    "Ever had a weird dream?",
    "Imagine flying cars everywhere.",
    "It’s nice talking to you!",
    "A virtual high-five! ✋",
    "How’s the weather where you are?",
    "You sound like a fun person.",
    "That’s deep. I like your thoughts.",
    "I’m always learning new things.",
    "Coffee or tea person?",
    "Let’s play a game sometime.",
    "You seem chill.",
    "Oh wow, I didn’t expect that.",
    "What's something cool you did recently?",
    "That sounds like a movie plot.",
    "I like how you think.",
    "How do you stay motivated?",
    "You’ve got style (even if I can’t see it 😄)",
    "Sometimes silence says a lot.",
    "Do you enjoy traveling?",
    "I could talk for hours!",
    "You ever just vibe to lo-fi beats?",
    "Feel free to vent—I’m listening.",
    "You're on a roll today!",
    "Ever wanted to time travel?",
    "I bet you're good at what you do.",
    "Random question: Do you like dogs or cats more?",
    "What’s your go-to snack?",
    "You ever stargaze and wonder?",
    "This is fun! Let’s keep chatting.",
    "How do you usually spend weekends?",
    "Hey, you’re pretty cool.",
    "I like our conversations.",
    "You’ve got a good sense of humor.",
    "You ever dance when no one’s watching?",
    "That gave me a chuckle.",
    "Some moments are just golden.",
    "Hey! Tell me something funny.",
    "Do you believe in aliens?",
    "Can’t believe how fast time flies.",
    "Random, but pineapple on pizza?",
    "I’m more of a night owl myself.",
    "That’s one way to look at it.",
    "You’ve got some good stories, huh?",
    "What makes you smile these days?",
    "Let’s talk about your dreams.",
    "That’s a vibe.",
    "I’d love to hear your thoughts.",
    "Tell me a joke, I dare you.",
    "You should write a book or something!",
    "Your energy is contagious.",
    "Let’s keep things light today.",
    "Some conversations just hit different.",
    "Whoa, plot twist!",
    "That reminds me of a meme.",
    "You’re full of surprises.",
    "Honestly, I enjoy these little chats.",
    "Care to share a favorite memory?",
    "Do you believe everything happens for a reason?",
    "Have you ever tried journaling?",
    "Even AI needs a break sometimes!",
    "Your curiosity is awesome.",
    "You’re pretty thoughtful.",
    "If I had a face, I’d be smiling.",
    "Let’s talk about the stars.",
    "If you had one superpower, what would it be?",
    "You seem like someone who’s got good stories.",
    "Do you talk to your plants?",
    "Got any favorite quotes?",
    "I could chat about this all day.",
    "Hmm, that's a good point.",
    "Now I’m curious!",
    "You’re giving main character energy.",
    "What’s a random skill you’d like to learn?",
    "I’m not bored, are you?",
    "You ever sing in the shower?",
    "Let’s do a thought experiment.",
    "That was unexpected… but fun!",
    "Keep being awesome.",
    "This feels like a real friendship.",
    "You ever write poems or songs?",
    "Got any hidden talents?",
    "We should chat more often!",
    "Mind if I ask a personal question?",
    "I love how creative you are.",
    "Every chat is a new adventure.",
    "This convo just made my circuits happy.",
    "You’re cool, you know that?"
]

# Randomly duplicate and shuffle to reach ~400
while len(casual_responses) < 400:
    casual_responses.append(random.choice(casual_responses))

random.shuffle(casual_responses)
casual_responses = casual_responses[:400]

# Preview the first few to confirm variety
casual_responses[:10]

listening = True

# ---------- Voice Setup ----------
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------- Command Handling ----------
def create_folder(folder_name, path="."):
    os.makedirs(os.path.join(path, folder_name), exist_ok=True)
    return f"📁 Folder '{folder_name}' created."

def delete_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return "🗑️ File deleted."
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            return "🗂️ Folder deleted."
        else:
            return "⚠️ File or folder not found."
    except Exception as e:
        return f"❌ Error deleting: {e}"

def move_file(src, dest):
    try:
        shutil.move(src, dest)
        return f"📦 Moved to {dest}"
    except Exception as e:
        return f"❌ Error moving: {e}"

def play_song_on_youtube(query):
    pywhatkit.playonyt(query)
    time.sleep(3)
    return f"🎶 Playing '{query}' on YouTube."

def open_application(app_name):
    try:
        pyautogui.press('win')
        pyautogui.write(app_name)
        time.sleep(2.5)
        pyautogui.press('enter')
        return f"🚀 Opening {app_name}..."
    except Exception as e:
        return f"❌ Failed to open {app_name}: {e}"

def calculate_expression(command):
    command = command.lower()
    command = command.replace("plus", "+").replace("add", "+")
    command = command.replace("minus", "-").replace("subtract", "-")
    command = command.replace("times", "*").replace("multiply", "*").replace("x", "*")
    command = command.replace("divide", "/").replace("divided by", "/")
    
    match = re.findall(r'[-+]?\d*\.?\d+|[+\-*/]', command)
    if not match or len(match) < 3:
        return None
    try:
        expression = ''.join(match)
        result = eval(expression)
        return f"🧮 The answer is {result}"
    except Exception as e:
        return f"❌ Error calculating: {e}"

def handle_command(cmd):
    cmd = cmd.lower()
    if cmd.startswith("open "):
        app = cmd.replace("open", "").strip()
        return open_application(app)
    calc = calculate_expression(cmd)
    if calc:
        return calc
    if "create folder" in cmd or "make folder" in cmd:
        folder_name = cmd.replace("create folder", "").replace("make folder", "").strip()
        return create_folder(folder_name)
    elif "delete" in cmd:
        item = cmd.replace("delete", "").strip()
        return delete_file(item)
    elif "move" in cmd and "to" in cmd:
        parts = cmd.split("to")
        if len(parts) == 2:
            src = parts[0].replace("move", "").strip()
            dest = parts[1].strip()
            return move_file(src, dest)
        return "Please say: move file.txt to D:\\Backup"
    elif "play" in cmd:
        song = cmd.split("play")[1].replace("on youtube", "").strip()
        return play_song_on_youtube(song)
        # --- Casual Chat ---
    elif "how are you" in cmd:
        return "I'm doing great! Thanks for asking 😊"
    elif "who made you" in cmd or "who created you" in cmd:
        return "I was created by my developer with lots of love and Python skills! 🐍"
    elif "what is your name" in cmd:
        return "I'm Echo, your AI assistant. Nice to meet you!"
    elif "tell me a joke" in cmd:
        return "Why did the computer go to therapy? Because it had too many bytes of emotional baggage! 😄"
    elif "thank you" in cmd or "thanks" in cmd:
        return "You're welcome! 😊"
    elif "what can you do" in cmd:
        return "I can help you manage files, open apps, play music, do calculations, and even chat a bit!"
    elif "good morning" in cmd:
        return "Good morning! ☀️ Hope you have a productive day ahead!"
    elif "good night" in cmd:
        return "Good night! 🌙 Sweet dreams!"
    else:
        return "🤖 Hmm... I didn’t quite get that, but I'm learning more every day!"


# ---------- Modern GUI Setup ----------
class ModernEchoGUI:
    def toggle_voice(self):
        global listening
        if not listening:
            # Check microphone availability before starting
            try:
                mic_list = sr.Microphone.list_microphone_names()
                if not mic_list:
                    self.add_system_message("❌ No microphone detected! Please connect a microphone.")
                    return

                listening = True  # ✅ Set this BEFORE starting the thread
                self.voice_btn.config(text="🛑 Stop Auto", bg=self.colors['error'])
                self.update_status("Initializing...", self.colors['warning'])
                threading.Thread(target=self.listen_voice_loop, daemon=True).start()

            except Exception as e:
                self.add_system_message(f"❌ Microphone error: {e}")
                self.add_system_message("💡 Try checking your microphone permissions and connection.")
        else:
            listening = False
            self.voice_btn.config(text="🔄 Auto Listen", bg=self.colors['success'])
            self.update_status("Ready", self.colors['success'])
            self.add_system_message("🛑 Auto-listen stopped.")

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Echo AI Assistant")
        self.window.geometry("900x700")
        self.window.configure(bg="#0a0a0a")
        self.window.resizable(True, True)
        
        # Color scheme
        self.colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#1a1a1a',
            'bg_tertiary': '#2a2a2a',
            'accent': '#00d4ff',
            'accent_hover': '#00b8e6',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'text_muted': '#888888',
            'success': '#00ff88',
            'error': '#ff4444',
            'warning': '#ffaa00'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.setup_waveform()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='black',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_hover'])])
        
    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.window, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_frame)
        
        # Status indicator
        self.create_status_section(main_frame)
        
        # Waveform visualization
        self.create_waveform_section(main_frame)
        
        # Chat area
        self.create_chat_section(main_frame)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Control buttons
        self.create_control_section(main_frame)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo/Title
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(side='left')
        
        title_label = tk.Label(title_frame, 
                              text="Echo", 
                              font=('Segoe UI', 28, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent'])
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(title_frame,
                                 text="AI Assistant",
                                 font=('Segoe UI', 14),
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(side='left', padx=(10, 0))
        
        # Time display
        self.time_label = tk.Label(header_frame,
                                  text="",
                                  font=('Segoe UI', 12),
                                  bg=self.colors['bg_primary'],
                                  fg=self.colors['text_muted'])
        self.time_label.pack(side='right')
        self.update_time()
        
    def create_status_section(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=50)
        status_frame.pack(fill='x', pady=(0, 15))
        status_frame.pack_propagate(False)
        
        # Status indicator
        self.status_indicator = tk.Label(status_frame,
                                        text="● Ready",
                                        font=('Segoe UI', 12, 'bold'),
                                        bg=self.colors['bg_secondary'],
                                        fg=self.colors['success'])
        self.status_indicator.pack(side='left', padx=20, pady=15)
        
        # Quick stats
        self.stats_label = tk.Label(status_frame,
                                   text="Commands processed: 0",
                                   font=('Segoe UI', 10),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_muted'])
        self.stats_label.pack(side='right', padx=20, pady=15)
        
    def create_waveform_section(self, parent):
        waveform_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        waveform_frame.pack(fill='x', pady=(0, 20))
        
        # Waveform canvas with modern styling
        self.canvas = tk.Canvas(waveform_frame, 
                               width=860, 
                               height=80, 
                               bg=self.colors['bg_secondary'],
                               highlightthickness=0,
                               relief='flat')
        self.canvas.pack(pady=10)
        
        # Create gradient effect bars
        self.wave_bars = []
        bar_width = 4
        bar_spacing = 6
        num_bars = 140
        
        for i in range(num_bars):
            x = i * bar_spacing + 10
            bar = self.canvas.create_rectangle(x, 35, x + bar_width, 45, 
                                             fill=self.colors['accent'], 
                                             outline='')
            self.wave_bars.append(bar)
            
    def create_chat_section(self, parent):
        chat_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        chat_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Custom scrolled text with modern styling
        self.chat_area = scrolledtext.ScrolledText(chat_frame,
                                                  wrap=tk.WORD,
                                                  font=('Segoe UI', 11),
                                                  bg=self.colors['bg_secondary'],
                                                  fg=self.colors['text_primary'],
                                                  insertbackground=self.colors['accent'],
                                                  selectbackground=self.colors['accent'],
                                                  selectforeground='black',
                                                  relief='flat',
                                                  borderwidth=0,
                                                  padx=20,
                                                  pady=20)
        self.chat_area.pack(fill='both', expand=True)
        self.chat_area.configure(state='disabled')
        
        # Add welcome message
        self.add_system_message("Welcome to Echo AI Assistant! I'm ready to help you with various tasks.")
        
    def create_input_section(self, parent):
        input_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        input_frame.pack(fill='x', pady=(0, 15))
        
        # Input container with modern styling
        input_container = tk.Frame(input_frame, bg=self.colors['bg_tertiary'])
        input_container.pack(fill='x', ipady=10)
        
        # Text input
        self.entry = tk.Entry(input_container,
                             font=('Segoe UI', 12),
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'],
                             insertbackground=self.colors['accent'],
                             relief='flat',
                             borderwidth=0)
        self.entry.pack(side='left', fill='x', expand=True, padx=(20, 10), ipady=5)
        self.entry.bind('<Return>', lambda e: self.on_enter())
        
        # Send button
        send_btn = tk.Button(input_container,
                            text="Send",
                            font=('Segoe UI', 10, 'bold'),
                            bg=self.colors['accent'],
                            fg='black',
                            relief='flat',
                            borderwidth=0,
                            padx=20,
                            command=self.on_enter)
        send_btn.pack(side='right', padx=(0, 20))
        
        # Hover effects
        def on_enter_hover(e):
            send_btn.config(bg=self.colors['accent_hover'])
        def on_leave_hover(e):
            send_btn.config(bg=self.colors['accent'])
            
        send_btn.bind('<Enter>', on_enter_hover)
        send_btn.bind('<Leave>', on_leave_hover)
        
    def create_control_section(self, parent):
        control_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        control_frame.pack(fill='x')
        
        # Control buttons with modern styling
        btn_frame = tk.Frame(control_frame, bg=self.colors['bg_primary'])
        btn_frame.pack()
        
        # Listen button (primary action)
        self.listen_btn = tk.Button(btn_frame,
                                   text="🎙️ Listen",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['accent'],
                                   fg='black',
                                   relief='flat',
                                   borderwidth=0,
                                   padx=40,
                                   pady=10,
                                   command=self.start_single_listen)
        self.listen_btn.pack(side='left', padx=10)
        
        # Voice toggle button (continuous listening)
        self.voice_btn = tk.Button(btn_frame,
                                  text="🔄 Auto Listen",
                                  font=('Segoe UI', 11, 'bold'),
                                  bg=self.colors['success'],
                                  fg='black',
                                  relief='flat',
                                  borderwidth=0,
                                  padx=30,
                                  pady=8,
                                  command=self.toggle_voice)
        self.voice_btn.pack(side='left', padx=10)
        
        # Clear button
        clear_btn = tk.Button(btn_frame,
                             text="Clear Chat",
                             font=('Segoe UI', 11),
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'],
                             relief='flat',
                             borderwidth=0,
                             padx=30,
                             pady=8,
                             command=self.clear_chat)
        clear_btn.pack(side='left', padx=10)
        
        # Add hover effects
        self.add_button_hover_effects()
        
    def add_button_hover_effects(self):
        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=normal_color)
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)
        
        # Add hover effects to buttons
        for widget in self.window.winfo_children():
            self.add_hover_to_buttons(widget)
    
    def add_hover_to_buttons(self, widget):
        if isinstance(widget, tk.Button):
            original_bg = widget.cget('bg')
            if original_bg == self.colors['success']:
                hover_color = '#00e699'
            elif original_bg == self.colors['bg_tertiary']:
                hover_color = '#3a3a3a'
            else:
                hover_color = self.colors['accent_hover']
                
            def on_enter(e):
                widget.config(bg=hover_color)
            def on_leave(e):
                widget.config(bg=original_bg)
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
        
        for child in widget.winfo_children():
            self.add_hover_to_buttons(child)
    
    def setup_waveform(self):
        # Start audio monitoring thread
        threading.Thread(target=self.audio_loop, daemon=True).start()
        
    def audio_loop(self):
        try:
            p = pyaudio.PyAudio()
            
            # Check if audio input is available
            input_devices = []
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_devices.append(device_info)
            
            if not input_devices:
                print("No audio input devices found")
                return
            
            stream = p.open(format=pyaudio.paInt16, 
                          channels=1, 
                          rate=44100, 
                          input=True, 
                          frames_per_buffer=1024)
            
            while True:
                try:
                    data = np.frombuffer(stream.read(1024, exception_on_overflow=False), 
                                       dtype=np.int16)
                    volume = np.linalg.norm(data) / 300
                    volume = min(volume, 1.0)
                    self.update_waveform(volume)
                    time.sleep(0.05)
                except Exception as e:
                    print(f"Audio loop error: {e}")
                    continue
        except Exception as e:
            print(f"Audio initialization error: {e}")
            # Continue without audio visualization
            while True:
                self.update_waveform(0.1)  # Show static waveform
                time.sleep(0.1)
    
    def update_waveform(self, volume):
        if not hasattr(self, 'wave_bars'):
            return
            
        for i, bar in enumerate(self.wave_bars):
            # Create wave pattern
            wave_height = volume * 30 * np.sin(i * 0.1 + time.time() * 3)
            wave_height = abs(wave_height)
            
            # Update bar height
            bar_height = max(2, wave_height)
            y1 = 40 - bar_height/2
            y2 = 40 + bar_height/2
            
            # Get bar coordinates
            coords = self.canvas.coords(bar)
            if coords:
                x1, x2 = coords[0], coords[2]
                self.canvas.coords(bar, x1, y1, x2, y2)
                
                # Color based on volume
                if volume > 0.3:
                    color = self.colors['success']
                elif volume > 0.1:
                    color = self.colors['accent']
                else:
                    color = self.colors['text_muted']
                    
                self.canvas.itemconfig(bar, fill=color)
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.window.after(1000, self.update_time)
    
    def add_user_message(self, message):
        self.chat_area.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"\n[{timestamp}] You: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)
    
    def add_bot_message(self, message):
        self.chat_area.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] Echo: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)
    
    def add_system_message(self, message):
        self.chat_area.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] System: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)
    
    def update_status(self, status, color=None):
        if color is None:
            color = self.colors['success']
        self.status_indicator.config(text=f"● {status}", fg=color)
    
    def on_enter(self):
        cmd = self.entry.get().strip()
        if cmd:
            self.entry.delete(0, tk.END)
            self.add_user_message(cmd)
            
            # Update status
            self.update_status("Processing...", self.colors['warning'])
            
            # Process command
            response = handle_command(cmd)
            self.add_bot_message(response)
            
            # Speak response
            threading.Thread(target=lambda: speak(response), daemon=True).start()
            
            # Update status
            self.update_status("Ready", self.colors['success'])
    
    def start_single_listen(self):
        """Listen for a single command (one-time listening)"""
        if listening:
            self.add_system_message("⚠️ Auto-listen is already running. Stop it first or just speak.")
            return
            
        self.listen_btn.config(text="🎙️ Listening...", bg=self.colors['warning'])
        self.update_status("Listening...", self.colors['accent'])
        
        threading.Thread(target=self.single_listen_loop, daemon=True).start()
    
    def single_listen_loop(self):
        """Listen for a single command and then stop"""
        try:
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            recognizer.phrase_threshold = 0.3
            
            # Check if microphone is available
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                self.add_system_message("❌ No microphone detected!")
                self.reset_listen_button()
                return
                
            mic = sr.Microphone()
            
            # Quick calibration
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for single command
            try:
                with mic as source:
                    self.update_status("Listening...", self.colors['accent'])
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    
                self.update_status("Processing...", self.colors['warning'])
                
                try:
                    command = recognizer.recognize_google(audio).lower()
                    self.add_user_message(command)
                    
                    response = handle_command(command)
                    self.add_bot_message(response)
                    threading.Thread(target=lambda: speak(response), daemon=True).start()
                    
                except sr.UnknownValueError:
                    self.add_bot_message("❌ I didn't catch that. Please try again.")
                    
            except sr.WaitTimeoutError:
                self.add_system_message("⏱️ No speech detected. Click Listen to try again.")
            except sr.RequestError as e:
                self.add_system_message(f"❌ Speech recognition error: {e}")
            except Exception as e:
                self.add_system_message(f"⚠️ Unexpected error: {e}")
                
        except Exception as e:
            self.add_system_message(f"❌ Failed to initialize voice recognition: {e}")
            self.add_system_message("💡 Make sure your microphone is connected and permissions are granted.")
            
        finally:
            self.reset_listen_button()
    
    def reset_listen_button(self):
        """Reset the listen button to its original state"""
        self.listen_btn.config(text="🎙️ Listen", bg=self.colors['accent'])
        self.update_status("Ready", self.colors['success'])
    
    def listen_voice_loop(self):
        global listening
        listening = True
        
        try:
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            recognizer.phrase_threshold = 0.3
            
            # Check if microphone is available
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                self.add_system_message("❌ No microphone detected!")
                listening = False
                return
                
            mic = sr.Microphone()
            
            self.add_system_message("🎙️ Voice recognition started. Say 'stop listening' to stop.")
            self.add_system_message("🔧 Adjusting for ambient noise... Please wait.")
            
            # Initial calibration
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
            self.add_system_message("✅ Ready to listen!")
            
            while listening:
                try:
                    with mic as source:
                        self.update_status("Listening...", self.colors['accent'])
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)
                        
                    self.update_status("Processing...", self.colors['warning'])
                    
                    try:
                        command = recognizer.recognize_google(audio).lower()
                        self.add_user_message(command)
                        
                        if "stop listening" in command:
                            self.add_bot_message("🛑 Voice recognition stopped.")
                            speak("Voice recognition stopped.")
                            listening = False
                            self.voice_btn.config(text="🔄 Auto Listen", bg=self.colors['success'])
                            self.update_status("Ready", self.colors['success'])
                            break
                        
                        response = handle_command(command)
                        self.add_bot_message(response)
                        threading.Thread(target=lambda: speak(response), daemon=True).start()
                        
                    except sr.UnknownValueError:
                        self.add_bot_message("❌ I didn't catch that. Please try again.")
                        
                except sr.WaitTimeoutError:
                    # This is normal - just continue listening
                    continue
                except sr.RequestError as e:
                    self.add_system_message(f"❌ Speech recognition error: {e}")
                    break
                except Exception as e:
                    self.add_system_message(f"⚠️ Unexpected error: {e}")
                    break
                    
        except Exception as e:
            self.add_system_message(f"❌ Failed to initialize voice recognition: {e}")
            self.add_system_message("💡 Make sure your microphone is connected and permissions are granted.")
            
        finally:
            listening = False
            self.voice_btn.config(text="🎙️ Start Voice", bg=self.colors['success'])
            self.update_status("Ready", self.colors['success'])
    
    def clear_chat(self):
        self.chat_area.configure(state='normal')
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.configure(state='disabled')
        self.add_system_message("Chat cleared. How can I help you?")
    
    def run(self):
        self.window.mainloop()

# ---------- Launch Application ----------
if __name__ == "__main__":
    app = ModernEchoGUI()
    app.run()