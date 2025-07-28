import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

# Adicione o caminho do ffmpeg manualmente aqui, se necessário
# Exemplo no Windows: r'C:\ffmpeg\bin'
ffmpeg_location = r'C:\Software\ffmpeg\bin'  # Altere o caminho se necessário ou deixe vazio se estiver no Path do sistema

# Função para atualizar o status dos vídeos na interface
def update_status(video_title, status):
    listbox.insert(tk.END, f"{video_title}: {status}")
    listbox.yview(tk.END)  # Rola a listbox para o final

# Função de hook de progresso
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('percent', 0)
        progress_bar['value'] = percent
        janela.update_idletasks()  # Atualiza a interface enquanto baixa

    elif d['status'] == 'finished':
        download_label.config(text="Download concluído. Convertendo o arquivo...")

# Função para baixar vídeo ou playlist
def download_video_as_mp3(youtube_url, output_path, is_playlist=False):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s' if is_playlist else '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': not is_playlist,  # Define se vai baixar uma playlist inteira ou um único vídeo
            'ffmpeg_location': ffmpeg_location if ffmpeg_location else None,  # Adiciona o local do ffmpeg se especificado
            'progress_hooks': [progress_hook],  # Adiciona o hook de progresso
            'ignoreerrors': True  # Ignora vídeos indisponíveis
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            
            if 'entries' in info:  # Se for uma playlist
                for entry in info['entries']:
                    try:
                        video_title = entry['title']
                        update_status(video_title, "Baixando...")
                        ydl.download([entry['webpage_url']])
                        update_status(video_title, "Baixado com sucesso!")
                    except Exception as e:
                        update_status(video_title, f"Erro: {str(e)}")
            else:  # Se for um único vídeo
                try:
                    video_title = info['title']
                    update_status(video_title, "Baixando...")
                    ydl.download([youtube_url])
                    update_status(video_title, "Baixado com sucesso!")
                except Exception as e:
                    update_status(video_title, f"Erro: {str(e)}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para escolher pasta de saída
def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, pasta)

# Função para iniciar o download
def iniciar_download():
    youtube_url = url_entry.get().strip()
    output_path = output_entry.get().strip()
    is_playlist = playlist_var.get()

    if not youtube_url or not output_path:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    download_video_as_mp3(youtube_url, output_path, is_playlist)

# Configurando a janela principal
janela = tk.Tk()
janela.title("YouTube to MP3 Downloader")
janela.geometry("600x400")
janela.configure(bg="#f0f0f0")

# Título
titulo_label = tk.Label(janela, text="YouTube to MP3 Downloader", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
titulo_label.pack(pady=10)

# Campo URL do YouTube
url_label = tk.Label(janela, text="URL do vídeo ou playlist:", bg="#f0f0f0")
url_label.pack(pady=5)
url_entry = tk.Entry(janela, width=50)
url_entry.pack(pady=5)

# Campo para escolher a pasta de saída
output_label = tk.Label(janela, text="Salvar em:", bg="#f0f0f0")
output_label.pack(pady=5)
output_frame = tk.Frame(janela)
output_frame.pack(pady=5)

output_entry = tk.Entry(output_frame, width=40)
output_entry.pack(side=tk.LEFT, padx=5)
escolher_button = tk.Button(output_frame, text="Escolher Pasta", command=escolher_pasta)
escolher_button.pack(side=tk.LEFT)

# Checkbox para selecionar se é uma playlist
playlist_var = tk.BooleanVar()
playlist_checkbox = tk.Checkbutton(janela, text="Baixar playlist inteira", variable=playlist_var, bg="#f0f0f0")
playlist_checkbox.pack(pady=5)

# Barra de progresso
progress_bar = ttk.Progressbar(janela, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Label de status do download
download_label = tk.Label(janela, text="Aguardando download...", bg="#f0f0f0")
download_label.pack(pady=5)

# Listbox para mostrar o status dos vídeos baixados
listbox_frame = tk.Frame(janela)
listbox_frame.pack(pady=5)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(listbox_frame, height=10, width=70, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=listbox.yview)

# Botão de iniciar download
download_button = tk.Button(janela, text="Baixar MP3", font=("Helvetica", 12, "bold"), bg="#4caf50", fg="white", command=iniciar_download)
download_button.pack(pady=20)

# Executando a interface gráfica
janela.mainloop()

