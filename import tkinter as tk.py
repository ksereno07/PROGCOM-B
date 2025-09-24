import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class TablasMultiplicar:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Tablas Divertidas 🌟")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f8ff')
        
        # Variables del juego
        self.current_table = 1
        self.question_number = 1
        self.score = 0
        self.correct_answers = 0
        self.game_active = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#f0f8ff')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="🌟 Tablas Divertidas 🌟", 
            font=('Arial', 24, 'bold'),
            fg='#ff6b6b',
            bg='#f0f8ff'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="¡Aprende las tablas de multiplicar jugando!",
            font=('Arial', 12),
            fg='#666666',
            bg='#f0f8ff'
        )
        subtitle_label.pack(pady=5)
        
        # Frame para botones de tablas
        self.buttons_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.buttons_frame.pack(pady=20)
        
        # Crear botones de tablas (1-10)
        self.table_buttons = []
        for i in range(10):
            row = i // 5
            col = i % 5
            
            btn = tk.Button(
                self.buttons_frame,
                text=str(i + 1),
                font=('Arial', 16, 'bold'),
                width=4,
                height=2,
                bg='#ff6b6b',
                fg='white',
                border=0,
                cursor='hand2',
                command=lambda x=i+1: self.select_table(x)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.table_buttons.append(btn)
        
        # Barra de progreso
        self.progress_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.progress_frame.pack(pady=10, fill='x', padx=50)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack()
        self.progress_frame.pack_forget()  # Ocultar inicialmente
        
        # Área del juego
        self.game_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.game_frame.pack(pady=30)
        
        # Pregunta
        self.question_label = tk.Label(
            self.game_frame,
            text="Selecciona una tabla para empezar 🎯",
            font=('Arial', 20, 'bold'),
            fg='#333333',
            bg='#f0f8ff'
        )
        self.question_label.pack(pady=20)
        
        # Campo de respuesta
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(
            self.game_frame,
            textvariable=self.answer_var,
            font=('Arial', 18),
            width=10,
            justify='center',
            relief='solid',
            bd=2
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.pack_forget()  # Ocultar inicialmente
        
        # Botones de acción
        self.buttons_action_frame = tk.Frame(self.game_frame, bg='#f0f8ff')
        self.buttons_action_frame.pack(pady=10)
        
        self.check_button = tk.Button(
            self.buttons_action_frame,
            text="🚀 Verificar",
            font=('Arial', 14, 'bold'),
            bg='#4ecdc4',
            fg='white',
            padx=20,
            pady=10,
            border=0,
            cursor='hand2',
            command=self.check_answer
        )
        
        self.next_button = tk.Button(
            self.buttons_action_frame,
            text="➡️ Siguiente",
            font=('Arial', 14, 'bold'),
            bg='#4ecdc4',
            fg='white',
            padx=20,
            pady=10,
            border=0,
            cursor='hand2',
            command=self.next_question
        )
        
        # Feedback
        self.feedback_label = tk.Label(
            self.game_frame,
            text="",
            font=('Arial', 14, 'bold'),
            bg='#f0f8ff',
            fg='#333333',
            wraplength=600
        )
        self.feedback_label.pack(pady=20)
        
        # Área de puntuación
        self.score_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.score_frame.pack(pady=20)
        
        # Crear cajas de puntuación
        self.create_score_box("Puntos", "score_value")
        self.create_score_box("Correctas", "correct_value")
        self.create_score_box("Pregunta", "current_value")
        
        self.score_frame.pack_forget()  # Ocultar inicialmente
        
        # Binding para Enter
        self.root.bind('<Return>', lambda e: self.check_answer() if self.game_active else None)
        
    def create_score_box(self, title, var_name):
        box_frame = tk.Frame(self.score_frame, bg='white', relief='solid', bd=2)
        box_frame.pack(side='left', padx=20, pady=10, fill='both')
        
        title_label = tk.Label(
            box_frame,
            text=title,
            font=('Arial', 10),
            fg='#666666',
            bg='white'
        )
        title_label.pack(pady=5)
        
        value_label = tk.Label(
            box_frame,
            text="0",
            font=('Arial', 18, 'bold'),
            fg='#4ecdc4',
            bg='white',
            width=8
        )
        value_label.pack(pady=5)
        
        # Guardar referencia al label
        setattr(self, var_name, value_label)
    
    def select_table(self, table_number):
        self.current_table = table_number
        self.question_number = 1
        self.score = 0
        self.correct_answers = 0
        self.game_active = True
        
        # Resaltar botón seleccionado
        for i, btn in enumerate(self.table_buttons):
            if i + 1 == table_number:
                btn.configure(bg='#4ecdc4')
            else:
                btn.configure(bg='#ff6b6b')
        
        # Mostrar elementos del juego
        self.progress_frame.pack(pady=10, fill='x', padx=50)
        self.answer_entry.pack(pady=10)
        self.check_button.pack(side='left', padx=5)
        self.score_frame.pack(pady=20)
        
        # Ocultar botón siguiente inicialmente
        self.next_button.pack_forget()
        
        # Empezar juego
        self.show_question()
        self.update_score()
        
        # Enfocar campo de entrada
        self.answer_entry.focus_set()
    
    def show_question(self):
        question_text = f"{self.current_table} × {self.question_number} = ?"
        self.question_label.configure(text=question_text)
        self.answer_var.set("")
        self.feedback_label.configure(text="", bg='#f0f8ff')
        
        # Actualizar progreso
        progress = (self.question_number / 10) * 100
        self.progress_bar['value'] = progress
        self.current_value.configure(text=f"{self.question_number}/10")
    
    def check_answer(self):
        if not self.game_active:
            return
            
        try:
            user_answer = int(self.answer_var.get())
        except ValueError:
            self.show_feedback("¡Escribe un número! 🤔", "incorrect")
            return
        
        correct_answer = self.current_table * self.question_number
        
        if user_answer == correct_answer:
            feedback_text = f"¡Muy bien! 🎉 {self.current_table} × {self.question_number} = {correct_answer}"
            self.show_feedback(feedback_text, "correct")
            self.score += 10
            self.correct_answers += 1
        else:
            feedback_text = f"¡Intenta otra vez! 😊 La respuesta es {correct_answer}"
            self.show_feedback(feedback_text, "incorrect")
        
        # Cambiar botones
        self.check_button.pack_forget()
        self.next_button.pack(side='left', padx=5)
        
        self.update_score()
    
    def show_feedback(self, text, type_feedback):
        self.feedback_label.configure(text=text)
        if type_feedback == "correct":
            self.feedback_label.configure(bg='#2ecc71', fg='white')
        else:
            self.feedback_label.configure(bg='#e74c3c', fg='white')
    
    def next_question(self):
        if self.question_number < 10:
            self.question_number += 1
            self.next_button.pack_forget()
            self.check_button.pack(side='left', padx=5)
            self.show_question()
            self.answer_entry.focus_set()
        else:
            self.end_game()
    
    def end_game(self):
        self.game_active = False
        percentage = round((self.correct_answers / 10) * 100)
        
        if percentage >= 80:
            message = f"¡EXCELENTE! 🌟 Obtuviste {percentage}% - ¡Eres genial!"
        elif percentage >= 60:
            message = f"¡MUY BIEN! 👏 Obtuviste {percentage}% - ¡Sigue así!"
        else:
            message = f"¡BUEN INTENTO! 💪 Obtuviste {percentage}% - ¡Practica más!"
        
        self.question_label.configure(text="🎊 ¡Tabla completada! 🎊")
        self.show_feedback(message, "correct")
        
        # Ocultar botones y entrada
        self.check_button.pack_forget()
        self.next_button.pack_forget()
        self.answer_entry.pack_forget()
        
        # Mostrar mensaje final
        messagebox.showinfo("¡Juego Completado!", message)
        
        # Reiniciar después de cerrar el mensaje
        self.reset_game()
    
    def reset_game(self):
        # Resetear botones de tabla
        for btn in self.table_buttons:
            btn.configure(bg='#ff6b6b')
        
        # Ocultar elementos del juego
        self.progress_frame.pack_forget()
        self.score_frame.pack_forget()
        
        # Resetear textos
        self.question_label.configure(text="Selecciona una tabla para empezar 🎯")
        self.feedback_label.configure(text="", bg='#f0f8ff')
        
        self.game_active = False
    
    def update_score(self):
        self.score_value.configure(text=str(self.score))
        self.correct_value.configure(text=str(self.correct_answers))

def main():
    root = tk.Tk()
    game = TablasMultiplicar(root)
    root.mainloop()

if __name__ == "__main__":
    main()