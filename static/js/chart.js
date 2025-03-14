/*
 * static/js/chart.js
 *
 * Este script realiza a requisição AJAX para o endpoint /api/chart_data,
 * interpreta os dados JSON recebidos e utiliza Chart.js para renderizar:
 *  - Um gráfico de barras agrupadas para comparar os valores reais versus os esperados
 *    de tempo por metro quadrado para cada tarefa.
 *  - Um gráfico de barras agrupadas para comparar os valores reais versus os esperados
 *    de consumo por metro quadrado para cada tarefa.
 *  - Um gráfico de linhas para exibir a evolução semanal do tempo por m².
 *  - Um gráfico de linhas para exibir a evolução mensal do tempo por m².
 *
 * As funções estão modularizadas para facilitar a manutenção e o entendimento.
 */

/**
 * Realiza a requisição para o endpoint /api/chart_data e retorna os dados JSON.
 */
function fetchChartData() {
  return fetch('/api/chart_data')
    .then(response => response.json())
    .then(data => {
      console.log("Dados recebidos da API:", data); // Log dos dados recebidos
      return data;
    })
    .catch(error => {
      console.error("Erro ao buscar dados da API:", error);
      return null;
    });
}

/**
 * Renderiza um gráfico de barras agrupadas comparando o tempo real versus o esperado por m² para cada tarefa.
 * @param {Array} tarefasIndividuais - Lista de tarefas individuais com seus indicadores.
 */
function renderGroupedBarChart(tarefasIndividuais) {
  console.log("Renderizando gráfico de tempo por m² com dados:", tarefasIndividuais);
  const labels = [];
  const realTimeData = [];
  const expectedTimeData = [];
  
  tarefasIndividuais.forEach(item => {
    labels.push(`${item.tarefa} (ID ${item.id})`);
    // Converter os valores para números, se necessário
    const tempoReal = parseFloat(item.tempo_por_m2) || 0;
    const tempoEsperado = parseFloat(item.expected_tempo_por_m2) || 0;
    realTimeData.push(tempoReal);
    expectedTimeData.push(tempoEsperado);
  });
  
  const canvas = document.getElementById('groupedBarChart');
  if (!canvas) {
    console.error("Canvas com id 'groupedBarChart' não encontrado.");
    return;
  }
  const ctx = canvas.getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Tempo Real por m² (minutos)',
          data: realTimeData,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: 'Tempo Esperado por m² (minutos)',
          data: expectedTimeData,
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

/**
 * Renderiza um gráfico de barras agrupadas comparando o consumo real versus o esperado por m² para cada tarefa.
 * Supõe que cada tarefa possua, no dicionário, apenas um material relevante para a comparação.
 * @param {Array} tarefasIndividuais - Lista de tarefas individuais com seus indicadores.
 */
function renderGroupedConsumptionChart(tarefasIndividuais) {
  console.log("Renderizando gráfico de consumo por m² com dados:", tarefasIndividuais);
  const labels = [];
  const realConsumptionData = [];
  const expectedConsumptionData = [];
  
  tarefasIndividuais.forEach(item => {
    let realConsumption = 0;
    let expectedConsumption = 0;
    const realConsumo = item.consumo_por_m2;
    const expectedConsumo = item.expected_consumo_por_m2;
    
    if (realConsumo && Object.keys(realConsumo).length > 0) {
      const material = Object.keys(realConsumo)[0];
      realConsumption = parseFloat(realConsumo[material]) || 0;
      expectedConsumption = expectedConsumo ? (parseFloat(expectedConsumo[material]) || 0) : 0;
      labels.push(`${item.tarefa} (ID ${item.id}) - ${material}`);
    } else {
      labels.push(`${item.tarefa} (ID ${item.id})`);
    }
    realConsumptionData.push(realConsumption);
    expectedConsumptionData.push(expectedConsumption);
  });
  
  const canvas = document.getElementById('groupedConsumptionChart');
  if (!canvas) {
    console.warn("Canvas com id 'groupedConsumptionChart' não encontrado. Pulando renderização do gráfico de consumo.");
    return;
  }
  const ctx = canvas.getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Consumo Real por m²',
          data: realConsumptionData,
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: 'Consumo Esperado por m²',
          data: expectedConsumptionData,
          backgroundColor: 'rgba(153, 102, 255, 0.5)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

/**
 * Renderiza um gráfico de linhas para exibir a evolução semanal do tempo por m².
 * @param {Object} mediaSemanal - Objeto com chaves representando semanas e valores com a média do tempo por m².
 */
function renderWeeklyChart(mediaSemanal) {
  console.log("Renderizando gráfico semanal com dados:", mediaSemanal);
  const labels = Object.keys(mediaSemanal);
  const values = Object.values(mediaSemanal).map(val => parseFloat(val) || 0);
  
  const canvas = document.getElementById('weeklyChart');
  if (!canvas) {
    console.error("Canvas com id 'weeklyChart' não encontrado.");
    return;
  }
  const ctx = canvas.getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Média Semanal (minutos por m²)',
        data: values,
        fill: false,
        borderColor: 'rgba(255, 159, 64, 1)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

/**
 * Renderiza um gráfico de linhas para exibir a evolução mensal do tempo por m².
 * @param {Object} mediaMensal - Objeto com chaves representando meses e valores com a média do tempo por m².
 */
function renderMonthlyChart(mediaMensal) {
  console.log("Renderizando gráfico mensal com dados:", mediaMensal);
  const labels = Object.keys(mediaMensal);
  const values = Object.values(mediaMensal).map(val => parseFloat(val) || 0);
  
  const canvas = document.getElementById('monthlyChart');
  if (!canvas) {
    console.error("Canvas com id 'monthlyChart' não encontrado.");
    return;
  }
  const ctx = canvas.getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Média Mensal (minutos por m²)',
        data: values,
        fill: false,
        borderColor: 'rgba(75, 192, 192, 1)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

/**
 * Função principal que inicia a renderização dos gráficos.
 * Faz a requisição dos dados e chama as funções de renderização.
 */
function initCharts() {
  fetchChartData().then(data => {
    if (!data) return;
    console.log("Dados para gráficos:", data);
    
    // Renderiza os gráficos de tarefas individuais, se houver dados.
    if (data.tarefas_individuais && data.tarefas_individuais.length > 0) {
      renderGroupedBarChart(data.tarefas_individuais);
      // Renderiza o gráfico de consumo somente se o canvas estiver presente.
      renderGroupedConsumptionChart(data.tarefas_individuais);
    }
    
    // Renderiza o gráfico de evolução semanal, se houver dados.
    if (data.media_semanal && Object.keys(data.media_semanal).length > 0) {
      renderWeeklyChart(data.media_semanal);
    }
    
    // Renderiza o gráfico de evolução mensal, se houver dados.
    if (data.media_mensal && Object.keys(data.media_mensal).length > 0) {
      renderMonthlyChart(data.media_mensal);
    }
  });
}
  
// Inicializa os gráficos quando o documento estiver carregado.
document.addEventListener('DOMContentLoaded', initCharts);
