const FOLLOWER_RANGES = [
  'Under 1K',
  '1K–4.9K',
  '5K–9.9K',
  '10K–24.9K',
  '25K–49.9K',
  '50K–99.9K',
  '100K–249.9K',
  '250K–499.9K',
  '500K–999.9K',
  '1M–4.9M',
  '5M+',
];

const RANGE_ORDER = {
  'Under 1K': 0,
  '1K–4.9K': 1,
  '5K–9.9K': 2,
  '10K–24.9K': 3,
  '25K–49.9K': 4,
  '50K–99.9K': 5,
  '100K–249.9K': 6,
  '250K–499.9K': 7,
  '500K–999.9K': 8,
  '1M–4.9M': 9,
  '5M+': 10,
  FOLLOWER_RANGE_UNKNOWN: 99,
};

const state = {
  entries: [],
  filteredEntries: [],
  irregularities: [],
  reviewQueue: [],
};

const elements = {
  total: document.querySelector('#stat-total'),
  verified: document.querySelector('#stat-verified'),
  review: document.querySelector('#stat-review'),
  reviewQueue: document.querySelector('#stat-review-queue'),
  irregularities: document.querySelector('#stat-irregularities'),
  under10k: document.querySelector('#stat-under-10k'),
  midFollowers: document.querySelector('#stat-mid-followers'),
  megaFollowers: document.querySelector('#stat-mega-followers'),
  unknownFollowers: document.querySelector('#stat-unknown-followers'),
  search: document.querySelector('#search'),
  statusFilter: document.querySelector('#status-filter'),
  categoryFilter: document.querySelector('#category-filter'),
  platformFilter: document.querySelector('#platform-filter'),
  followerFilter: document.querySelector('#follower-filter'),
  sortFilter: document.querySelector('#sort-filter'),
  catalogBody: document.querySelector('#catalog-body'),
  emptyState: document.querySelector('#empty-state'),
  irregularityList: document.querySelector('#irregularity-list'),
  reviewQueueList: document.querySelector('#review-queue-list'),
  followerDist: document.querySelector('#follower-distribution'),
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
    state.reviewQueue = Array.isArray(catalog.reviewQueue) ? catalog.reviewQueue : [];
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
  populatePlatforms();
  populateFollowerRanges();
  applyFilters();
  renderIrregularities();
  renderReviewQueue();
  renderFollowerDistribution();
  updateStats();
}

