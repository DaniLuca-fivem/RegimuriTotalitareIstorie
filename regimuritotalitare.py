import tkinter as tk
from tkinter import Frame, Label, Button, PhotoImage, Radiobutton, Scale, Scrollbar, StringVar, image_names, scrolledtext, Text
from PIL import Image, ImageTk # type: ignore
import time
import math
import random
import pygame # type: ignore
import google.generativeai as genai # type: ignore
import colorsys

pygame.mixer.init()

root = tk.Tk()
root.title("Joc Istoric de Strategie") # titlu
root.geometry("1920x1080") # rezolutie
root.attributes('-fullscreen', True)  # fullscreen


root.grid_rowconfigure(0, weight=1) 
root.grid_columnconfigure(0, weight=1)

def exit_fullscreen(event=None): #comanda exit fullscreen
    root.geometry("1080x720")
    root.attributes('-fullscreen', False)

def enter_fullscreen(event=None): #comanda enter fullscreen
    root.geometry("1920x1080")
    root.attributes('-fullscreen', True)

root.bind("<Escape>", exit_fullscreen) #bind exit fullscreen
root.bind('<Alt-Return>', enter_fullscreen) #bind enter fullscreen (Alt+Enter)

#
# Imagini pentru backgrounds
#

intro_bg_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\imagineintro.png"
intro_bg_image = Image.open(intro_bg_path)
intro_bg_tk = ImageTk.PhotoImage(intro_bg_image, master=root)

info_bg_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\imagineinfo.png"
info_bg_image = Image.open(info_bg_path)
info_bg_tk = ImageTk.PhotoImage(info_bg_image, master=root)

add_comunism_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\imaginecomunism.png"
comunism_bg_image = Image.open(add_comunism_path)
com_bg_tk = ImageTk.PhotoImage(comunism_bg_image, master=root)

add_nazism_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\imaginenazism.png"
nazism_bg_image= Image.open(add_nazism_path)
naz_bg_tk = ImageTk.PhotoImage(nazism_bg_image, master=root)

add_fascism_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\imaginefascism.png"
fascism_bg_image = Image.open(add_fascism_path)
fasc_bg_tk = ImageTk.PhotoImage(fascism_bg_image, master=root)

add_carteHitler_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\carteHitler.jpeg"
carteHitler_bg_image = Image.open(add_carteHitler_path)
carteHitler_bg_tk = ImageTk.PhotoImage(carteHitler_bg_image, master=root)

#add_quizbg_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\quiz_bg.png"
#quizbg_image = Image.open(add_quizbg_path)
#quizbg_tk = ImageTk.PhotoImage(quizbg_image)

# Frame-uri
loading_frame = Frame(root, bg="#90EE90")  # Verde pal pentru loading
loading_frame2 = Frame(root, bg="#90EE90")  # Verde pal pentru loading
intro_frame = Frame(root)
info_frame = Frame(root)
regime_frame = Frame(root, bg="#004d40")
additional_frame = Frame(root, bg="#2e2e2e", width=1920, height=1080)
quiz_frame = Frame(root, width=1920, height=1080)

# Background-uri
loading_label = Label(loading_frame, bg="#90EE90")  # Label gol pentru a putea seta bg-ul frame-ului
loading_label.place(x=0, y=0, relwidth=1, relheight=1)

loading_label2 = Label(loading_frame, bg="#90EE90")  # Label gol pentru a putea seta bg-ul frame-ului
loading_label2.place(x=0, y=0, relwidth=1, relheight=1)

background_label = Label(intro_frame, image=intro_bg_tk)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

