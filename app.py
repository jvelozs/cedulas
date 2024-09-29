from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_cedula', methods=['POST'])
def buscar_cedula():
    data = request.json
    cedula = data['cedula']

    # Configurar Chrome en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://si.secap.gob.ec/sisecap/logeo_web/usuario_nuevo.php")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tidentificacion"))
        )
        select = Select(driver.find_element(By.ID, "tidentificacion"))
        select.select_by_value("1")

        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "documento"))
        )
        input_field.clear()
        input_field.send_keys(cedula)
        input_field.send_keys("\t")

        apellidos = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "apellidos"))
        ).get_attribute("value")
        nombres = driver.find_element(By.ID, "nombres").get_attribute("value")
        fecha_nacimiento = driver.find_element(By.ID, "fecha_nacimiento").get_attribute("value")
        estado_civil = Select(driver.find_element(By.ID, "estado_civil")).first_selected_option.text

    finally:
        driver.quit()

    return jsonify({
        "apellidos": apellidos,
        "nombres": nombres,
        "fecha_nacimiento": fecha_nacimiento,
        "estado_civil": estado_civil
    })

if __name__ == '__main__':
    app.run(debug=True)
