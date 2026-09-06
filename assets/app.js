const state = {
  entries: [],
  filteredEntries: [],
  irregularities: [],
};

const elements = {
  total: document.querySelector('#stat-total'),
  verified: document.querySelector('#stat-verified'),
  review: document.querySelector('#stat-review'),
  irregularities: document.querySelector('#stat-irregularities'),
  search: document.querySelector('#search'),
  statusFilter: document.querySelector('#status-filter'),
  categoryFilter: document.querySelector('#category-filter'),
  catalogBody: document.querySelector('#catalog-body'),
  emptyState: document.querySelector('#empty-state'),
  irregularityList: document.querySelector('#irregularity-list'),
  downloadJson: document.querySelector('#download-json'),
  downloadCsv: document.querySelector('#download-csv'),
};

const statusLabels = {
  verified: 'Verified',
  'needs-review': 'Needs review',
  blocked: 'Blocked',
};

async function loadCatalog() {
  try {
    const response = await fetch('data/catalog.json', { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`Catalog request failed with ${response.status}`);
    }
    const catalog = await response.json();
    state.entries = Array.isArray(catalog.entries) ? catalog.entries : [];
    state.irregularities = Array.isArray(catalog.irregularities) ? catalog.irregularities : [];
  } catch (error) {
    state.entries = [];
    state.irregularities = [
      {
        id: 'LOAD-ERROR',
        severity: 'blocked',
        summary: 'Catalog data could not be loaded.',
        detail: error.message,
        reviewStatus: 'needs-owner-review',
      },
    ];
  }

  populateCategories();
  applyFilters();
  renderIrregularities();
  updateStats();
}

function populateCategories() {
  const categories = new Set();
  state.entries.forEach((entry) => {
    normalizeArray(entry.categories).forEach((category) => categories.add(category));
  });

  const currentValue = elements.categoryFilter.value;
  elements.categoryFilter.innerHTML = '<option value="all">All categories</option>';
  [...categories].sort((a, b) => a.localeCompare(b)).forEach((category) => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    elements.categoryFilter.append(option);
  });
  elements.categoryFilter.value = [...categories].includes(currentValue) ? currentValue : 'all';
}