bg_label = Label(info_frame, image=info_bg_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

quiz_label = Label(quiz_frame, bg="black")
quiz_label.place(x=0, y=0, relwidth=1, relheight=1)

# Grid pentru frame-uri
loading_frame.grid(row=0, column=0, sticky="nsew")
loading_frame2.grid(row=0, column=0, sticky="nsew")
intro_frame.grid(row=0, column=0, sticky="nsew")
info_frame.grid(row=0, column=0, sticky="nsew")
regime_frame.grid(row=0, column=0, sticky="nsew")
additional_frame.grid(row=0, column=0, sticky="nsew")

logo_image_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\cnvl.jpg"
logo_image = Image.open(logo_image_path)
logo_image = logo_image.resize((150, 150))  
logo_photo = ImageTk.PhotoImage(logo_image)

holocaust_frame = tk.Frame(root, bg="#2e2e2e")  # Creare frame pentru Holocaust
holocaust_frame.grid(row=0, column=0, sticky="nsew")

#
# Culorile regimurilor
#

regimes_colors = {
    "Nazism": "#4d4d00",  # Galben
    "Fascism": "#264d00",  # Verde inchis
    "Comunism": "#661a00",  # Rosu
}

##################################################
################### FUNCTII ######################
##################################################


def show_frame(frame):  # afiseaza cadrul
    frame.tkraise()
    root.update()

def show_frame_stop_music(frame):
    stop_music()
    frame.tkraise()
    root.update()

def stop_music():
    pygame.mixer.music.stop()

def toggle_image_size(image_label, image_path, enlarged_size=(750, 750), original_size=(150, 150)):
    current_size = getattr(image_label, "current_size", original_size)
    new_size = enlarged_size if current_size == original_size else original_size

    try:
        img = Image.open(image_path)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo 
        image_label.current_size = new_size

    except Exception as e:
        print(f"Error loading image {image_path}: {e}")

def reset_all_images():
    for label, path in image_labels:
        toggle_image_size(label, path)

image_labels = []

bg_label.bind("<Button-1>", lambda event: toggle_image_size(bg_label, info_bg_path))
image_labels.append((bg_label, info_bg_path))

com_bg_label = Label(regime_frame, image=com_bg_tk, bg="#3e3e3e")
com_bg_label.image = com_bg_tk
com_bg_label.place(x=50, y=50)

naz_bg_label = Label(regime_frame, image=naz_bg_tk, bg="#3e3e3e")
naz_bg_label.image = naz_bg_tk
naz_bg_label.place(x=250, y=50)

fasc_bg_label = Label(regime_frame, image=fasc_bg_tk, bg="#3e3e3e")
fasc_bg_label.image = fasc_bg_tk
fasc_bg_label.place(x=450, y=50)

com_bg_label.bind("<Button-1>", lambda event: toggle_image_size(com_bg_label, add_comunism_path))
image_labels.append((com_bg_label, add_comunism_path))

naz_bg_label.bind("<Button-1>", lambda event: toggle_image_size(naz_bg_label, add_nazism_path))
image_labels.append((naz_bg_label, add_nazism_path))

fasc_bg_label.bind("<Button-1>", lambda event: toggle_image_size(fasc_bg_label, add_fascism_path))
image_labels.append((fasc_bg_label, add_fascism_path))


def display_images(image_paths):
    global img_refs
    img_refs = []
    image_size = (150, 150)
    positions = [(50, 50), (1300, 50), (50, 600), (1300, 600)]
    for i, path in enumerate(image_paths):
        try:
            img = Image.open(path)
            img = img.resize(image_size, Image.Resampling.LANCZOS)
            img_refs.append(img)
            photo = ImageTk.PhotoImage(img)
            label = Label(regime_frame, image=photo, bg="#3e3e3e")
            label.image = photo
            label.place(x=positions[i][0], y=positions[i][1])

            label.bind("<Button-1>", lambda event, l=label, p=path: toggle_image_size(l, p))
            image_labels.append((label, path))

        except Exception as e:
            print(f"Eroare la încărcarea imaginii {path}: {e}")


def add_logo_to_frame(frame):
    logo_path = r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\cnvl.jpg"
    
    try:
        pil_image = Image.open(logo_path)
        pil_image = pil_image.resize((150, 150), Image.Resampling.LANCZOS)
        
        logo_image = ImageTk.PhotoImage(pil_image)
        
        logo_label = tk.Label(frame, image=logo_image, bg="white")
        logo_label.image = logo_image  
        
        logo_label.place(relx=0.94, rely=0.90, anchor="center") 

    except Exception as e:
        print(f"Eroare la încărcarea imaginii: {e}")


class TextNeon(tk.Canvas):
    def __init__(self, master, text, culori_neon, latime=400, inaltime=200):
        super().__init__(master, width=latime, height=inaltime, highlightthickness=0, bg="#90EE90")
        self.text = text.upper()
        self.culori_neon = culori_neon
        self.latime = latime
        self.inaltime = inaltime
        self.litere = []

        self.x_centru = latime / 2
        self.y_centru = inaltime / 2

        self.creeaza_text()
        self.animatie_id = None

    def creeaza_text(self):
        latime_text = self.latime / len(self.text)  
        for i, litera in enumerate(self.text):
            x = self.x_centru  
            y = self.y_centru
            culoare = self.culori_neon[i % len(self.culori_neon)]

           
            x_final = latime_text * (i + 0.5)  
            y_final = self.y_centru

            litera_id = self.create_text(x, y, text=litera, font=("Arial", 80), fill=culoare)
            self.litere.append((litera_id, x_final, y_final)) 

    def anima_aparitia(self, i=0):
        if i < len(self.litere):
            litera_id, x_final, y_final = self.litere[i]
            x_curent, y_curent = self.coords(litera_id)

            x_nou = x_curent + (x_final - x_curent) * 0.1
            y_nou = y_curent + (y_final - y_curent) * 0.1

            self.coords(litera_id, x_nou, y_nou)

            if abs(x_nou - x_final) < 1 and abs(y_nou - y_final) < 1:
                self.after(100, self.anima_aparitia, i + 1)
            else:
                self.after(50, self.anima_aparitia, i)
        else:
            self.anima_stralucirea()

    def anima_stralucirea(self, intensitate=0.5):
        culoare_curenta1 = self.winfo_rgb(self.culori_neon[0])
        culoare_curenta2 = self.winfo_rgb(self.culori_neon[1])
        factor = 1 + intensitate * (0.5 - time.time() % 1)

        noua_culoare1 = "#%02x%02x%02x" % (
            int((culoare_curenta1[0] * factor) / 256),  
            int((culoare_curenta1[1] * factor) / 256),  
            int((culoare_curenta1[2] * factor) / 256) 
        )
        noua_culoare2 = "#%02x%02x%02x" % (
            int((culoare_curenta2[0] * factor) / 256), 
            int((culoare_curenta2[1] * factor) / 256), 
            int((culoare_curenta2[2] * factor) / 256)   
        )

        for j, item in enumerate(self.find_all()):
            if self.type(item) == 'text': 
                if j < len(self.litere) // 2:  
                    self.itemconfig(item, fill=noua_culoare1)
                else:
                    self.itemconfig(item, fill=noua_culoare2)

        self.animatie_id = self.after(50, self.anima_stralucirea, intensitate)

    def opreste_animatia(self):
        if self.animatie_id:
            self.after_cancel(self.animatie_id)
            self.animatie_id = None

    def reinitializeaza_animatia(self):
        self.opreste_animatia()
        for litera_id, x, y in self.litere:
            self.coords(litera_id, self.x_centru, self.y_centru)  
        self.anima_aparitia()

def loading_screen(root):
    global loading_frame
    loading_frame = tk.Frame(root, bg="#90EE90")
    loading_frame.grid(row=0, column=0, sticky="nsew")
    
    Label(
        loading_frame,
        text="Istorie și societate în dimensiunea virtuală",
        font=("Arial Black", 36),
        bg="#90EE90",
        fg="black",
    ).place(relx=0.5, rely=0.3, anchor="center")
    
    Label(
        loading_frame,
        text="Toate informatiile, respectiv, melodiile sunt utilizate cu scop educativ.",
        font=("Arial Black", 27),
        bg="#90EE90",
        fg="black",
    ).place(relx=0.5, rely=0.5, anchor="center")

    Label(
        loading_frame,
        text="Budea Daniel-Mircea -- Clasa a X-a A -- CNVL",
        font=("Arial Black", 20),
        bg="#90EE90",
        fg="red",
    ).place(relx=0.5, rely=0.85, anchor="center")
    
    canvas = tk.Canvas(loading_frame, width=200, height=200, bg="#90EE90", highlightthickness=0)
    canvas.place(relx=0.5, rely=0.7, anchor="center")
    
    def animation(angle=0):
        canvas.delete("all")
        width, height = 200, 200
        center_x, center_y = width // 2, height // 2
        size = 50
        
        points = []
        for i in range(360):
            rad = math.radians(i)
            x = center_x + size * math.sin(2 * rad + angle)
            y = center_y + size * math.sin(3 * rad + angle)
            points.append((x, y))
        
        for i in range(len(points) - 1):
            canvas.create_line(points[i], points[i + 1], fill='#0000e6', width=5)
        
        loading_frame.after(50, lambda: animation(angle + 0.1))

    text_cnvl = TextNeon(loading_frame, 'CNVL', ['#03b5f7', '#06a6e3'])
    text_cnvl.place(relx=0.5, rely=0.15, anchor="center")
    text_cnvl.anima_aparitia()

    
    animation()

    root.update()  

def loading_screen2():
    loading_frame2.tkraise()

    Label(
        loading_frame2,
        text="""Bibliografie:
                    United States Holocaust Memorial Museum: https://www.ushmm.org
                    Britannica: https://www.britannica.com/topic/Nazism    
                    Britannica - Holocaust: https://www.britannica.com/event/Holocaust
                    Zeev Sternhell - The Birth of Fascist Ideology
                    Hannah Arendt - The Origins of Totalitarianism
                    Harvard University – Library of Soviet History: https://library.harvard.edu/collections/soviet-history
                    Stanford Encyclopedia of Philosophy: https://plato.stanford.edu/entries/fascism
                    Stanford University – Hoover Institution: https://www.hoover.org
                    Stanford Encyclopedia of Philosophy: https://plato.stanford.edu
                    Imnurile regimurilor totalitare: 
                    https://www.youtube.com/@HistoryFandom - R. nazist
                    https://www.youtube.com/@rascrifice - R. comunist 
                    https://www.youtube.com/@Ingenting - R. fascist
            """,
        font=("Arial Black", 20),
        bg="#90EE90",
        fg="black",
    ).place(relx=0.45, rely=0.4, anchor="center")
    Label(
        loading_frame2,
        text="""Credite imagini: 
        - imagini generate cu ajutorul inteligentei artificiale
        - preluate de pe Wikipedia sau alte site-uri deja mentionate mai sus
        - Text Studio (anii)
        """,
        font=("Arial Black", 18),
        bg="#90EE90",
        fg="black",
    ).place(relx=0.45, rely=0.8, anchor="center")

    root.update_idletasks() 
    root.update()  
loading_screen2()

# Creare frame pentru chat AI
ai_chat_frame = Frame(root, bg="#2e2e2e", width=1920, height=1080)
ai_chat_frame.grid(row=0, column=0, sticky="nsew")

# Configurare API Gemini AI
genai.configure(api_key="AIzaSyCZaJ3joNaKvwxonki1sKLpMvAEv2G1dlE")

def ask_ai(question):
    prompt = f"Raspunde la urmatoarea intrebare: {question}"
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"

def display_ai_response(question_entry, response_text):  
    question = question_entry.get("1.0", tk.END).strip()
    if question:
        response = ask_ai(question)
        response_text.config(state=tk.NORMAL)
        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, response)
        response_text.config(state=tk.DISABLED)
        question_entry.delete("1.0", tk.END)  


