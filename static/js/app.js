// State management
const state = {
    currentDataset: null,
    proposals: [],
    selectedProposal: null,
    vizData: null,
    currentChart: null
};

// DOM Elements
const elements = {
    fileInput: document.getElementById('fileInput'),
    uploadSection: document.getElementById('uploadSection'),
    questionSection: document.getElementById('questionSection'),
    proposalsSection: document.getElementById('proposalsSection'),
    visualizationSection: document.getElementById('visualizationSection'),
    uploadInfo: document.getElementById('uploadInfo'),
    uploadProgress: document.getElementById('uploadProgress'),
    datasetInfo: document.getElementById('datasetInfo'),
    questionInput: document.getElementById('questionInput'),
    generateBtn: document.getElementById('generateBtn'),
    generateProgress: document.getElementById('generateProgress'),
    changeDatasetBtn: document.getElementById('changeDatasetBtn'),
    proposalsList: document.getElementById('proposalsList'),
    vizTitle: document.getElementById('vizTitle'),
    vizJustification: document.getElementById('vizJustification'),
    chartCanvas: document.getElementById('chartCanvas'),
    downloadBtn: document.getElementById('downloadBtn'),
    backToProposalsBtn: document.getElementById('backToProposalsBtn'),
    newQuestionBtn: document.getElementById('newQuestionBtn'),
    errorMessage: document.getElementById('errorMessage')
};

// API Base URL
const API_URL = '/api';

// Event Listeners
elements.fileInput.addEventListener('change', handleFileUpload);
elements.generateBtn.addEventListener('click', handleGenerateVisualization);
elements.changeDatasetBtn.addEventListener('click', goBackToUpload);
elements.downloadBtn.addEventListener('click', downloadChart);
elements.backToProposalsBtn.addEventListener('click', goBackToProposals);
elements.newQuestionBtn.addEventListener('click', goBackToQuestion);

// File Upload Handler
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    elements.uploadInfo.textContent = file.name;
    elements.uploadProgress.classList.remove('hidden');
    hideError();

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            state.currentDataset = data;
            showSuccess(`Dataset chargé: ${data.rows} lignes, ${data.columns.length} colonnes`);
            showSection('question');
        } else {
            showError(data.error || 'Erreur lors du téléchargement');
        }
    } catch (error) {
        showError('Erreur de connexion au serveur. Assurez-vous que Flask est lancé.');
    } finally {
        elements.uploadProgress.classList.add('hidden');
    }
}

