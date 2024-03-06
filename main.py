import subprocess
import json

def run_docker_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except Exception as e:
        print(f"Erreur lors de l'exécution de la commande: {e}")
        return None

def print_result(step, condition):
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    status = "OK" if condition else "NOK"
    color = GREEN if condition else RED
    print(f"{color}{step}: {status}{RESET}")

score = 0

image_downloaded = run_docker_command("docker images -q registry.gitlab.com/0xbochi/docker_evaluation:01")
print_result("1.1", image_downloaded is not None and image_downloaded != "")
score += 1 if image_downloaded is not None and image_downloaded != "" else 0

docker01_info = run_docker_command("docker inspect docker01")
docker01 = json.loads(docker01_info)[0] if docker01_info else None
docker01_port_ok = "8091" in json.dumps(docker01["NetworkSettings"]["Ports"]) if docker01 else False
print_result("1.2", docker01_port_ok)
score += 1 if docker01_port_ok else 0

docker02_info = run_docker_command("docker inspect docker02")
docker02 = json.loads(docker02_info)[0] if docker02_info else None
docker02_port_ok = "8092" in json.dumps(docker02["NetworkSettings"]["Ports"]) if docker02 else False
docker02_env_ok = "container4life=true" in json.dumps(docker02["Config"]["Env"]) if docker02 else False
print_result("1.3", docker02_port_ok and docker02_env_ok)
score += 1 if docker02_port_ok and docker02_env_ok else 0

network_info = run_docker_command("docker network ls --format '{{.Name}}' | grep mon_reseau_flask")
network_ok = network_info == "mon_reseau_flask"
print_result("2.1", network_ok)
score += 1 if network_ok else 0

docker03_info = run_docker_command("docker inspect docker03")
docker03 = json.loads(docker03_info)[0] if docker03_info else None
docker03_network_ok = "mon_reseau_flask" in json.dumps(docker03["NetworkSettings"]["Networks"]) if docker03 else False
docker03_env_ok = "ZG9uJ3QgdHJ5IHRvIG91dHNtYXJ0IG1lIHlvdW5nIHN0dWRlbnQ=" in json.dumps(docker03["Config"]["Env"]) if docker03 else False
print_result("2.2", docker03_network_ok and docker03_env_ok)
score += 1 if docker03_network_ok and docker03_env_ok else 0

image_created = run_docker_command("docker images -q superImage:latest")
print_result("3.1", image_created is not None and image_created != "")
score += 1 if image_created is not None and image_created != "" else 0

nginxperso_info = run_docker_command("docker inspect nginxperso")
nginxperso = json.loads(nginxperso_info)[0] if nginxperso_info else None
nginxperso_port_ok = "8094" in json.dumps(nginxperso["NetworkSettings"]["Ports"]) if nginxperso else False
print_result("3.2", nginxperso_port_ok)
score += 1 if nginxperso_port_ok else 0

final_score = (score / 8) * 20  # Il y a 8 vérifications, chacune valant 2.5 points
print(f"Note finale: {final_score} / 20")