def create_ai_chat_frame(root):
    ai_chat_frame = Frame(root, bg="#2e2e2e")
    ai_chat_frame.grid(row=0, column=0, sticky="nsew")

    # Titlu
    Label(ai_chat_frame, text="Intrebări suplimentare", font=("Arial Black", 36), bg="#2e2e2e", fg="white").pack(pady=(20, 10))

    question_frame = Frame(ai_chat_frame, bg="#333333", padx=20, pady=10)
    question_frame.pack(pady=(10, 5))

    Label(question_frame, text="Introdu întrebarea ta:", font=("Arial", 16), bg="#333333", fg="white").pack()
    question_entry = Text(question_frame, height=5, width=80, font=("Arial", 14), bg="#444444", fg="white", insertbackground="white")
    question_entry.pack()

    response_frame = Frame(ai_chat_frame, bg="#333333", padx=20, pady=10)
    response_frame.pack(pady=(5, 20))

    Label(response_frame, text="Răspunsul la întrebarea ta:", font=("Arial", 16), bg="#333333", fg="white").pack()
    response_text = Text(response_frame, height=10, width=80, font=("Arial", 14), bg="#444444", fg="white", state=tk.DISABLED, insertbackground="white")
    response_text.pack()

    Button(ai_chat_frame, text="Trimite", font=("Arial", 16), bg="#0077cc", fg="white",
           command=lambda: display_ai_response(question_entry, response_text), activebackground="#0055aa").pack(pady=(10, 20))

    question_entry.bind("<Return>", lambda event: display_ai_response(question_entry, response_text))  # Ambele widget-uri sunt transmise

    Button(
        ai_chat_frame, 
        text="⬅ Înapoi la Informații", 
        font=("Arial", 16), 
        bg="#990000", 
        fg="white",
        command=lambda: show_frame(info_frame)
    ).place(relx=0.5, rely=0.9, anchor="center")

    return ai_chat_frame  

create_ai_chat_frame(root)

ai_chat_frame = create_ai_chat_frame(root)
info_frame = Frame(root, bg="white")  # Frame de test

ai_chat_frame.grid(row=0, column=0, sticky="nsew")
info_frame.grid(row=0, column=0, sticky="nsew")

ai_chat_frame.tkraise()