function applyFilters() {
  const query = elements.search.value.trim().toLowerCase();
  const status = elements.statusFilter.value;
  const category = elements.categoryFilter.value;

  state.filteredEntries = state.entries.filter((entry) => {
    const haystack = [
      entry.displayName,
      entry.legalAdultEvidence?.summary,
      entry.verificationStatus,
      entry.lastReviewed,
      ...normalizeArray(entry.categories),
      ...normalizeArray(entry.flags),
      ...normalizeArray(entry.sources).flatMap((source) => [source.label, source.url, source.platform]),
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();

    const matchesSearch = !query || haystack.includes(query);
    const matchesStatus = status === 'all' || entry.verificationStatus === status;
    const matchesCategory = category === 'all' || normalizeArray(entry.categories).includes(category);
    return matchesSearch && matchesStatus && matchesCategory;
  });

  renderTable();
  updateStats();
}

function renderTable() {
  elements.catalogBody.innerHTML = '';

  state.filteredEntries.forEach((entry) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>${escapeHtml(entry.displayName || 'Unnamed record')}</strong><br><small>${escapeHtml(entry.id || '')}</small></td>
      <td>${renderChips(normalizeArray(entry.categories))}</td>
      <td>${renderAgeEvidence(entry.legalAdultEvidence)}</td>
      <td>${renderSources(normalizeArray(entry.sources))}</td>
      <td>${renderStatus(entry.verificationStatus)}</td>
      <td>${escapeHtml(entry.lastReviewed || 'Not reviewed')}</td>
      <td>${renderChips(normalizeArray(entry.flags), 'No flags')}</td>
    `;
    elements.catalogBody.append(row);
  });

  const hasRows = state.filteredEntries.length > 0;
  elements.emptyState.hidden = hasRows;
}

function renderAgeEvidence(evidence) {
  if (!evidence) {
    return '<span class="status-pill needs-review">Missing evidence</span>';
  }

  const summary = escapeHtml(evidence.summary || 'Evidence recorded');
  const sourceUrl = safeUrl(evidence.sourceUrl);
  const sourceLabel = escapeHtml(evidence.sourceLabel || 'Review source');
  const sourceLink = sourceUrl
    ? `<br><a class="chip" href="${escapeAttribute(sourceUrl)}" rel="noopener noreferrer" target="_blank">${sourceLabel}</a>`
    : '';
  return `${summary}${sourceLink}`;
}

function renderSources(sources) {
  if (!sources.length) {
    return '<span class="status-pill needs-review">No sources</span>';
  }

  return `<ul class="source-list">${sources
    .map((source) => {
      const label = escapeHtml(source.label || source.platform || 'Source');
      const url = safeUrl(source.url) || '#';
      return `<li><a class="chip" href="${escapeAttribute(url)}" rel="noopener noreferrer" target="_blank">${label}</a></li>`;
    })
    .join('')}</ul>`;
}

function renderChips(items, emptyText = 'None') {
  if (!items.length) {
    return `<span class="chip">${escapeHtml(emptyText)}</span>`;
  }

  return `<ul class="flag-list">${items
    .map((item) => `<li><span class="chip">${escapeHtml(item)}</span></li>`)
    .join('')}</ul>`;
}

function renderStatus(status = 'needs-review') {
  const normalized = ['verified', 'needs-review', 'blocked'].includes(status) ? status : 'needs-review';
  return `<span class="status-pill ${normalized}">${statusLabels[normalized]}</span>`;
}

function renderIrregularities() {
  elements.irregularityList.innerHTML = '';

  if (!state.irregularities.length) {
    elements.irregularityList.innerHTML = '<p>No irregularities recorded.</p>';
    return;
  }

  state.irregularities.forEach((item) => {
    const card = document.createElement('article');
    card.className = `irregularity-card ${escapeAttribute(item.severity || '')}`;
    card.innerHTML = `
      <header>
        <div>
          <strong>${escapeHtml(item.id || 'UNTRACKED')}</strong>
          <p>${escapeHtml(item.summary || 'Irregularity recorded for review.')}</p>
        </div>
        ${renderStatus(item.severity === 'resolved' ? 'verified' : item.severity === 'blocked' ? 'blocked' : 'needs-review')}
      </header>
      ${item.detail ? `<p>${escapeHtml(item.detail)}</p>` : ''}
      <small>Review status: ${escapeHtml(item.reviewStatus || 'needs-review')}</small>
    `;
    elements.irregularityList.append(card);
  });
}

function updateStats() {
  const entries = state.entries;
  const verified = entries.filter((entry) => entry.verificationStatus === 'verified').length;
  const needsReview = entries.filter((entry) => entry.verificationStatus === 'needs-review').length;

  elements.total.textContent = entries.length.toLocaleString();
  elements.verified.textContent = verified.toLocaleString();
  elements.review.textContent = needsReview.toLocaleString();
  elements.irregularities.textContent = state.irregularities.length.toLocaleString();
}

function download(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function toCsv(entries) {
  const headers = ['id', 'displayName', 'categories', 'ageEvidence', 'sources', 'status', 'lastReviewed', 'flags'];
  const rows = entries.map((entry) => [
    entry.id,
    entry.displayName,
    normalizeArray(entry.categories).join('; '),
    entry.legalAdultEvidence?.summary,
    normalizeArray(entry.sources)
      .map((source) => `${source.label || source.platform || 'Source'}: ${source.url}`)
      .join('; '),
    entry.verificationStatus,
    entry.lastReviewed,
    normalizeArray(entry.flags).join('; '),
  ]);

  return [headers, ...rows]
    .map((row) => row.map((cell) => `"${String(cell || '').replaceAll('"', '""')}"`).join(','))
    .join('\n');
}

function normalizeArray(value) {
  return Array.isArray(value) ? value.filter(Boolean) : [];
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll('`', '&#096;');
}

function safeUrl(value) {
  if (!value) return '';
  try {
    const url = new URL(value, window.location.href);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
  } catch {
    return '';
  }
}

[elements.search, elements.statusFilter, elements.categoryFilter].forEach((element) => {
  element.addEventListener('input', applyFilters);
});

elements.downloadJson.addEventListener('click', () => {
  download('projx-catalog.json', JSON.stringify({ entries: state.filteredEntries }, null, 2), 'application/json');
});

elements.downloadCsv.addEventListener('click', () => {
  download('projx-catalog.csv', toCsv(state.filteredEntries), 'text/csv;charset=utf-8');
});

loadCatalog();
