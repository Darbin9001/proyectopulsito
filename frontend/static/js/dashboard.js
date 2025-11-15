const bpmCtx = document.getElementById('bpmChart').getContext('2d');
const tempCtx = document.getElementById('tempChart').getContext('2d');
const alertPanel = document.getElementById('alert-panel');
const alertMessage = document.getElementById('alert-message');
const alertSound = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
const searchBtn = document.getElementById('search-btn');
const cedulaInput = document.getElementById('cedula-input');
const patientInfo = document.getElementById('patient-info');
const patientCedula = document.getElementById('patient-cedula');
const statusMessage = document.getElementById('status-message');
const statusText = document.getElementById('status-text');
const lastBpmElement = document.getElementById('last-bpm');
const lastTempElement = document.getElementById('last-temp');

let currentCedula = null;
let updateInterval = null;

// Configuración de gráficas
let bpmChart = new Chart(bpmCtx, {
  type: 'line',
  data: { 
    labels: [], 
    datasets: [{ 
      label: 'BPM', 
      data: [], 
      borderColor: '#f44336',
      backgroundColor: 'rgba(244, 67, 54, 0.1)',
      tension: 0.4,
      fill: true
    }] 
  },
  options: { 
    responsive: true,
    maintainAspectRatio: true,
    scales: { 
      y: { 
        beginAtZero: false,
        min: 40,
        max: 120
      } 
    },
    plugins: {
      legend: {
        display: true,
        position: 'top'
      }
    }
  }
});

let tempChart = new Chart(tempCtx, {
  type: 'line',
  data: { 
    labels: [], 
    datasets: [{ 
      label: 'Temperatura °C', 
      data: [], 
      borderColor: '#ff9800',
      backgroundColor: 'rgba(255, 152, 0, 0.1)',
      tension: 0.4,
      fill: true
    }] 
  },
  options: { 
    responsive: true,
    maintainAspectRatio: true,
    scales: { 
      y: { 
        beginAtZero: false,
        min: 35,
        max: 40
      } 
    },
    plugins: {
      legend: {
        display: true,
        position: 'top'
      }
    }
  }
});

// Función para mostrar mensajes de estado
function showStatus(message, isError = false) {
  statusText.textContent = message;
  statusMessage.classList.remove('hidden', 'error');
  if (isError) {
    statusMessage.classList.add('error');
  }
  setTimeout(() => {
    statusMessage.classList.add('hidden');
  }, 4000);
}

// Función para actualizar las gráficas
async function updateCharts() {
  if (!currentCedula) return;

  try {
    const res = await fetch(`/api/data/${currentCedula}`);
    
    if (!res.ok) {
      if (res.status === 404) {
        showStatus('No se encontró historial para esta cédula', true);
        clearCharts();
        return;
      }
      throw new Error(`Error ${res.status}`);
    }

    const data = await res.json();

    // La API devuelve un objeto con la estructura: {cedula, total_registros, registros_mostrados, historial: [...]}
    if (data.historial && Array.isArray(data.historial) && data.historial.length > 0) {
      const historial = data.historial;
      
      const timestamps = historial.map(d => {
        // El timestamp ya viene en formato "2025-10-30 23:13:15"
        const parts = d.timestamp.split(' ')[1]; // Obtener solo la hora
        return parts.substring(0, 5); // HH:MM
      });
      
      const bpm = historial.map(d => d.datos.ritmo_cardiaco);
      const temp = historial.map(d => d.datos.temperatura);

      // Actualizar gráficas
      bpmChart.data.labels = timestamps;
      bpmChart.data.datasets[0].data = bpm;
      tempChart.data.labels = timestamps;
      tempChart.data.datasets[0].data = temp;

      bpmChart.update();
      tempChart.update();

      // Actualizar valores actuales
      const lastBpm = bpm[bpm.length - 1];
      const lastTemp = temp[temp.length - 1];
      lastBpmElement.textContent = lastBpm;
      lastTempElement.textContent = lastTemp.toFixed(1);

      // Verificar alertas
      checkAlerts(lastBpm, lastTemp);
      
      showStatus(`Datos actualizados - ${data.total_registros} registros totales (mostrando ${data.registros_mostrados})`);
    } else {
      showStatus('No hay datos disponibles para esta cédula', true);
      clearCharts();
    }
  } catch (error) {
    console.error("Error al obtener datos:", error);
    showStatus('Error al conectar con el servidor', true);
  }
}

// Función para limpiar las gráficas
function clearCharts() {
  bpmChart.data.labels = [];
  bpmChart.data.datasets[0].data = [];
  tempChart.data.labels = [];
  tempChart.data.datasets[0].data = [];
  bpmChart.update();
  tempChart.update();
  lastBpmElement.textContent = '--';
  lastTempElement.textContent = '--';
  alertPanel.classList.add('hidden');
}

// Función para verificar alertas
function checkAlerts(bpm, temp) {
  let messages = [];
  
  if (bpm > 100) messages.push(`Ritmo cardíaco alto (${bpm} BPM)`);
  if (bpm < 50) messages.push(`Ritmo cardíaco bajo (${bpm} BPM)`);
  if (temp > 37.8) messages.push(`Temperatura elevada (${temp.toFixed(1)}°C)`);
  if (temp < 35.5) messages.push(`Temperatura baja (${temp.toFixed(1)}°C)`);

  if (messages.length > 0) {
    alertMessage.textContent = messages.join(' | ');
    alertPanel.classList.remove('hidden');
    alertSound.play().catch(err => console.log('No se pudo reproducir el sonido'));
  } else {
    alertPanel.classList.add('hidden');
  }
}

// Función para iniciar el monitoreo
function startMonitoring(cedula) {
  currentCedula = cedula;
  patientCedula.textContent = cedula;
  patientInfo.classList.remove('hidden');
  
  // Limpiar intervalo anterior si existe
  if (updateInterval) {
    clearInterval(updateInterval);
  }
  
  // Primera actualización inmediata
  updateCharts();
  
  // Actualizar cada 5 segundos
  updateInterval = setInterval(updateCharts, 5000);
}

// Event listener para el botón de búsqueda
searchBtn.addEventListener('click', () => {
  const cedula = cedulaInput.value.trim();
  
  if (!cedula) {
    showStatus('Por favor ingrese una cédula', true);
    return;
  }
  
  if (!/^\d+$/.test(cedula)) {
    showStatus('La cédula debe contener solo números', true);
    return;
  }
  
  startMonitoring(cedula);
});

// Event listener para presionar Enter en el input
cedulaInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    searchBtn.click();
  }
});

// Limpiar intervalo al cerrar la página
window.addEventListener('beforeunload', () => {
  if (updateInterval) {
    clearInterval(updateInterval);
  }
});