def create_intro_frame(): 
    
    #
    # Labels pentru text 
    #
    
    Label(
        intro_frame,
        text="Regimuri totalitare",
        font=("Arial Black", 46),
        bg="#fff2cc",
        fg="black",
    ).place(relx=0.5, rely=0.2, anchor="center") 

    max_height = intro_frame.winfo_reqheight() * 0.5  

    # Caseta 1
    frame_caseta1 = Frame(intro_frame, bg="#fff2cc", height=max_height)  
    frame_caseta1.place(relx=0.3, rely=0.5, anchor="center")  

    Label(
        frame_caseta1,
        text="© 2025 Budea Daniel-Mircea. Toate drepturile rezervate.",
        font=("Arial", 16),
        bg="#fff2cc",
        fg="black",
    ).pack()

    Label(
        frame_caseta1,
        text="""Autori:
 Profesori coordonatori:
 Bodnar Anca Alexandra - prof. Istorie
 Mureșan Ioana Claudia - prof. Informatică
 Elev: 
 Budea Daniel-Mircea""",
        font=("Arial", 15),
        bg="#fff2cc",
        fg="black",
    ).pack()

    # Caseta 2
    frame_caseta2 = Frame(intro_frame, bg="#fff2cc", height=max_height)  
    frame_caseta2.place(relx=0.7, rely=0.5, anchor="center")  

    Label(
        frame_caseta2,
        text="Acest joc a fost creat cu scop educativ.",
        font=("Arial", 15),
        bg="#fff2cc",
        fg="black",
    ).pack()

    Label(
        frame_caseta2,
        text="Toate informatiile au fost verificate din mai multe surse.",
        font=("Arial", 15),
        bg="#fff2cc",
        fg="black",
    ).pack()

    Label(
        frame_caseta2,
        text="""Pentru a raporta o neregula trimiteti un email urmatoarea adresa:
            daniel.budea@lucaciu.ro""",
        font=("Arial", 15),
        bg="#fff2cc",
        fg="black",
    ).pack()

    Button( # buton care te trimite la cel de al doilea frame
        intro_frame,
        text="Să începem",
        font=("Arial", 16),
        bg="red", 
        fg="white",
        width=15,
        height=2,
        command=lambda: show_frame(info_frame),
    ).place(relx=0.5, rely=0.7, anchor="center")  

def create_info_frame():
    for widget in info_frame.winfo_children():
        widget.destroy()

    bg = Label(info_frame, image=info_bg_tk)
    bg.image = info_bg_tk  
    bg.place(x=0, y=0, relwidth=1, relheight=1)

    Label(
        info_frame, 
        text="Informații despre Regimuri Totalitare", 
        font=("Arial Black", 36), 
        bg="#ffffff", 
        fg="black"
        ).grid(row=0, column=0, columnspan=3, pady=40)
    
    Label(
        info_frame, 
        text="Alege un regim pentru a afla mai multe detalii:", 
        font=("Arial", 16), 
        bg="#b3b3b3", 
        fg="white"
        ).grid(row=1, column=0, columnspan=3, pady=20)

    Button(
        info_frame, 
        text="Nazism", 
        bg="#4d4d00", 
        fg="white", 
        width=15, 
        height=1, 
        font=("Arial", 16),
        command=lambda: show_regime_details("Nazism")
        ).grid(row=2, column=0, padx=10)

    Button(
        info_frame, 
        text="Fascism", 
        bg="#264d00", 
        fg="white", 
        width=15, 
        height=1, 
        font=("Arial", 16),
        command=lambda: show_regime_details("Fascism")).grid(row=2, column=1, padx=10)

    Button(
        info_frame, 
        text="Comunism", 
        bg="#661a00", 
        fg="white", 
        width=15, 
        height=1, 
        font=("Arial", 16),
        command=lambda: show_regime_details("Comunism")).grid(row=2, column=2, padx=10)

    Button(
        info_frame, 
        text="Înapoi la Introducere", 
        font=("Arial", 16), 
        bg="#990000", 
        fg="white",
        command=lambda: show_frame(intro_frame)).grid(row=3, column=0, columnspan=3, pady=20)

    info_frame.grid_rowconfigure(0, weight=1)
    info_frame.grid_columnconfigure(0, weight=1)
    info_frame.grid_columnconfigure(1, weight=1)
    info_frame.grid_columnconfigure(2, weight=1)

    Button(info_frame, text="Intrebări suplimentare despre regimurile totalitare", font=("Arial", 16), bg="#DAA520", fg="white", command=lambda: show_frame(ai_chat_frame)).place(relx=0.35, rely=0.62)


