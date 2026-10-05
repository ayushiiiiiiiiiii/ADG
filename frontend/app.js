const API_BASE = 'http://127.0.0.1:8000';

const form = document.getElementById('analysis-form');
const languageSelect = document.getElementById('language');
const codeEditor = document.getElementById('code');
const analyzeButton = document.getElementById('analyze-btn');
const clearButton = document.getElementById('clear-btn');
const exampleButton = document.getElementById('load-example');
const apiStatus = document.getElementById('api-status');
const resultState = document.getElementById('result-state');
const complexity = document.getElementById('complexity');
const confidence = document.getElementById('confidence');
const reason = document.getElementById('reason');
const featuresTable = document.getElementById('features-table');
const rowTemplate = document.getElementById('feature-row-template');

const examples = {
  python: `for i in range(n):
    print(i)`,
  java: `for (int i = 0; i < n; i++) {
    System.out.println(i);
}`,
};

const formatFeatureValue = (value) => {
  if (typeof value === 'boolean') {
    return value ? 'true' : 'false';
  }

  if (value === null || value === undefined) {
    return '—';
  }

  return String(value);
};

const setStatus = (message, tone = 'neutral') => {
  apiStatus.textContent = message;
  apiStatus.classList.remove('flash-success', 'flash-error');

  if (tone === 'success') {
    apiStatus.classList.add('flash-success');
  }

  if (tone === 'error') {
    apiStatus.classList.add('flash-error');
  }
};

const setResultState = (message, tone = 'neutral') => {
  resultState.textContent = message;
  resultState.classList.remove('flash-success', 'flash-error');

  if (tone === 'success') {
    resultState.classList.add('flash-success');
  }

  if (tone === 'error') {
    resultState.classList.add('flash-error');
  }
};

const renderFeatures = (featureMap) => {
  featuresTable.innerHTML = '';
  const keys = Object.keys(featureMap || {});

  if (keys.length === 0) {
    featuresTable.innerHTML = '<tr><td colspan="2" class="muted-cell">No features returned.</td></tr>';
    return;
  }

  keys.forEach((key) => {
    const row = rowTemplate.content.cloneNode(true);
    row.querySelector('.feature-name').textContent = key;
    row.querySelector('.feature-value').textContent = formatFeatureValue(featureMap[key]);
    featuresTable.appendChild(row);
  });
};

const fetchHealth = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/health`);

    if (!response.ok) {
      throw new Error(`Health check failed (${response.status})`);
    }

    setStatus('Backend connected', 'success');
  } catch (error) {
    setStatus('Backend offline', 'error');
  }
};

const analyzeCode = async (payload) => {
  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    const detail = typeof data.detail === 'string' ? data.detail : 'Analysis failed.';
    throw new Error(detail);
  }

  return data;
};

const resetResults = () => {
  complexity.textContent = '—';
  confidence.textContent = '—';
  reason.textContent = 'Run an analysis to see an explanation.';
  featuresTable.innerHTML = '<tr><td colspan="2" class="muted-cell">No results yet.</td></tr>';
  setResultState('Idle');
};

languageSelect.addEventListener('change', () => {
  if (!codeEditor.value.trim()) {
    codeEditor.value = examples[languageSelect.value];
  }
});

exampleButton.addEventListener('click', () => {
  codeEditor.value = examples[languageSelect.value];
  codeEditor.focus();
});

clearButton.addEventListener('click', () => {
  codeEditor.value = '';
  resetResults();
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    language: languageSelect.value,
    code: codeEditor.value,
  };

  analyzeButton.disabled = true;
  setResultState('Analyzing...');
  setStatus('Sending request...', 'neutral');

  try {
    const data = await analyzeCode(payload);
    complexity.textContent = data.time_complexity;
    confidence.textContent = `${Math.round(data.confidence * 100)}%`;
    reason.textContent = data.reason;
    renderFeatures(data.features);
    setResultState('Success', 'success');
    setStatus('Analysis complete', 'success');
  } catch (error) {
    setResultState('Error', 'error');
    setStatus(error.message, 'error');
    reason.textContent = error.message;
  } finally {
    analyzeButton.disabled = false;
  }
});

codeEditor.value = examples.python;
resetResults();
fetchHealth();