// Generate Visualizations Handler
async function handleGenerateVisualization() {
    const question = elements.questionInput.value.trim();
    
    if (!question) {
        showError('Veuillez poser une question');
        return;
    }

    elements.generateBtn.disabled = true;
    elements.generateProgress.classList.remove('hidden');
    hideError();

    try {
        const response = await fetch(`${API_URL}/generate-visualizations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (data.success) {
            state.proposals = data.proposals;
            displayProposals(data.proposals);
            showSection('proposals');
        } else {
            showError(data.error || 'Erreur lors de la génération');
        }
    } catch (error) {
        showError('Erreur de connexion au serveur');
    } finally {
        elements.generateBtn.disabled = false;
        elements.generateProgress.classList.add('hidden');
    }
}

// Display Proposals
function displayProposals(proposals) {
    elements.proposalsList.innerHTML = '';
    
    proposals.forEach(proposal => {
        const card = document.createElement('div');
        card.className = 'proposal-card';
        card.innerHTML = `
            <h3>${proposal.title}</h3>
            <span class="proposal-type">${proposal.type}</span>
            <p class="proposal-justification">${proposal.justification}</p>
        `;
        
        card.addEventListener('click', () => selectProposal(proposal));
        elements.proposalsList.appendChild(card);
    });
}

// Select Proposal and Prepare Visualization
async function selectProposal(proposal) {
    state.selectedProposal = proposal;
    hideError();

    // Show loading in visualization section
    elements.vizTitle.textContent = 'Préparation de la visualisation...';
    showSection('visualization');

    try {
        const response = await fetch(`${API_URL}/prepare-visualization`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: proposal.type,
                config: proposal.config
            })
        });

        const data = await response.json();

        if (data.success) {
            state.vizData = data;
            displayVisualization(proposal, data);
        } else {
            showError(data.error || 'Erreur lors de la préparation');
        }
    } catch (error) {
        showError('Erreur de connexion au serveur');
    }
}

// Display Visualization with Chart.js
function displayVisualization(proposal, vizData) {
    elements.vizTitle.textContent = proposal.title;
    elements.vizJustification.textContent = proposal.justification;

    // Destroy previous chart if exists
    if (state.currentChart) {
        state.currentChart.destroy();
    }

    const ctx = elements.chartCanvas.getContext('2d');
    
    let chartConfig;

    switch (proposal.type) {
        case 'scatter':
            chartConfig = createScatterChart(vizData);
            break;
        case 'bar':
            chartConfig = createBarChart(vizData);
            break;
        case 'horizontalBar':
            chartConfig = createHorizontalBarChart(vizData);
            break;
        case 'pie':
            chartConfig = createPieChart(vizData);
            break;
        case 'box':
            chartConfig = createBoxChart(vizData);
            break;
        case 'correlationMatrix':
            chartConfig = createCorrelationMatrixChart(vizData);
            break;
        case 'heatmap':
            chartConfig = createHeatmapChart(vizData);
            break;
        case 'line':
            chartConfig = createLineChart(vizData);
            break;
        default:
            showError(`Type de visualisation non supporté: ${proposal.type}`);
            return;
    }

    state.currentChart = new Chart(ctx, chartConfig);
}

// Chart Creation Functions
function createScatterChart(vizData) {
    return {
        type: 'scatter',
        data: {
            datasets: [{
                label: state.selectedProposal.title,
                data: vizData.data.data.map(d => ({ x: d.x, y: d.y })),
                backgroundColor: 'rgba(59, 130, 246, 0.6)',
                borderColor: 'rgba(59, 130, 246, 0.8)',
                borderWidth: 1,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },  // Single dataset = no legend (reduce chartjunk)
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { size: 18, weight: 'bold', family: '-apple-system, sans-serif' },
                    padding: { top: 10, bottom: 20 }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    displayColors: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: vizData.x_label || 'X',
                        font: { size: 13, weight: '600' }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',  // Minimal grid
                        lineWidth: 1
                    },
                    ticks: { font: { size: 11 } }
                },
                y: {
                    title: {
                        display: true,
                        text: vizData.y_label || 'Y',
                        font: { size: 13, weight: '600' }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        lineWidth: 1
                    },
                    ticks: { font: { size: 11 } }
                }
            }
        }
    };
}

function createBarChart(vizData) {
    const colors = [
        'rgba(59, 130, 246, 0.85)',   // Blue
        'rgba(16, 185, 129, 0.85)',   // Green
        'rgba(245, 158, 11, 0.85)',   // Orange
        'rgba(239, 68, 68, 0.85)',    // Red
        'rgba(139, 92, 246, 0.85)',   // Purple
        'rgba(236, 72, 153, 0.85)',   // Pink
        'rgba(14, 165, 233, 0.85)',   // Cyan
        'rgba(234, 179, 8, 0.85)'     // Yellow
    ];

    return {
        type: 'bar',
        data: {
            labels: vizData.data.data.map(d => d.category),
            datasets: [{
                label: vizData.y_label || 'Value',
                data: vizData.data.data.map(d => d.value),
                backgroundColor: vizData.data.data.map((_, i) => colors[i % colors.length]),
                borderColor: 'transparent', // No borders for cleaner look (Tufte principle)
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    display: false  // Remove legend for single dataset (reduce chartjunk)
                },
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { 
                        size: 18, 
                        weight: 'bold',
                        family: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
                    },
                    padding: { top: 10, bottom: 20 }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 },
                    displayColors: false  // Remove color box (reduce chartjunk)
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: vizData.x_label || 'Category',
                        font: { size: 13, weight: '600' },
                        padding: { top: 10 }
                    },
                    grid: {
                        display: false  // Remove vertical grid lines (Tufte: minimize non-data ink)
                    },
                    ticks: {
                        font: { size: 11 },
                        maxRotation: 45,
                        minRotation: 0
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: vizData.y_label || 'Value',
                        font: { size: 13, weight: '600' }
                    },
                    beginAtZero: true,  // CRITICAL: Always start at 0 for bar charts (best practice)
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',  // Subtle horizontal lines only
                        lineWidth: 1
                    },
                    ticks: {
                        font: { size: 11 }
                    }
                }
            },
            layout: {
                padding: {
                    top: 5,
                    right: 20,
                    bottom: 5,
                    left: 10
                }
            }
        }
    };
}

function createHorizontalBarChart(vizData) {
    const colors = [
        'rgba(102, 126, 234, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(236, 72, 153, 0.8)'
    ];

    return {
        type: 'bar',
        data: {
            labels: vizData.data.data.map(d => d.category),
            datasets: [{
                label: vizData.y_label || 'Value',
                data: vizData.data.data.map(d => d.value),
                backgroundColor: vizData.data.data.map((_, i) => colors[i % colors.length]),
                borderColor: vizData.data.data.map((_, i) => colors[i % colors.length].replace('0.8', '1')),
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y', // This makes it horizontal
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { size: 18, weight: 'bold' }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: vizData.y_label || 'Value',
                        font: { size: 14, weight: 'bold' }
                    },
                    beginAtZero: true
                },
                y: {
                    title: {
                        display: true,
                        text: vizData.x_label || 'Category',
                        font: { size: 14, weight: 'bold' }
                    }
                }
            }
        }
    };
}

function createPieChart(vizData) {
    const colors = [
        'rgba(102, 126, 234, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(14, 165, 233, 0.8)',
        'rgba(234, 179, 8, 0.8)',
        'rgba(251, 146, 60, 0.8)',
        'rgba(20, 184, 166, 0.8)'
    ];

    return {
        type: 'pie',
        data: {
            labels: vizData.data.data.map(d => d.label),
            datasets: [{
                data: vizData.data.data.map(d => d.value),
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.8', '1')),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    display: true,
                    position: 'right',
                    labels: {
                        font: { size: 12 }
                    }
                },
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { size: 18, weight: 'bold' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    };
}

function createBoxChart(vizData) {
    // Box plot as bar chart showing medians
    return {
        type: 'bar',
        data: {
            labels: vizData.data.data.map(d => d.category),
            datasets: [{
                label: 'Médiane',
                data: vizData.data.data.map(d => d.median),
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { size: 18 }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: vizData.x_label || 'Category'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: vizData.y_label || 'Value'
                    }
                }
            }
        }
    };
}

function createLineChart(vizData) {
    return {
        type: 'line',
        data: {
            labels: vizData.data.data.map(d => d.x),
            datasets: [{
                label: vizData.y_label || 'Value',
                data: vizData.data.data.map(d => d.y),
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { size: 18, weight: 'bold' }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: vizData.x_label || 'X',
                        font: { size: 14, weight: 'bold' }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: vizData.y_label || 'Y',
                        font: { size: 14, weight: 'bold' }
                    }
                }
            }
        }
    };
}

function createHeatmapChart(vizData) {
    // For true heatmap, we need Chart.js Matrix plugin
    // Using a bubble chart as alternative visualization
    const data = vizData.data.data;
    
    // Get unique x and y values
    const xValues = [...new Set(data.map(d => d.x))];
    const yValues = [...new Set(data.map(d => d.y))];
    
    // Create bubble data
    const bubbleData = data.map(d => ({
        x: xValues.indexOf(d.x),
        y: yValues.indexOf(d.y),
        r: Math.abs(d.value) * 20, // Scale bubble size by correlation value
        value: d.value,
        xLabel: d.x,
        yLabel: d.y
    }));

    // Color based on correlation value
    const getColor = (value) => {
        if (value > 0.7) return 'rgba(16, 185, 129, 0.8)'; // Strong positive - green
        if (value > 0.3) return 'rgba(102, 126, 234, 0.6)'; // Moderate positive - blue
        if (value > -0.3) return 'rgba(156, 163, 175, 0.6)'; // Weak - gray
        if (value > -0.7) return 'rgba(245, 158, 11, 0.6)'; // Moderate negative - orange
        return 'rgba(239, 68, 68, 0.8)'; // Strong negative - red
    };

    return {
        type: 'bubble',
        data: {
            datasets: [{
                label: 'Correlation',
                data: bubbleData,
                backgroundColor: bubbleData.map(d => getColor(d.value)),
                borderColor: bubbleData.map(d => getColor(d.value).replace('0.8', '1')),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { size: 18, weight: 'bold' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const point = context.raw;
                            return `${point.xLabel} vs ${point.yLabel}: ${point.value.toFixed(3)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: vizData.x_label || 'Variables',
                        font: { size: 14, weight: 'bold' }
                    },
                    ticks: {
                        callback: function(value) {
                            return xValues[value] || '';
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: vizData.y_label || 'Variables',
                        font: { size: 14, weight: 'bold' }
                    },
                    ticks: {
                        callback: function(value) {
                            return yValues[value] || '';
                        }
                    }
                }
            }
        }
    };
}