def show_regime_details(regime):
    stop_music() # functia opreste muzica

    # dictionar audio
    music_files = {
        "Nazism": r"E:\IstorieSiSocietateInDimensiuneaVirtuala\sounds\nazism.mp3",
        "Fascism": r"E:\IstorieSiSocietateInDimensiuneaVirtuala\sounds\fascism.mp3",
        "Comunism": r"E:\IstorieSiSocietateInDimensiuneaVirtuala\sounds\comunism.mp3"
    }
    music_file = music_files.get(regime)

    if music_file:
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 = loop infinit
        except Exception as e:
            print(f"Nu s-a putut încărca fișierul audio {music_file}: {e}")

    for widget in regime_frame.winfo_children():
        widget.destroy()

    regime_color = regimes_colors.get(regime, "#ffffff")
    regime_frame.config(bg=regime_color)

    bg_label = Label(regime_frame)
    if regime == "Nazism":
        bg_label.config(image=naz_bg_tk)
        bg_label.image = naz_bg_tk
    elif regime == "Fascism":
        bg_label.config(image=fasc_bg_tk)
        bg_label.image = fasc_bg_tk
    elif regime == "Comunism":
        bg_label.config(image=com_bg_tk)
        bg_label.image = com_bg_tk
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Frame pentru controalele audio
    controls_frame = Frame(regime_frame, bg=regime_color)
    controls_frame.pack(pady=10)

    Button(controls_frame, text="▶ Play", font=("Arial", 16),
           command=lambda: pygame.mixer.music.play(-1)).pack(side="left", padx=5)
    Button(controls_frame, text="⏸ Stop", font=("Arial", 16),
           command=stop_music).pack(side="left", padx=5)

    volume_slider = Scale(controls_frame, from_=0, to=1, resolution=0.1,
                          orient="horizontal", label="Volum",
                          command=lambda v: pygame.mixer.music.set_volume(float(v)))
    volume_slider.set(0.5)
    volume_slider.pack(side="left", padx=5)

    regimes_info = {
        "Nazism": """
📜 Caracteristicile regimului:
   ✏️ Supremația rasei ariene  
   ✏️ Antisemitism și persecuția minorităților  
   ✏️ Extindere teritorială agresivă  
   ✏️ Propagandă intensă și cultul personalității lui Hitler  
   ✏️ Economia sub controlul statului  

🔹 Lideri: Adolf Hitler (Germania), Joseph Goebbels (Germania), Hermann Göring (Germania), Heinrich Himmler (Germania)""",
        "Fascism": """
📜 Caracteristicile regimului:
   ✏️ Naționalism extremist  
   ✏️ Cultul liderului suprem  
   ✏️ Militarizare intensivă  
   ✏️ Opoziția față de democrație și liberalism  
   ✏️ Controlul economiei prin stat  

🔹 Lideri: Benito Mussolini (Italia), Francisco Franco (Spania), Ion Antonescu (România)""",
        "Comunism": """
📜 Caracteristicile regimului:
   ✏️ Proprietate comună asupra mijloacelor de producție  
   ✏️ Planificare economică centralizată  
   ✏️ Partid unic și control total asupra statului  
   ✏️ Cenzura și reprimarea opoziției  
   ✏️ Sustine preluarea puterii de catre proletari (muncitori)

🔹 Lideri: Vladimir Lenin (URSS), Iosif Stalin (URSS), Mao Zedong (China), Fidel Castro (Cuba)"""
    }
    
    details_text = regimes_info.get(regime, "Informațiile nu sunt disponibile.")

    Label(regime_frame, text=f"Detalii despre {regime}:", font=("Arial Black", 36),
          bg=regime_color, fg="white").pack(pady=20)

    Label(regime_frame, text=details_text, font=("Arial", 14),
          bg="#e0f7fa", fg="black", wraplength=1000, justify="left").pack(pady=20)

    # Butoane pentru navigare
    Button(regime_frame, text="Înapoi la Informații", font=("Arial", 16),
           bg="#990000", fg="white", command=lambda: [stop_music(), show_frame(info_frame)]).pack(pady=20)

    Button(regime_frame, text=f"Afla mai multe informații despre {regime}",
           font=("Arial", 16), bg="#990000", fg="white",
           command=lambda:[create_addinfo(regime)]).pack(pady=20)

    if regime == "Nazism":
        Button(regime_frame, text="📜 Află mai multe despre Holocaust",
               font=("Arial", 16), bg="#333366", fg="white",
               command=lambda: [show_holocaust_info(), show_frame(holocaust_frame)]).pack(pady=20)

    nazism_images = [
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img1.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img2.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img3.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\carteHitler.jpeg"
    ]
    fascism_images = [
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img5.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\fasces.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img7.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img8.jpg"
    ]
    comunism_images = [
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img9.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img10.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img11.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\img12.jpg"]
  
    # Imagini pentru fiecare regim
    def display_images(paths):
        global img_refs
        img_refs = []
        image_size = (150, 150)

        positions = [
            {"relx": 0.05, "rely": 0.05, "anchor": "nw"},
            {"relx": 0.95, "rely": 0.05, "anchor": "ne"},
            {"relx": 0.1, "rely": 0.9, "anchor": "sw"},
            {"relx": 0.9, "rely": 0.9, "anchor": "se"},
        ]
        for i, path in enumerate(paths):
            try:
                img = Image.open(path)
                img = img.resize(image_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                label = Label(regime_frame, image=photo, bg="#3e3e3e")
                label.image = photo
                label.bind("<Button-1>", lambda event, l=label, p=path: toggle_image_size(l, p))
                image_labels.append((label, path))
                label.place(**positions[i])
            except Exception as e:
                print(f"Eroare la încărcarea imaginii {path}: {e}")


    if regime == "Nazism":
        display_images(nazism_images)
    elif regime == "Fascism":
        display_images(fascism_images)
    elif regime == "Comunism":
        display_images(comunism_images)

    show_frame(regime_frame)



def show_holocaust_info():

    stop_music()

    for widget in holocaust_frame.winfo_children():
        widget.destroy()

    holocaust_image_paths = [
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\holocaust1.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\holocaust2.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\holocaust3.jpg",
        r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\holocaust4.jpg",
    ]

    holocaust_corner_labels = []
    positions = [
        {"relx": 0, "rely": 0, "anchor": "nw"},
        {"relx": 1, "rely": 0, "anchor": "ne"},
        {"relx": 0, "rely": 1, "anchor": "sw"},
        {"relx": 1, "rely": 1, "anchor": "se"},
    ]

    # Titlu
    Label(
        holocaust_frame,
        text="Holocaustul - Crimele regimului nazist",
        font=("Arial Black", 32),
        bg="#2e2e2e",
        fg="white",
    ).place(relx=0.5, rely=0.1, anchor="center")

    Label(
        holocaust_frame,
        text="Holocaustul - Crimele regimului nazist",
        font=("Arial Black", 32),
        bg="#1a1a1a",
        fg="white",
        padx=2,
        pady=2,
    ).place(relx=0.5, rely=0.1, anchor="center")

    info_text = """
        Holocaustul: Un capitol dureros al istoriei
         Definiție:
           Holocaustul a fost genocidul sistematic al evreilor europeni și al altor grupuri persecutate de regimul nazist între 1933 și 1945.
        Măsuri implementate:
           * Naziștii, sub conducerea lui Adolf Hitler, au implementat "Soluția Finală" (planul de exterminare) care a dus la exterminarea a peste 6 milioane de evrei.
           * Lagărele de exterminare precum Auschwitz, Treblinka și Sobibor au fost folosite pentru omorârea sistematică a victimelor.
        Consecințe:
           * Pierderi umane imense și suferință nemărginită.
           * Impact major asupra istoriei mondiale și a conștiinței colective.
    """

    # Frame pentru text 
    text_frame = Frame(holocaust_frame, bg="#2e2e2e", width=640, height=300)  # Dimensiuni reduse
    text_frame.place(relx=0.5, rely=0.55, anchor="center")

    text_label = Label(
        text_frame,
        font=("Arial", 16),
        bg="#333333",
        fg="white",
        text=info_text,
        wraplength=600,
        justify=tk.LEFT, 
        anchor=tk.NW
    )
    text_label.pack(fill=tk.BOTH, expand=True)

    image_label = Label(holocaust_frame, bg="#2e2e2e")  
    image_label.place(relx=0, rely=1, anchor=tk.SW)  

    Button(
        holocaust_frame,
        text="⬅ Înapoi la Nazism",
        font=("Arial", 16),
        bg="#990000",
        fg="white",
        activebackground="#aa0000",  # Culoare la apasare
        relief=tk.RAISED,  # Aspect 3D
        padx=20,  # Padding orizontal
        pady=10,  # Padding vertical
        command=lambda: show_frame(regime_frame)
    ).place(relx=0.5, rely=0.9, anchor="center")

    for path, pos in zip(holocaust_image_paths, positions):
        try:
            img = Image.open(path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(holocaust_frame, image=photo, bg="#2e2e2e", borderwidth=2, relief=tk.SOLID)  
            label.image = photo
            label.place(**pos)

            label.bind("<Button-1>", lambda event, l=label, p=path: toggle_image_size(l, p))
            holocaust_corner_labels.append(label)

            # Efect la hover
            label.bind("<Enter>", lambda event, l=label: l.config(relief=tk.RIDGE))
            label.bind("<Leave>", lambda event, l=label: l.config(relief=tk.SOLID))

        except Exception as e:
            print(f"Error loading image {path}: {e}")

    holocaust_frame.corner_images = holocaust_corner_labels


def create_addinfo(regime): #informatii pentru fiecare regim existent
    stop_music()
    regimes_add_info = {
        "Nazism": """
        📜 Masuri luate de regim:
            ✏️ Legi antisemite și Holocaustul
            ✏️ Control total asupra mass-media și educației
            ✏️ Militarizare și agresiune expansionistă
            ✏️ Economie de război

        📜 Curiozitati:
            ✏️ Hitler a ajuns la putere în 1933 prin alegeri democratice.
            ✏️ Al Doilea Război Mondial a fost cauzat în mare parte de politica expansionistă nazistă.
            ✏️ După înfrângerea Germaniei în 1945, nazismul a fost interzis și condamnat la nivel internațional.
        """,
        
        "Fascism": """
        📜 Masuri luate de regim:
            ✏️ Abolirea partidelor de opoziție
            ✏️ Extinderea puterii militare
            ✏️ Propagandă intensă
            ✏️ Reprimarea libertății de exprimare

        📜 Curiozitati:
            ✏️ Italia fascistă a fost primul regim de acest tip, sub conducerea lui Mussolini.
            ✏️ Spania a fost condusă de un regim fascist până în 1975.
            ✏️ Fascismul s-a inspirat din ideologiile naționaliste și militariste ale secolului XX.
            ✏️ Concordatul cu Biserica Catolica de la Lateran din 1929 in urma caruia Vaticanul devine stat independent.
        """,
        
        "Comunism": """
        📜 Masuri luate de regim:
            ✏️ Colectivizarea agriculturii
            ✏️ Industrializare forțată
            ✏️ Cenzură și propagandă
            ✏️ Reprimarea opozanților politici

        📜 Curiozitati:
            ✏️ Rusia a fost primul stat comunist, înființat în 1917.
            ✏️ Războiul Rece a fost un conflict ideologic major între comunism și capitalism.
            ✏️ China rămâne oficial un stat comunist, deși a introdus elemente de economie de piață.
        """
    }

    for widget in additional_frame.winfo_children():
        widget.destroy()

    # culoarea si textul regimului + in caz ca exista eroare
    regime_text = regimes_add_info.get(regime, "Informațiile nu sunt disponibile.")
    regime_color = regimes_colors.get(regime, "#ffffff")

    # background color in functie de regim
    additional_frame.config(bg=regime_color)

    Label( # frame pentru regim
        additional_frame,
        text=f"Detalii suplimentare despre {regime}",
        font=("Arial Black", 36),
        bg=regime_color,
        fg="white"
    ).pack(pady=20)

    Label(
        additional_frame,
        text=regime_text,
        font=("Arial", 14),
        bg="#e0f7fa",
        fg="black",
        wraplength=1000,
        justify="left"
    ).pack(pady=20)

    Button( # back
        additional_frame,
        text="Înapoi la Detalii Regim",
        font=("Arial", 16),
        bg="#990000",
        fg="white",
        command=lambda: show_frame(regime_frame)
    ).pack(pady=20)

    # butonul de trecut la quizz
    add_quiz_button()

    show_frame(additional_frame) 

# quizz start up
quiz_frame = Frame(root, bg="#3e3e3e", width=1920, height=1080)
quiz_frame.grid(row=0, column=0, sticky="nsew")
quiz_frame.place(relx=0.5, rely=0.5, anchor="center", width=1536, height=864)

def create_quiz_frame():
    global score, current_question
    score = 0
    current_question = 0
    random.shuffle(questions)
    for widget in quiz_frame.winfo_children():
        widget.destroy()

    Label(
        quiz_frame,
        text="Test de cunoștințe",
        font=("Arial Black", 36),
        bg="#3e3e3e",
        fg="white",
        command=lambda: stop_music()
    ).pack(pady=20)

    question_label = Label(quiz_frame, text="", font=("Arial", 16), bg="#3e3e3e", fg="white")
    question_label.pack(pady=10)

    feedback_label = Label(quiz_frame, text="", font=("Arial", 20), bg="#3e3e3e", fg="white")
    feedback_label.pack(pady=10)

    button_frame = Frame(quiz_frame, bg="#3e3e3e")
    button_frame.pack()
    def check_answer(correct):
        if correct:
            feedback_label.config(text="✔ Răspuns corect!", fg="green")
        else:
            feedback_label.config(text="❌ Răspuns greșit!", fg="red")
            feedback_label.place(relx=0.5, rely=1.1, anchor="center")
            feedback_label.after(1623, lambda: correct.place_forget())

    Button(
        quiz_frame,
        text="1920",  # raspuns corect
        font=("Arial", 14),
        bg="#005500",
        fg="white",
        command=lambda: check_answer(True)  # afiseaza corect
    ).pack(pady=5)
    
    Button(
        quiz_frame,
        text="1933",  # raspuns gresit
        font=("Arial", 14),
        bg="#550000",
        fg="white",
        command=lambda: check_answer(False)  # afiseaza gresit
    ).pack(pady=5)
    
    Button( # back
        quiz_frame,
        text="Înapoi la Informații Suplimentare",
        font=("Arial", 16),
        bg="#990000",
        fg="white",
        command=lambda: show_frame(additional_frame)
    ).pack(pady=20)

def add_quiz_button(): #crearea butonului
    Button(
        additional_frame,
        text="Testează-ți cunoștințele",
        font=("Arial", 16),
        bg="#DAA520",
        fg="white",
        command=lambda: [stop_music(), create_quiz_frame(), show_frame(quiz_frame)]  # run si afisare quizz
    ).pack(pady=20)


class QuizApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Istorie Totalitarism")
        self.root.geometry("1920x1080")
        quiz_frame.pack(expand=True)

questions = [
    ("În ce an a fost fondat oficial Partidul Nazist?", [(None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1919.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1920.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1933.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1941.jpg")],0),
    ("Cine a fost principalul lider al regimului nazist?", [("Benito Mussolini", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\benitoMussolini.jpg"), ("Karl Marx", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\karlMarx.jpg"), ("Adolf Hitler", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\adolfHitler.jpg"), ("Iosif Stalin", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\iosifStalin.jpg")], 2),
    ("Simbolul principal al regimului nazist este?", [("Steaua Roșie", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\steauaRosie.jpg"), ("Fasces", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\fasces.jpg"), ("Svastica", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\svastica.jpg"), ("Secera și Ciocanul", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\seceraSiCiocanul.jpg")], 2),
    ("Cine a fost fondatorul fascismului italian?", [("Adolf Hitler", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\adolfHitler.jpg"), ("Francisco Franco",r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\franciscoFranco.jpg"), ("Benito Mussolini", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\benitoMussolini.jpg"), ("Napoleon Bonaparte", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\napoleonBonaparte.jpg")], 2),
    ("Care era doctrina principală a fascismului?", [("Internaționalismul proletar", None), ("Naționalismul extrem și autoritarismul", None), ("Egalitatea absolută", None), ("Liberalismul economic", None)], 1),
    ("Ce an marchează instaurarea oficială a regimului fascist în Italia?", [(None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1919.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1922.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1936.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1945.jpg")], 1),
    ("Cine a scris 'Manifestul Partidului Comunist'?", [("Vladimir Lenin", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\vladimirLenin.jpg"), ("Friedrich Engels și Karl Marx", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\friedrichEngelsKarlMarx.jpg"), ("Nicolae Ceaușescu", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\nicolaeCeausescu.jpg"), ("Mihail Gorbaciov", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\mihailGorbaciov.jpg")], 1),
    ("Ce simbol reprezintă cel mai bine comunismul?", [("Svastica", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\svastica.jpg"), ("Secera și Ciocanul", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\seceraSiCiocanul.jpg"), ("Vulturul cu două capete", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\vulturulCuDouaCapete.png"), ("Crucea celtică", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\cruceaCeltica.png")], 1),
    ("În ce an a fost fondată Uniunea Sovietică?", [(None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1917.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1922.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1936.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1945.jpg")], 1),
    ("Cine a fost primul lider al Uniunii Sovietice?", [("Iosif Stalin", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\iosifStalin.jpg"), ("Vladimir Lenin", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\vladimirLenin.jpg"), ("Leon Troțki", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\leonTrotki.jpg"), ("Nikita Hrușciov", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\nikitaHrusciov.jpg")], 1),
    ("Ce eveniment a marcat începutul celui de-al Doilea Război Mondial?", [("Atacul Japoniei asupra Pearl Harbor", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\ajaph.jpg"), ("Invadarea Poloniei de către Germania", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\ipdcg.jpg"), ("Bătălia de la Stalingrad", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\blds.jpg"), ("Revoluția Rusă", r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\revolutiaRusa.jpg")], 1),
    ("Când a căzut Zidul Berlinului?", [(None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1985.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1989.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1991.jpg"), (None, r"E:\IstorieSiSocietateInDimensiuneaVirtuala\images\1995.jpg")], 1)
]

current_question = 0 # initializare contor pentru intrebari
score = 0 # initialezare scor

def create_quiz_frame(): # frameul de la quiz
    global score, current_question
    score = 0
    current_question = 0

    random.shuffle(questions)

    for widget in quiz_frame.winfo_children():
        widget.destroy()
    
    Label(
        quiz_frame,
        text="Test de cunoștințe",
        font=("Arial Black", 36),
        bg="#3e3e3e",
        fg="white"
    ).pack(pady=20)

    question_label = Label(quiz_frame, text="", font=("Arial", 16), bg="#3e3e3e", fg="white")
    question_label.pack(pady=10)

    progress_label = Label(quiz_frame, text="", font=("Arial", 14), bg="#3e3e3e", fg="white")
    progress_label.pack(pady=5)

    feedback_label = Label(quiz_frame, text="", font=("Arial", 20), bg="#3e3e3e", fg="white")
    feedback_label.pack(pady=10)

    button_frame = Frame(quiz_frame, bg="#3e3e3e")
    button_frame.pack()

    def animate_feedback(correct): # animatie pentru feedback la raspunsuri
        color = "green" if correct else "red"
        text = "✔ Corect!" if correct else "❌ Greșit!"
        feedback_label.config(text=text, fg=color)

        def play_sound(file_path):
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

        if correct:
            play_sound(r"E:\IstorieSiSocietateInDimensiuneaVirtuala\sounds\correct.mp3")
        else:
            play_sound(r"E:\IstorieSiSocietateInDimensiuneaVirtuala\sounds\wrong.mp3")

        for _ in range(3):
            feedback_label.config(font=("Arial", 24, "bold"))
            quiz_frame.update()
            time.sleep(0.2)
            feedback_label.config(font=("Arial", 20))
            quiz_frame.update()
            time.sleep(0.2)

        feedback_label.after(1500, lambda: feedback_label.config(text=""))

    def load_question():
        global current_question
        if current_question < len(questions):
            question, answers_with_images, correct_index = questions[current_question]

            shuffeled_answers = list(enumerate(answers_with_images))
            random.shuffle(shuffeled_answers)

            new_correct_index = [idx for idx, (orig_idx, _) in enumerate(shuffeled_answers) if orig_idx == correct_index][0]

            question_label.config(text=question)

            progress_label.config(text=f"{current_question + 1}/{len(questions)}")

            for widget in button_frame.winfo_children():
                widget.destroy()

            for i, item in enumerate(shuffeled_answers):
                original_index, answer_tuple = item

                if isinstance(answer_tuple, tuple): # initial trebuia sa fie tuple (sa aiba si img si txt), acum daca are doar una dintre good job
                    if len(answer_tuple) == 2: 
                        answer_text, image_path = answer_tuple
                        display_image = True
                    elif len(answer_tuple) == 1:
                        answer_text = answer_tuple[0]
                        image_path = None
                        display_image = False
                    else:
                        print(f"Eroare: Tuplu invalid pentru întrebarea {current_question}. Trebuie să aibă 1 sau 2 elemente.")
                        continue # throw error in cazu in care variantele de raspuns sunt nule

                    try:
                        if image_path and display_image:
                            image = Image.open(image_path)
                            image = image.resize((75, 75), Image.LANCZOS)
                            photo = ImageTk.PhotoImage(image)

                            button = Button(
                                button_frame,
                                image=photo,
                                compound=tk.LEFT,
                                text=answer_text,
                                font=("Arial", 14),
                                bg="#0000CD",
                                fg="white",
                                command=lambda idx=i: check_answer(idx, new_correct_index),
                                anchor="w"
                            )
                            button.image = photo
                        else:
                            button = Button(
                                button_frame,
                                text=answer_text,
                                font=("Arial", 14),
                                bg="#0000CD",
                                fg="white",
                                command=lambda idx=i: check_answer(idx, new_correct_index),
                                anchor="w"
                            )

                        button.pack(pady=5, padx=20, fill="x", anchor="center", expand=True)

                    except FileNotFoundError:
                        print(f"Eroare: Fișierul imagine '{image_path}' nu a fost găsit. Verifică calea și existența fișierului.")
                        button = Button(
                            button_frame,
                            text=answer_text,
                            font=("Arial", 14),
                            bg="#005500",
                            fg="white",
                            command=lambda idx=i: check_answer(idx, new_correct_index)
                        )
                        button.pack(pady=5, padx=20, fill="x", anchor="center", expand=True)

                else:
                    print(f"Eroare: Date incorecte pentru întrebarea {current_question}. Trebuie să fie un tuplu.")

        else:
            show_final_screen()

    def check_answer(selected_index, correct_index): # verifica si trece la urm intrebare
        global current_question, score
        correct = selected_index == correct_index
        if correct:
            score += 1
        animate_feedback(correct)  
        current_question += 1
        quiz_frame.after(1000, load_question)  

    def show_final_screen():
        for widget in quiz_frame.winfo_children():
            widget.destroy()

        total_questions = len(questions)
        percentage = (score / total_questions) * 100

        if percentage >= 90:
            level = "🌟 Expert, se vede ca ai invatat!"
            color = "cyan"
        elif percentage >= 75:
            level = "⭐ Avansat, felicitari!"
            color = "green"
        elif percentage >= 50:
            level = "🌐 Intermediar"
            color = "orange"
        elif percentage >=25:
            level = "📉 Se putea mai bine, nu ai trecut testul"
            color = "purple"
        else: 
            level = "🔻 Mai parcurge o data materialul"
            color = "red"

        Label(
            quiz_frame,
            text=f"🎉 Felicitări! Ai terminat testul!\nScor: {score}/{total_questions} ({percentage:.2f}%)",
            font=("Arial Black", 24),
            bg="#3e3e3e",
            fg="white"
        ).pack(pady=20)

        Label(
            quiz_frame,
            text=f"Nivel: {level}",
            font=("Arial", 20),
            bg="#3e3e3e",
            fg=color
        ).pack(pady=10)

        Button(
            quiz_frame,
            text="🔄 Reîncearcă testul", # try again :33
            font=("Arial", 16),
            bg="#005500",
            fg="white",
            command=create_quiz_frame
        ).place(relx=0.5, rely=0.75, anchor="center")

        Button(
            quiz_frame,
            text="⬅ Înapoi la Regimuri",
            font=("Arial", 16),
            bg="#990000",
            fg="white",
            command=lambda: show_frame(info_frame)
        ).place(relx=0.5, rely=0.86, anchor="center")
    load_question()
   
create_intro_frame()
create_info_frame()

loading_screen(root)
root.after(11500, lambda: show_frame(loading_frame2))
root.after(22000, lambda: show_frame(intro_frame))

add_logo_to_frame(loading_frame)
add_logo_to_frame(loading_frame2)
add_logo_to_frame(intro_frame)



root.mainloop()




