import subprocess
import platform


#Runs both WhicperMain.py and app.py in new terminals
def run_in_new_terminal(command):
    system = platform.system()
    if system == "Linux":
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command])
    elif system == "Darwin":  # macOS
        subprocess.Popen(["open", "-a", "Terminal", command])
    elif system == "Windows":
        subprocess.Popen(["cmd.exe", "/c", command])

def main():
    # Whisper betiğini yeni terminalde çalıştırma
    run_in_new_terminal("python WhisperMain.py")
    # Flask betiğini yeni terminalde çalıştırma
    run_in_new_terminal("python app.py")

if __name__ == "__main__":
    main()
