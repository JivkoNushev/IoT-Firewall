import subprocess

HOST = "192.168.113.134"
INTERVAL = 1 

def ping_host(host="localhost", interval=1):
    try:
        import platform
        system = platform.system()
        
        if system == "Windows":
            cmd = ["ping", "-w", "-n", 1, str(interval * 1000), host]
        else: 
            cmd = ["ping", "-i", str(interval), host]

        output = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return output.stdout
    except subprocess.CalledProcessError as e:
        return f"Ping failed: {e.stderr}"

if __name__ == "__main__":
    result = ping_host(host=HOST, interval=INTERVAL)
    print(result)