function renderReviewQueue() {
  if (!elements.reviewQueueList) return;
  elements.reviewQueueList.innerHTML = '';

  if (!state.reviewQueue.length) {
    elements.reviewQueueList.innerHTML = '<p>No candidates are currently awaiting review.</p>';
    return;
  }

  state.reviewQueue.forEach((item) => {
    const card = document.createElement('article');
    card.className = 'review-queue-card';
    const profileUrl = safeUrl(item.profileUrl);
    const evidenceUrl = safeUrl(item.evidenceFound?.sourceUrl);
    const followerLine = item.followerCountDisplay
      ? `<p><strong>Followers (observed):</strong> ${escapeHtml(item.followerCountDisplay)}${
          item.followerSizeRange ? ` · ${escapeHtml(item.followerSizeRange)}` : ''
        }${
          item.followerCountCheckedAt
            ? ` <small>(checked ${escapeHtml(item.followerCountCheckedAt)})</small>`
            : ''
        }</p>`
      : '';
    card.innerHTML = `
      <header>
        <div>
          <strong>${escapeHtml(item.displayName || 'Unnamed candidate')}</strong>
          ${
            item.handle
              ? `<small>${escapeHtml(item.handle)} · ${escapeHtml(item.platform || '')}</small>`
              : `<small>${escapeHtml(item.platform || '')}</small>`
          }
        </div>
        <span class="status-pill needs-review">REVIEW_REQUIRED</span>
      </header>
      <p><strong>Discovery category:</strong> ${escapeHtml(item.discoveryCategory || 'Unspecified')}</p>
      ${followerLine}
      ${
        profileUrl
          ? `<p><strong>Profile:</strong> <a class="chip" href="${escapeAttribute(
              profileUrl
            )}" rel="noopener noreferrer" target="_blank">${escapeHtml(item.profileUrl)}</a></p>`
          : ''
      }
      ${
        item.evidenceFound?.summary
          ? `<p><strong>Evidence found:</strong> ${escapeHtml(item.evidenceFound.summary)}${
              evidenceUrl
                ? ` <a class="chip" href="${escapeAttribute(
                    evidenceUrl
                  )}" rel="noopener noreferrer" target="_blank">${escapeHtml(
                    item.evidenceFound.sourceLabel || 'Source'
                  )}</a>`
                : ''
            }</p>`
          : ''
      }
      <p><strong>Missing verification:</strong> ${renderChips(
        normalizeArray(item.missingEvidence),
        'Unspecified'
      )}</p>
      ${
        normalizeArray(item.flags).length
          ? `<p><strong>Flags:</strong> ${renderChips(normalizeArray(item.flags))}</p>`
          : ''
      }
      ${item.notes ? `<p class="notes">${escapeHtml(item.notes)}</p>` : ''}
      <small>Last checked: ${escapeHtml(item.lastChecked || 'Unknown')}</small>
    `;
    elements.reviewQueueList.append(card);
  });
}

function populateCategories() {
  const categories = new Set();
  state.entries.forEach((entry) => {
    normalizeArray(entry.categories).forEach((category) => categories.add(category));
  });

  const currentValue = elements.categoryFilter.value;
  elements.categoryFilter.innerHTML = '<option value="all">All categories</option>';
  [...categories]
    .sort((a, b) => a.localeCompare(b))
    .forEach((category) => {
      const option = document.createElement('option');
      option.value = category;
      option.textContent = category;
      elements.categoryFilter.append(option);
    });
  elements.categoryFilter.value = [...categories].includes(currentValue) ? currentValue : 'all';
}

function populatePlatforms() {
  if (!elements.platformFilter) return;
  const platforms = new Set();
  state.entries.forEach((entry) => {
    normalizeArray(entry.socialAccounts).forEach((account) => {
      if (account.platform) platforms.add(account.platform);
    });
    normalizeArray(entry.sources).forEach((source) => {
      if (source.platform) platforms.add(source.platform);
    });
  });

  const currentValue = elements.platformFilter.value;
  elements.platformFilter.innerHTML = '<option value="all">All platforms</option>';
  [...platforms]
    .sort((a, b) => a.localeCompare(b))
    .forEach((platform) => {
      const option = document.createElement('option');
      option.value = platform;
      option.textContent = platform;
      elements.platformFilter.append(option);
    });
  elements.platformFilter.value = [...platforms].includes(currentValue) ? currentValue : 'all';
}

function populateFollowerRanges() {
  if (!elements.followerFilter) return;
  const currentValue = elements.followerFilter.value;
  elements.followerFilter.innerHTML = `
    <option value="all">All sizes</option>
    <option value="unknown">Unknown / not observed</option>
  `;
  FOLLOWER_RANGES.forEach((range) => {
    const option = document.createElement('option');
    option.value = range;
    option.textContent = range;
    elements.followerFilter.append(option);
  });
  const allowed = ['all', 'unknown', ...FOLLOWER_RANGES];
  elements.followerFilter.value = allowed.includes(currentValue) ? currentValue : 'all';
}

function entryPlatforms(entry) {
  const platforms = new Set();
  normalizeArray(entry.socialAccounts).forEach((account) => {
    if (account.platform) platforms.add(account.platform);
  });
  normalizeArray(entry.sources).forEach((source) => {
    if (source.platform) platforms.add(source.platform);
  });
  return platforms;
}

function entryHasPlatform(entry, platform) {
  if (platform === 'all') return true;
  return entryPlatforms(entry).has(platform);
}

function entryMatchesFollowerRange(entry, rangeValue) {
  if (rangeValue === 'all') return true;
  const range = entry.overallFollowerSizeRange || 'FOLLOWER_RANGE_UNKNOWN';
  if (rangeValue === 'unknown') {
    return range === 'FOLLOWER_RANGE_UNKNOWN' || !entry.largestPublicFollowing?.numeric;
  }
  // Exact range match on overall (largest platform) classification
  if (range === rangeValue) return true;
  // Also allow match if ANY tracked platform falls in the selected range
  return normalizeArray(entry.socialAccounts).some(
    (account) => account.followerSizeRange === rangeValue
  );
}

function largestNumeric(entry) {
  const n = entry.largestPublicFollowing?.numeric;
  return typeof n === 'number' ? n : null;
}

function sortEntries(entries, sortMode) {
  const copy = [...entries];
  switch (sortMode) {
    case 'followers-asc':
      return copy.sort((a, b) => {
        const an = largestNumeric(a);
        const bn = largestNumeric(b);
        if (an === null && bn === null) return a.displayName.localeCompare(b.displayName);
        if (an === null) return 1;
        if (bn === null) return -1;
        return an - bn;
      });
    case 'followers-desc':
      return copy.sort((a, b) => {
        const an = largestNumeric(a);
        const bn = largestNumeric(b);
        if (an === null && bn === null) return a.displayName.localeCompare(b.displayName);
        if (an === null) return 1;
        if (bn === null) return -1;
        return bn - an;
      });
    case 'name-asc':
      return copy.sort((a, b) => (a.displayName || '').localeCompare(b.displayName || ''));
    case 'recent':
    default:
      return copy.sort((a, b) => {
        const ad = a.lastReviewed || '';
        const bd = b.lastReviewed || '';
        if (ad === bd) return (a.id || '').localeCompare(b.id || '');
        return bd.localeCompare(ad);
      });
  }
}

function applyFilters() {
  const query = elements.search.value.trim().toLowerCase();
  const status = elements.statusFilter.value;
  const category = elements.categoryFilter.value;
  const platform = elements.platformFilter ? elements.platformFilter.value : 'all';
  const followerRange = elements.followerFilter ? elements.followerFilter.value : 'all';
  const sortMode = elements.sortFilter ? elements.sortFilter.value : 'recent';

  const filtered = state.entries.filter((entry) => {
    const haystack = [
      entry.displayName,
      entry.legalAdultEvidence?.summary,
      entry.verificationStatus,
      entry.lastReviewed,
      entry.overallFollowerSizeRange,
      entry.largestPublicFollowing?.display,
      entry.largestPublicFollowing?.platform,
      ...normalizeArray(entry.categories),
      ...normalizeArray(entry.flags),
      ...normalizeArray(entry.sources).flatMap((source) => [
        source.label,
        source.url,
        source.platform,
      ]),
      ...normalizeArray(entry.socialAccounts).flatMap((account) => [
        account.platform,
        account.username,
        account.followerCountDisplay,
        account.followerSizeRange,
      ]),
    ]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();

    const matchesSearch = !query || haystack.includes(query);
    const matchesStatus = status === 'all' || entry.verificationStatus === status;
    const matchesCategory =
      category === 'all' || normalizeArray(entry.categories).includes(category);
    const matchesPlatform = entryHasPlatform(entry, platform);
    const matchesFollowers = entryMatchesFollowerRange(entry, followerRange);
    return (
      matchesSearch &&
      matchesStatus &&
      matchesCategory &&
      matchesPlatform &&
      matchesFollowers
    );
  });

  state.filteredEntries = sortEntries(filtered, sortMode);
  renderTable();
  updateStats();
}

function renderFollowers(entry) {
  const accounts = normalizeArray(entry.socialAccounts).filter(
    (account) => account.followerCountDisplay && account.followerCountDisplay !== 'FOLLOWER_COUNT_UNKNOWN'
  );
  const largest = entry.largestPublicFollowing;
  const size = entry.overallFollowerSizeRange || 'FOLLOWER_RANGE_UNKNOWN';

  if (!accounts.length && (!largest || largest.numeric == null)) {
    return `<span class="chip follower-unknown">FOLLOWER_COUNT_UNKNOWN</span>
      <br><small class="muted">Size: ${escapeHtml(size)}</small>`;
  }

  const lines = accounts
    .map((account) => {
      const label = escapeHtml(account.platform || 'Platform');
      const count = escapeHtml(account.followerCountDisplay || '—');
      const user = account.username ? ` ${escapeHtml(account.username)}` : '';
      const checked = account.checkedAt
        ? ` <small class="muted">(${escapeHtml(account.checkedAt)})</small>`
        : '';
      const href = safeUrl(account.profileUrl);
      const countBit = href
        ? `<a class="chip" href="${escapeAttribute(
            href
          )}" rel="noopener noreferrer" target="_blank">${count}</a>`
        : `<span class="chip">${count}</span>`;
      return `<li><strong>${label}${user}:</strong> ${countBit}${checked}</li>`;
    })
    .join('');

  const largestLine =
    largest && largest.display
      ? `<p class="follower-largest"><strong>Largest public following:</strong> ${escapeHtml(
          largest.display
        )}${largest.platform ? ` <small>(${escapeHtml(largest.platform)})</small>` : ''}</p>`
      : '';

  return `
    <ul class="follower-list">${lines}</ul>
    ${largestLine}
    <p class="follower-size"><strong>Creator size:</strong> <span class="chip">${escapeHtml(
      size
    )}</span></p>
  `;
}

