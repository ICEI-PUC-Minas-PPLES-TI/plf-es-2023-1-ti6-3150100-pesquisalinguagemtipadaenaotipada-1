import os
import shutil
import subprocess
import urllib.request
import zipfile
import sys

# Define a URL do arquivo do SonarScanner
url = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.6.2.2472.zip"

# Define o nome do arquivo a ser baixado
filename = "sonar-scanner.zip"

# Baixa o arquivo do SonarScanner
urllib.request.urlretrieve(url, filename)

# Extrai o conteúdo do arquivo zip
with zipfile.ZipFile(filename, "r") as zip_ref:
    zip_ref.extractall()

# Remove o arquivo zip
os.remove(filename)

# Define o caminho do diretório bin do SonarScanner
sonar_scanner_path = os.path.join(
    os.getcwd(), "sonar-scanner-4.6.2.2472", "bin")

# Adiciona o diretório bin do SonarScanner ao PATH do sistema
if "win" in sys.platform:
    os.environ["PATH"] += os.pathsep + sonar_scanner_path
else:
    shutil.copy(os.path.join(sonar_scanner_path,
                "sonar-scanner"), "/usr/local/bin/")

# Define o caminho do arquivo de configuração do SonarScanner
sonar_scanner_properties_path = os.path.join(
    os.getcwd(), "sonar-scanner-4.6.2.2472", "conf", "sonar-project.properties")

# Verifica se o arquivo de configuração existe e modifica o valor da porta do servidor, se necessário
if os.path.isfile(sonar_scanner_properties_path):
    with open(sonar_scanner_properties_path, "r") as f:
        content = f.read()
        if "sonar.host.url" not in content:
            content += "\nsonar.host.url=http://localhost:9000\n"
        if "sonar.sourceEncoding" not in content:
            content += "\nsonar.sourceEncoding=UTF-8\n"
    with open(sonar_scanner_properties_path, "w") as f:
        f.write(content)

command = 'sonar-scanner.bat -D"sonar.projectKey=tis6-test" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.token=sqp_60a7ba5cb8d91095b39b110176c3595d6ea9ca56"'
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

print(output.decode())