function createCorrelationMatrixChart(vizData) {
    // Create a proper correlation matrix visualization
    const variables = vizData.x_labels || vizData.variables;
    const flatData = vizData.data.flat();
    
    // Create matrix-style bubble chart
    const bubbleData = flatData.map(d => ({
        x: d.x,
        y: d.y,
        r: Math.abs(d.value) * 15,
        value: d.value,
        xLabel: d.xLabel,
        yLabel: d.yLabel
    }));

    // Color gradient from red (negative) to white (0) to green (positive)
    const getColor = (value) => {
        if (value >= 0.8) return 'rgba(5, 150, 105, 0.9)'; // Dark green
        if (value >= 0.5) return 'rgba(16, 185, 129, 0.8)'; // Green
        if (value >= 0.2) return 'rgba(134, 239, 172, 0.7)'; // Light green
        if (value >= -0.2) return 'rgba(229, 231, 235, 0.7)'; // Gray
        if (value >= -0.5) return 'rgba(252, 211, 77, 0.7)'; // Yellow
        if (value >= -0.8) return 'rgba(251, 146, 60, 0.8)'; // Orange
        return 'rgba(239, 68, 68, 0.9)'; // Red
    };

    return {
        type: 'bubble',
        data: {
            datasets: [{
                label: 'Correlation Coefficient',
                data: bubbleData,
                backgroundColor: bubbleData.map(d => getColor(d.value)),
                borderColor: bubbleData.map(d => getColor(d.value).replace(/0\.\d+/, '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: state.selectedProposal.title,
                    font: { size: 18, weight: 'bold' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const point = context.raw;
                            const corrValue = point.value.toFixed(3);
                            let strength = '';
                            if (Math.abs(point.value) >= 0.8) strength = ' (Strong)';
                            else if (Math.abs(point.value) >= 0.5) strength = ' (Moderate)';
                            else if (Math.abs(point.value) >= 0.2) strength = ' (Weak)';
                            else strength = ' (Very Weak)';
                            return `${point.xLabel} ↔ ${point.yLabel}: ${corrValue}${strength}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Variables',
                        font: { size: 14, weight: 'bold' }
                    },
                    ticks: {
                        callback: function(value) {
                            return variables[value] || '';
                        },
                        font: { size: 10 }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Variables',
                        font: { size: 14, weight: 'bold' }
                    },
                    ticks: {
                        callback: function(value) {
                            return variables[value] || '';
                        },
                        font: { size: 10 }
                    }
                }
            }
        }
    };
}

// Download Chart as PNG
function downloadChart() {
    if (!state.currentChart) return;

    const link = document.createElement('a');
    link.download = `${state.selectedProposal.title.replace(/\s+/g, '_')}.png`;
    link.href = elements.chartCanvas.toDataURL('image/png');
    link.click();
}

// Navigation Functions
function showSection(section) {
    // Hide all sections
    elements.uploadSection.classList.add('hidden');
    elements.questionSection.classList.add('hidden');
    elements.proposalsSection.classList.add('hidden');
    elements.visualizationSection.classList.add('hidden');

    // Show requested section
    switch(section) {
        case 'upload':
            elements.uploadSection.classList.remove('hidden');
            break;
        case 'question':
            elements.questionSection.classList.remove('hidden');
            break;
        case 'proposals':
            elements.proposalsSection.classList.remove('hidden');
            break;
        case 'visualization':
            elements.visualizationSection.classList.remove('hidden');
            break;
    }
}

function goBackToUpload() {
    // Reset file input
    elements.fileInput.value = '';
    elements.uploadInfo.textContent = 'Aucun fichier sélectionné';
    
    // Clear state
    state.currentDataset = null;
    state.proposals = [];
    state.selectedProposal = null;
    state.vizData = null;
    
    // Clear question
    elements.questionInput.value = '';
    
    // Destroy chart if exists
    if (state.currentChart) {
        state.currentChart.destroy();
        state.currentChart = null;
    }
    
    showSection('upload');
    hideError();
}

function goBackToProposals() {
    // Keep proposals but destroy current chart
    if (state.currentChart) {
        state.currentChart.destroy();
        state.currentChart = null;
    }
    
    state.selectedProposal = null;
    state.vizData = null;
    
    showSection('proposals');
    hideError();
}

function goBackToQuestion() {
    // Keep dataset but clear proposals
    state.proposals = [];
    state.selectedProposal = null;
    state.vizData = null;
    
    // Destroy chart if exists
    if (state.currentChart) {
        state.currentChart.destroy();
        state.currentChart = null;
    }
    
    // Clear question input
    elements.questionInput.value = '';
    
    showSection('question');
    hideError();
}

// Error Handling
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.classList.remove('hidden');
    setTimeout(() => {
        elements.errorMessage.classList.add('hidden');
    }, 5000);
}

function hideError() {
    elements.errorMessage.classList.add('hidden');
}

function showSuccess(message) {
    elements.datasetInfo.textContent = message;
}

// Initialize
console.log('Application de visualisation intelligente chargée ✓');