function renderTable() {
  elements.catalogBody.innerHTML = '';

  state.filteredEntries.forEach((entry) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>${escapeHtml(entry.displayName || 'Unnamed record')}</strong><br><small>${escapeHtml(
        entry.id || ''
      )}</small></td>
      <td>${renderChips(normalizeArray(entry.categories))}</td>
      <td>${renderFollowers(entry)}</td>
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
    ? `<br><a class="chip" href="${escapeAttribute(
        sourceUrl
      )}" rel="noopener noreferrer" target="_blank">${sourceLabel}</a>`
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
      return `<li><a class="chip" href="${escapeAttribute(
        url
      )}" rel="noopener noreferrer" target="_blank">${label}</a></li>`;
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
  const normalized = ['verified', 'needs-review', 'blocked'].includes(status)
    ? status
    : 'needs-review';
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
        ${renderStatus(
          item.severity === 'resolved'
            ? 'verified'
            : item.severity === 'blocked'
              ? 'blocked'
              : 'needs-review'
        )}
      </header>
      ${item.detail ? `<p>${escapeHtml(item.detail)}</p>` : ''}
      <small>Review status: ${escapeHtml(item.reviewStatus || 'needs-review')}</small>
    `;
    elements.irregularityList.append(card);
  });
}

function bandBucket(entry) {
  const n = largestNumeric(entry);
  if (n === null) return 'unknown';
  if (n < 10000) return 'under10k';
  if (n < 50000) return '10k49k';
  if (n < 250000) return '50k249k';
  if (n < 1000000) return '250k999k';
  return '1mplus';
}

function renderFollowerDistribution() {
  if (!elements.followerDist) return;
  const counts = {};
  FOLLOWER_RANGES.forEach((range) => {
    counts[range] = 0;
  });
  counts.FOLLOWER_RANGE_UNKNOWN = 0;

  state.entries.forEach((entry) => {
    const range = entry.overallFollowerSizeRange || 'FOLLOWER_RANGE_UNKNOWN';
    if (counts[range] === undefined) counts[range] = 0;
    counts[range] += 1;
  });

  const max = Math.max(1, ...Object.values(counts));
  elements.followerDist.innerHTML = '';
  [...FOLLOWER_RANGES, 'FOLLOWER_RANGE_UNKNOWN'].forEach((range) => {
    const count = counts[range] || 0;
    const bar = document.createElement('div');
    bar.className = 'dist-row';
    const pct = Math.round((count / max) * 100);
    bar.innerHTML = `
      <span class="dist-label">${escapeHtml(range)}</span>
      <span class="dist-bar" style="--pct:${pct}%"></span>
      <span class="dist-count">${count}</span>
    `;
    elements.followerDist.append(bar);
  });
}

function updateStats() {
  const entries = state.entries;
  const verified = entries.filter((entry) => entry.verificationStatus === 'verified').length;
  const needsReview = entries.filter((entry) => entry.verificationStatus === 'needs-review').length;

  elements.total.textContent = entries.length.toLocaleString();
  elements.verified.textContent = verified.toLocaleString();
  elements.review.textContent = needsReview.toLocaleString();
  if (elements.reviewQueue) {
    elements.reviewQueue.textContent = state.reviewQueue.length.toLocaleString();
  }
  elements.irregularities.textContent = state.irregularities.length.toLocaleString();

  const under10k = entries.filter((e) => bandBucket(e) === 'under10k').length;
  const mid = entries.filter((e) => ['10k49k', '50k249k'].includes(bandBucket(e))).length;
  const mega = entries.filter((e) => bandBucket(e) === '1mplus').length;
  const unknown = entries.filter((e) => bandBucket(e) === 'unknown').length;

  if (elements.under10k) elements.under10k.textContent = under10k.toLocaleString();
  if (elements.midFollowers) elements.midFollowers.textContent = mid.toLocaleString();
  if (elements.megaFollowers) elements.megaFollowers.textContent = mega.toLocaleString();
  if (elements.unknownFollowers) elements.unknownFollowers.textContent = unknown.toLocaleString();
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
  const headers = [
    'id',
    'displayName',
    'categories',
    'largestFollowing',
    'largestPlatform',
    'sizeRange',
    'ageEvidence',
    'sources',
    'status',
    'lastReviewed',
    'flags',
  ];
  const rows = entries.map((entry) => [
    entry.id,
    entry.displayName,
    normalizeArray(entry.categories).join('; '),
    entry.largestPublicFollowing?.display || 'FOLLOWER_COUNT_UNKNOWN',
    entry.largestPublicFollowing?.platform || '',
    entry.overallFollowerSizeRange || 'FOLLOWER_RANGE_UNKNOWN',
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

const filterControls = [
  elements.search,
  elements.statusFilter,
  elements.categoryFilter,
  elements.platformFilter,
  elements.followerFilter,
  elements.sortFilter,
].filter(Boolean);

filterControls.forEach((element) => {
  element.addEventListener('input', applyFilters);
  element.addEventListener('change', applyFilters);
});

elements.downloadJson.addEventListener('click', () => {
  download(
    'projx-catalog.json',
    JSON.stringify({ entries: state.filteredEntries }, null, 2),
    'application/json'
  );
});

elements.downloadCsv.addEventListener('click', () => {
  download('projx-catalog.csv', toCsv(state.filteredEntries), 'text/csv;charset=utf-8');
});

loadCatalog();
