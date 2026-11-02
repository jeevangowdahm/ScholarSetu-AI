/**
 * ScholarSetu AI — Client-Side Application Controller
 * Version 2.0.0 (Production Release)
 */

// Global State
let allSchemes = [];
let savedSchemes = [];
let compareSchemeIds = new Set();
let currentResults = [];
let toastTimeout = null;

// Utility Helpers
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const escapeHtml = (str) => {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

const formatINR = (val) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(Number(val) || 0);
};

const showToast = (message) => {
  const toastEl = $('#toast');
  if (!toastEl) return;
  toastEl.textContent = message;
  toastEl.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toastEl.classList.remove('show');
  }, 3200);
};

// ==========================================================================
// 1. Accessibility Toolbar & Theme Mode
// ==========================================================================
function initAccessibility() {
  const contrastBtn = $('#contrast-toggle');
  const fontDecBtn = $('#font-dec');
  const fontResetBtn = $('#font-reset');
  const fontIncBtn = $('#font-inc');

  // Load saved high contrast preference
  if (localStorage.getItem('scholarsetu_contrast') === 'high') {
    document.body.classList.add('theme-high-contrast');
    if (contrastBtn) contrastBtn.setAttribute('aria-pressed', 'true');
  }

  if (contrastBtn) {
    contrastBtn.addEventListener('click', () => {
      const isHigh = document.body.classList.toggle('theme-high-contrast');
      contrastBtn.setAttribute('aria-pressed', isHigh ? 'true' : 'false');
      localStorage.setItem('scholarsetu_contrast', isHigh ? 'high' : 'default');
      showToast(isHigh ? 'High Contrast Mode Enabled' : 'Standard View Enabled');
    });
  }

  const resetFontButtons = () => {
    $$('.accessibility-tools .tool-btn').forEach(btn => btn.classList.remove('active-tool'));
  };

  if (fontDecBtn) {
    fontDecBtn.addEventListener('click', () => {
      document.body.classList.remove('font-lg');
      document.body.classList.add('font-sm');
      resetFontButtons();
      fontDecBtn.classList.add('active-tool');
    });
  }

  if (fontResetBtn) {
    fontResetBtn.addEventListener('click', () => {
      document.body.classList.remove('font-sm', 'font-lg');
      resetFontButtons();
      fontResetBtn.classList.add('active-tool');
    });
  }

  if (fontIncBtn) {
    fontIncBtn.addEventListener('click', () => {
      document.body.classList.remove('font-sm');
      document.body.classList.add('font-lg');
      resetFontButtons();
      fontIncBtn.classList.add('active-tool');
    });
  }

  const dismissTrustBtn = $('#dismiss-trust');
  if (dismissTrustBtn) {
    dismissTrustBtn.addEventListener('click', () => {
      const banner = $('.trust-banner');
      if (banner) banner.remove();
    });
  }
}

// ==========================================================================
// 2. Multi-Step Wizard Engine
// ==========================================================================
function initWizard() {
  const stepTabs = $$('.wizard-stepper .step-tab');
  const panels = $$('.wizard-panel');

  const goToStep = (stepNum) => {
    panels.forEach(p => p.classList.remove('active'));
    stepTabs.forEach(t => t.classList.remove('active'));

    const targetPanel = $(`#step-panel-${stepNum}`);
    const targetTab = $(`.wizard-stepper .step-tab[data-step="${stepNum}"]`);

    if (targetPanel) targetPanel.classList.add('active');
    if (targetTab) {
      targetTab.classList.add('active');
      // Mark preceding steps as completed
      stepTabs.forEach(t => {
        const s = parseInt(t.getAttribute('data-step') || '1', 10);
        if (s < stepNum) t.classList.add('completed');
        else if (s >= stepNum) t.classList.remove('completed');
      });
    }
  };

  // Next and Prev buttons
  $$('.step-next-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetStep = parseInt(btn.getAttribute('data-target') || '1', 10);
      goToStep(targetStep);
    });
  });

  $$('.step-prev-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetStep = parseInt(btn.getAttribute('data-target') || '1', 10);
      goToStep(targetStep);
    });
  });

  // Tab click navigation
  stepTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const stepNum = parseInt(tab.getAttribute('data-step') || '1', 10);
      goToStep(stepNum);
    });
  });

  // Income presets
  $$('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const incVal = btn.getAttribute('data-income');
      const incInput = $('#student-income');
      if (incInput && incVal) {
        incInput.value = incVal;
        showToast(`Income set to ${formatINR(incVal)}`);
      }
    });
  });

  // Form submission
  const form = $('#eligibility-form');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const errBox = $('#form-error-msg');
      if (errBox) errBox.classList.add('hidden');

      const payload = {
        gender: $('#student-gender')?.value || 'All',
        age: $('#student-age')?.value,
        state: $('#student-state')?.value || 'All India',
        area: $('#student-area')?.value,
        level: $('#student-level')?.value || 'Undergraduate',
        stream: $('#student-stream')?.value || 'Engineering',
        marks: $('#student-marks')?.value,
        inst_type: $('#student-inst-type')?.value,
        category: $('#student-category')?.value || 'Any',
        minority: $('#student-minority')?.value || 'None',
        income: $('#student-income')?.value,
        is_pwd: $('#check-pwd')?.checked || false,
        is_single_girl_child: $('#check-single-girl')?.checked || false,
        is_orphan_covid: $('#check-orphan-covid')?.checked || false,
        is_ex_servicemen: $('#check-ex-servicemen')?.checked || false
      };

      const submitBtn = $('#run-check-btn');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-label').textContent = 'Evaluating Gazette Rules...';
      }

      try {
        const res = await fetch('/api/match', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Screening engine encountered an error.');

        currentResults = data.results || [];
        renderScreeningResults(data);

        const resultsContainer = $('#results-container');
        if (resultsContainer) {
          resultsContainer.classList.remove('hidden');
          resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        showToast(`Screening complete! Found ${data.summary?.eligible_count || 0} direct matches.`);
      } catch (err) {
        if (errBox) {
          errBox.textContent = err.message;
          errBox.classList.remove('hidden');
        }
        showToast(err.message);
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.querySelector('.btn-label').textContent = 'Run Real-Time Eligibility Match';
        }
      }
    });
  }

  // Edit profile button on results
  const reEditBtn = $('#re-edit-profile-btn');
  if (reEditBtn) {
    reEditBtn.addEventListener('click', () => {
      const elSection = $('#eligibility');
      if (elSection) elSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  // Export results button
  const exportResultsBtn = $('#export-results-btn');
  if (exportResultsBtn) {
    exportResultsBtn.addEventListener('click', () => {
      printApplicationSummary(currentResults);
    });
  }
}

// ==========================================================================
// 3. Render Screening Results
// ==========================================================================
function renderScreeningResults(data) {
  const summary = data.summary || {};
  $('#kpi-count-eligible').textContent = summary.eligible_count || 0;
  $('#kpi-count-conditional').textContent = summary.conditional_count || 0;
  $('#kpi-count-ineligible').textContent = summary.ineligible_count || 0;
  $('#kpi-total-aid').textContent = formatINR(summary.total_potential_aid || 0);

  const profile = data.profile || {};
  $('#results-meta-text').textContent =
    `Profile: ${profile.level || 'Undergraduate'} · Domicile: ${profile.state || 'All India'} · Category: ${profile.category || 'Any'} · Marks: ${profile.marks || '—'}% · Income: ${formatINR(profile.income)}`;

  renderFilteredResults('all');

  // Result filter tabs
  $$('.result-filter-tabs .filter-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      $$('.result-filter-tabs .filter-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filterMode = tab.getAttribute('data-result-tab') || 'all';
      renderFilteredResults(filterMode);
    });
  });
}

function renderFilteredResults(filterMode) {
  const container = $('#results-grid');
  if (!container) return;

  let list = currentResults;
  if (filterMode === 'eligible') {
    list = currentResults.filter(r => r.status === 'Potential match');
  } else if (filterMode === 'conditional') {
    list = currentResults.filter(r => r.status === 'Needs more information');
  } else if (filterMode === 'ineligible') {
    list = currentResults.filter(r => r.status === 'Not matched');
  }

  if (!list.length) {
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; padding: 40px; text-align: center;">
        <span style="font-size: 32px; display: block; margin-bottom: 10px;">📋</span>
        <h4>No schemes in this filter tab</h4>
        <p style="color: var(--text-muted); font-size: 13px;">Try switching to "All Evaluated Schemes" to see all 16 results.</p>
      </div>`;
    return;
  }

  container.innerHTML = list.map(item => {
    const s = item.scheme;
    const isEligible = item.status === 'Potential match';
    const isConditional = item.status === 'Needs more information';
    const isSaved = savedSchemes.some(x => Number(x.id) === Number(s.id));
    const isCompared = compareSchemeIds.has(Number(s.id));

    let statusBadgeClass = 'status-badge-eligible';
    let statusLabel = 'Direct Match (100%)';
    if (isConditional) {
      statusBadgeClass = 'status-badge-conditional';
      statusLabel = 'Action / Info Needed';
    } else if (!isEligible) {
      statusBadgeClass = 'status-badge-ineligible';
      statusLabel = 'Criteria Not Met';
    }

    const matchedChecks = item.matched_checks || [];
    const reasons = item.reasons || [];
    const gaps = item.gaps || [];

    return `
      <article class="result-card" data-scheme-id="${s.id}">
        <div class="card-top-bar">
          <span class="match-status-badge ${statusBadgeClass}">
            <span>●</span> ${escapeHtml(statusLabel)}
          </span>
          <span class="card-ministry-tag" title="${escapeHtml(s.ministry)}">${escapeHtml(s.ministry)}</span>
        </div>

        <h4 class="card-title">${escapeHtml(s.name)}</h4>

        <div class="card-benefit-row">
          <span class="benefit-pill">${escapeHtml(s.benefit_amount)}</span>
          ${s.is_dbt ? '<span class="dbt-tag">✓ Direct Benefit Transfer (DBT)</span>' : ''}
        </div>

        <p class="card-description">${escapeHtml(s.description)}</p>

        <!-- Rule Evaluation Details Accordion -->
        <div class="rule-check-box">
          <div class="rule-check-title">
            <span>Rule Evaluation Breakdown:</span>
            <small style="color: var(--text-muted);">${matchedChecks.length} Passed</small>
          </div>
          <ul class="rule-list">
            ${matchedChecks.slice(0, 3).map(c => `<li><span class="rule-icon-pass">✓</span> ${escapeHtml(c)}</li>`).join('')}
            ${gaps.map(g => `<li><span class="rule-icon-gap">⚠️</span> ${escapeHtml(g)}</li>`).join('')}
            ${reasons.map(r => `<li><span class="rule-icon-fail">✕</span> ${escapeHtml(r)}</li>`).join('')}
          </ul>
        </div>

        <div class="card-bottom-actions">
          <label class="compare-checkbox-label">
            <input type="checkbox" onchange="toggleCompare(${s.id}, this.checked)" ${isCompared ? 'checked' : ''}>
            <span>Compare</span>
          </label>
          <div class="card-action-btns">
            <button type="button" class="btn btn-outline btn-sm" onclick="openSchemeModal(${s.id})">
              View Details
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="toggleSaveScheme(${s.id})">
              ${isSaved ? '⭐ Shortlisted' : '☆ Save'}
            </button>
            <a href="${escapeHtml(s.official_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">
              Apply ↗
            </a>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

// ==========================================================================
// 4. Scheme Library Explorer
// ==========================================================================
async function loadLibrary() {
  try {
    const res = await fetch('/api/schemes');
    if (!res.ok) throw new Error('Failed to load scheme repository.');
    allSchemes = await res.json();

    const countText = `${allSchemes.length} verified schemes`;
    const navLibCount = $('#nav-lib-count');
    const libCountText = $('#library-count-text');
    if (navLibCount) navLibCount.textContent = allSchemes.length;
    if (libCountText) libCountText.textContent = `Showing ${countText}`;

    populateCompareDropdown();
    renderLibrary();
    await loadSaved();
    updateStats();
  } catch (err) {
    showToast(err.message);
  }
}

function renderLibrary() {
  const grid = $('#library-grid');
  if (!grid) return;

  const q = ($('#library-search')?.value || '').toLowerCase().trim();
  const category = $('#lib-category-filter')?.value || 'All';
  const sortBy = $('#lib-sort-filter')?.value || 'benefit_desc';

  let list = allSchemes.filter(s => {
    const matchSearch = !q || (s.name + ' ' + s.description + ' ' + s.category + ' ' + s.ministry + ' ' + s.code).toLowerCase().includes(q);
    const matchCat = category === 'All' || s.category === category;
    return matchSearch && matchCat;
  });

  if (sortBy === 'benefit_desc') list.sort((a, b) => b.benefit_value_num - a.benefit_value_num);
  else if (sortBy === 'benefit_asc') list.sort((a, b) => a.benefit_value_num - b.benefit_value_num);
  else if (sortBy === 'name') list.sort((a, b) => a.name.localeCompare(b.name));
  else if (sortBy === 'marks') list.sort((a, b) => a.min_marks - b.min_marks);

  const libCountText = $('#library-count-text');
  if (libCountText) libCountText.textContent = `Showing ${list.length} of ${allSchemes.length} verified schemes`;

  if (!list.length) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column: 1/-1; padding: 48px; text-align: center;">
        <span style="font-size: 36px; display: block; margin-bottom: 12px;">🔍</span>
        <h4>No Schemes Found</h4>
        <p style="color: var(--text-muted); font-size: 13px;">No scheme matched your keyword or category filter. Try clearing filters.</p>
      </div>`;
    return;
  }

  grid.innerHTML = list.map(s => {
    const isSaved = savedSchemes.some(x => Number(x.id) === Number(s.id));
    const isCompared = compareSchemeIds.has(Number(s.id));

    return `
      <article class="result-card" data-scheme-id="${s.id}">
        <div class="card-top-bar">
          <span class="match-status-badge status-badge-eligible" style="background: var(--bg-subtle); color: var(--primary-blue);">
            ${escapeHtml(s.category)}
          </span>
          <span class="card-ministry-tag" title="${escapeHtml(s.ministry)}">${escapeHtml(s.ministry)}</span>
        </div>

        <h4 class="card-title">${escapeHtml(s.name)}</h4>

        <div class="card-benefit-row">
          <span class="benefit-pill">${escapeHtml(s.benefit_amount)}</span>
          ${s.is_dbt ? '<span class="dbt-tag">✓ DBT</span>' : ''}
        </div>

        <p class="card-description">${escapeHtml(s.description)}</p>

        <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 14px; display: flex; flex-wrap: wrap; gap: 8px;">
          <span style="background: var(--bg-subtle); padding: 3px 6px; border-radius: 4px;">🎓 ${escapeHtml(s.level)}</span>
          <span style="background: var(--bg-subtle); padding: 3px 6px; border-radius: 4px;">📍 ${escapeHtml(s.state)}</span>
          <span style="background: var(--bg-subtle); padding: 3px 6px; border-radius: 4px;">📅 Closes: ${escapeHtml(s.deadline)}</span>
        </div>

        <div class="card-bottom-actions">
          <label class="compare-checkbox-label">
            <input type="checkbox" onchange="toggleCompare(${s.id}, this.checked)" ${isCompared ? 'checked' : ''}>
            <span>Compare</span>
          </label>
          <div class="card-action-btns">
            <button type="button" class="btn btn-outline btn-sm" onclick="openSchemeModal(${s.id})">
              Details
            </button>
            <button type="button" class="btn btn-outline btn-sm" onclick="toggleSaveScheme(${s.id})">
              ${isSaved ? '⭐ Shortlisted' : '☆ Save'}
            </button>
            <a href="${escapeHtml(s.official_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">
              Apply ↗
            </a>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

function initLibraryFilters() {
  const searchInput = $('#library-search');
  const catFilter = $('#lib-category-filter');
  const sortFilter = $('#lib-sort-filter');

  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(renderLibrary, 200);
    });
  }

  if (catFilter) catFilter.addEventListener('change', renderLibrary);
  if (sortFilter) sortFilter.addEventListener('change', renderLibrary);

  // Quick pills
  $$('.quick-pills-bar .pill-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('.quick-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const pillVal = btn.getAttribute('data-pill') || 'All';
      if (catFilter) catFilter.value = pillVal;
      renderLibrary();
    });
  });

  // Hero chips
  $$('.hero-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const cat = chip.getAttribute('data-filter-quick');
      if (cat && catFilter) {
        catFilter.value = cat;
        $$('.quick-pills-bar .pill-btn').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-pill') === cat);
        });
        const libSection = $('#library');
        if (libSection) libSection.scrollIntoView({ behavior: 'smooth' });
        renderLibrary();
      }
    });
  });
}

// ==========================================================================
// 5. Scheme Modal (Drawer / Deep-Dive)
// ==========================================================================
window.openSchemeModal = function(schemeId) {
  const scheme = allSchemes.find(s => Number(s.id) === Number(schemeId));
  if (!scheme) return;

  const modal = $('#scheme-modal');
  if (!modal) return;

  $('#modal-dept').textContent = scheme.ministry;
  $('#modal-title').textContent = scheme.name;
  $('#modal-code').textContent = scheme.code;
  $('#modal-benefit').textContent = scheme.benefit_amount;
  $('#modal-description').textContent = scheme.description;
  $('#modal-deadline').textContent = scheme.deadline;
  $('#modal-portal').textContent = scheme.source_name;
  $('#modal-target').textContent = `${scheme.level} (${scheme.gender})`;
  $('#modal-income-cap').textContent = scheme.max_income >= 999999999 ? 'No Income Cap' : `Up to ${formatINR(scheme.max_income)} / year`;
  $('#modal-notes').textContent = scheme.notes || 'Confirm verified conditions on the official portal.';

  const portalLink = $('#modal-portal-link');
  if (portalLink) portalLink.href = scheme.official_url;

  // Criteria list
  const criteriaList = $('#modal-criteria-list');
  if (criteriaList) {
    const items = [
      `Education Level: ${scheme.levels.join(', ')}`,
      `State of Domicile: ${scheme.states.join(', ')}`,
      `Eligible Streams: ${scheme.streams.join(', ')}`,
      `Eligible Categories: ${scheme.categories.join(', ')}`,
      `Minimum Academic Marks: ${scheme.min_marks}% in previous qualifying exam`,
      `Gender Requirement: ${scheme.gender}`
    ];
    criteriaList.innerHTML = items.map(c => `<li>${escapeHtml(c)}</li>`).join('');
  }

  // Documents required
  const docContainer = $('#modal-doc-checks');
  if (docContainer) {
    const docs = scheme.documents_required || [];
    docContainer.innerHTML = docs.map(d => `
      <div class="modal-doc-row">
        <input type="checkbox" id="modal-chk-${escapeHtml(d).substring(0, 8)}">
        <label for="modal-chk-${escapeHtml(d).substring(0, 8)}">${escapeHtml(d)}</label>
      </div>
    `).join('') || '<p>Standard government verification documents apply.</p>';
  }

  // Application steps
  const stepsList = $('#modal-apply-steps');
  if (stepsList) {
    const steps = scheme.application_steps || [];
    stepsList.innerHTML = steps.map(step => `<li>${escapeHtml(step)}</li>`).join('') ||
      '<li>Register on the official portal, upload verified documents, and submit before deadline.</li>';
  }

  // Save button in modal
  const modalSaveBtn = $('#modal-save-btn');
  if (modalSaveBtn) {
    const isSaved = savedSchemes.some(x => Number(x.id) === Number(scheme.id));
    modalSaveBtn.textContent = isSaved ? '⭐ Shortlisted' : '☆ Save to Shortlist';
    modalSaveBtn.onclick = () => {
      toggleSaveScheme(scheme.id);
      const nowSaved = savedSchemes.some(x => Number(x.id) === Number(scheme.id));
      modalSaveBtn.textContent = nowSaved ? '⭐ Shortlisted' : '☆ Save to Shortlist';
    };
  }

  // Reset to first tab
  $$('.modal-tab').forEach(t => t.classList.remove('active'));
  $$('.modal-pane').forEach(p => p.classList.remove('active'));
  $(`.modal-tab[data-modaltab="overview"]`)?.classList.add('active');
  $('#pane-overview')?.classList.add('active');

  modal.classList.remove('hidden');
};

function initModalTabs() {
  $$('.modal-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      $$('.modal-tab').forEach(t => t.classList.remove('active'));
      $$('.modal-pane').forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const paneId = tab.getAttribute('data-modaltab');
      const targetPane = $(`#pane-${paneId}`);
      if (targetPane) targetPane.classList.add('active');
    });
  });

  const closeBtn = $('#modal-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      $('#scheme-modal')?.classList.add('hidden');
    });
  }

  // Click outside to close
  const modalBackdrop = $('#scheme-modal');
  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) modalBackdrop.classList.add('hidden');
    });
  }
}

// ==========================================================================
// 6. Scheme Comparison Matrix
// ==========================================================================
window.toggleCompare = function(schemeId, isChecked) {
  const sid = Number(schemeId);
  if (isChecked) {
    if (compareSchemeIds.size >= 4) {
      showToast('Maximum 4 schemes can be compared side-by-side.');
      const cb = document.querySelector(`.result-card[data-scheme-id="${sid}"] .compare-checkbox-label input`);
      if (cb) cb.checked = false;
      return;
    }
    compareSchemeIds.add(sid);
    showToast(`Added to comparison matrix (${compareSchemeIds.size}/4)`);
  } else {
    compareSchemeIds.delete(sid);
    showToast('Removed from comparison');
  }

  updateCompareBadge();
  renderComparisonMatrix();
};

function updateCompareBadge() {
  const badge = $('#nav-compare-count');
  if (badge) badge.textContent = compareSchemeIds.size;
}

function populateCompareDropdown() {
  const select = $('#compare-add-select');
  if (!select) return;
  select.innerHTML = '<option value="">+ Add a scheme to compare...</option>' +
    allSchemes.map(s => `<option value="${s.id}">${escapeHtml(s.name.substring(0, 50))}...</option>`).join('');

  select.addEventListener('change', () => {
    if (select.value) {
      toggleCompare(Number(select.value), true);
      select.value = '';
    }
  });
}

function renderComparisonMatrix() {
  const wrapper = $('#compare-matrix-wrapper');
  if (!wrapper) return;

  if (compareSchemeIds.size < 1) {
    wrapper.innerHTML = `
      <div class="empty-compare-state">
        <span class="empty-icon">⚖️</span>
        <h4>No Schemes Selected for Comparison</h4>
        <p>Select at least 2 schemes by clicking the "+ Compare" button on any scheme card to see an exhaustive side-by-side breakdown.</p>
        <button type="button" class="btn btn-primary btn-sm" id="compare-demo-load">Load Sample Comparison (AICTE Pragati vs PM-USP vs Karnataka SSP)</button>
      </div>`;
    const demoBtn = $('#compare-demo-load');
    if (demoBtn) {
      demoBtn.addEventListener('click', loadDemoComparison);
    }
    return;
  }

  const selectedList = allSchemes.filter(s => compareSchemeIds.has(Number(s.id)));

  wrapper.innerHTML = `
    <table class="compare-table">
      <thead>
        <tr>
          <th>Attribute</th>
          ${selectedList.map(s => `
            <th class="compare-header-cell">
              <strong>${escapeHtml(s.name)}</strong>
              <br>
              <button type="button" class="compare-remove-btn" onclick="toggleCompare(${s.id}, false)">✕ Remove</button>
            </th>
          `).join('')}
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Financial Assistance (₹)</th>
          ${selectedList.map(s => `<td style="font-weight: 800; color: var(--primary-blue); font-size: 14px;">${escapeHtml(s.benefit_amount)}</td>`).join('')}
        </tr>
        <tr>
          <th>Sponsoring Ministry</th>
          ${selectedList.map(s => `<td>${escapeHtml(s.ministry)}</td>`).join('')}
        </tr>
        <tr>
          <th>Income Ceiling</th>
          ${selectedList.map(s => `<td>${s.max_income >= 999999999 ? 'No Income Cap' : 'Up to ' + formatINR(s.max_income)}</td>`).join('')}
        </tr>
        <tr>
          <th>Minimum Marks</th>
          ${selectedList.map(s => `<td>${s.min_marks > 0 ? s.min_marks + '%' : 'Passing marks'}</td>`).join('')}
        </tr>
        <tr>
          <th>Eligible Education Level</th>
          ${selectedList.map(s => `<td>${escapeHtml(s.levels.join(', '))}</td>`).join('')}
        </tr>
        <tr>
          <th>Target Category / Reservation</th>
          ${selectedList.map(s => `<td>${escapeHtml(s.categories.join(', '))}</td>`).join('')}
        </tr>
        <tr>
          <th>Gender Quota</th>
          ${selectedList.map(s => `<td>${escapeHtml(s.gender)}</td>`).join('')}
        </tr>
        <tr>
          <th>Eligible Domicile</th>
          ${selectedList.map(s => `<td>${escapeHtml(s.states.join(', '))}</td>`).join('')}
        </tr>
        <tr>
          <th>Application Window</th>
          ${selectedList.map(s => `<td>${escapeHtml(s.deadline)}</td>`).join('')}
        </tr>
        <tr>
          <th>Official Portal</th>
          ${selectedList.map(s => `<td><a href="${escapeHtml(s.official_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(s.source_name)} ↗</a></td>`).join('')}
        </tr>
      </tbody>
    </table>
  `;
}

function loadDemoComparison() {
  const p1 = allSchemes.find(s => s.code === 'AICTE-PRAGATI');
  const p2 = allSchemes.find(s => s.code === 'MHRD-PMUSP');
  const p3 = allSchemes.find(s => s.code === 'KAR-SSP-POSTMATRIC');

  compareSchemeIds.clear();
  if (p1) compareSchemeIds.add(Number(p1.id));
  if (p2) compareSchemeIds.add(Number(p2.id));
  if (p3) compareSchemeIds.add(Number(p3.id));

  updateCompareBadge();
  renderComparisonMatrix();
  showToast('Loaded 3-scheme demo comparison');
}

// Clear comparison button
const clearCompareBtn = $('#clear-compare-btn');
if (clearCompareBtn) {
  clearCompareBtn.addEventListener('click', () => {
    compareSchemeIds.clear();
    updateCompareBadge();
    renderComparisonMatrix();
    // Uncheck card checkboxes
    $$('.compare-checkbox-label input').forEach(cb => cb.checked = false);
    showToast('Comparison matrix cleared');
  });
}

// ==========================================================================
// 7. Document Readiness Calculator
// ==========================================================================
function initDocumentReadiness() {
  const checks = $$('.doc-check');
  const scoreEl = $('#doc-readiness-percent');
  const guidanceEl = $('#readiness-guidance');

  const updateScore = () => {
    let totalScore = 0;
    let checkedCount = 0;

    checks.forEach(chk => {
      if (chk.checked) {
        totalScore += parseInt(chk.getAttribute('data-weight') || '0', 10);
        checkedCount++;
      }
    });

    if (scoreEl) {
      scoreEl.textContent = `${totalScore}%`;
      if (totalScore >= 80) {
        scoreEl.style.borderColor = 'var(--gov-green)';
        scoreEl.style.color = 'var(--gov-green-dark)';
        scoreEl.style.background = 'var(--gov-green-light)';
      } else if (totalScore >= 50) {
        scoreEl.style.borderColor = 'var(--gov-amber)';
        scoreEl.style.color = 'var(--gov-amber)';
        scoreEl.style.background = 'var(--gov-amber-light)';
      } else {
        scoreEl.style.borderColor = 'var(--gov-red)';
        scoreEl.style.color = 'var(--gov-red)';
        scoreEl.style.background = 'var(--gov-red-light)';
      }
    }

    if (guidanceEl) {
      if (totalScore === 100) {
        guidanceEl.innerHTML = `<strong>Ready to Apply!</strong> Your document kit is 100% complete. Proceed to the National Scholarship Portal (NSP) or Karnataka SSP to register.`;
      } else if (totalScore >= 60) {
        guidanceEl.innerHTML = `<strong>Good Progress (${checkedCount}/6 Documents Ready):</strong> Ensure your Aadhaar is linked to your bank account with active NPCI status to avoid payment delays.`;
      } else {
        guidanceEl.innerHTML = `<strong>Action Required (${checkedCount}/6 Documents Ready):</strong> Apply for your income certificate and check your Aadhaar bank seeding immediately at your bank branch or via DigiLocker.`;
      }
    }
  };

  checks.forEach(chk => chk.addEventListener('change', updateScore));
  updateScore();
}

// ==========================================================================
// 8. Saved Schemes (Shortlist) & Persistence
// ==========================================================================
window.toggleSaveScheme = async function(schemeId) {
  const sid = Number(schemeId);
  const isSaved = savedSchemes.some(x => Number(x.id) === sid);

  try {
    if (isSaved) {
      const res = await fetch(`/api/saved/${sid}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_key: 'student-user' })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to remove scheme.');
      showToast('Scheme removed from shortlist.');
    } else {
      const res = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scheme_id: sid, student_key: 'student-user' })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to save scheme.');
      showToast('Scheme saved to your shortlist! ⭐');
    }

    await loadSaved();
    renderLibrary();
    if (currentResults.length) renderFilteredResults('all');
  } catch (err) {
    showToast(err.message);
  }
};

async function loadSaved() {
  try {
    const res = await fetch('/api/saved?student_key=student-user');
    if (!res.ok) throw new Error('Could not fetch saved schemes.');
    savedSchemes = await res.json();

    const navSavedCount = $('#nav-saved-count');
    const summaryText = $('#saved-summary-text');
    if (navSavedCount) navSavedCount.textContent = savedSchemes.length;
    if (summaryText) summaryText.textContent = `${savedSchemes.length} schemes shortlisted for application`;

    renderSaved();
  } catch (err) {
    console.error(err);
  }
}

function renderSaved() {
  const grid = $('#saved-grid');
  if (!grid) return;

  if (!savedSchemes.length) {
    grid.innerHTML = `
      <div class="empty-shortlist" style="grid-column: 1/-1;">
        <span class="empty-star">⭐</span>
        <h4>Your Shortlist is Empty</h4>
        <p>Save scholarships from the Eligibility Checker or Scheme Library by clicking the "☆ Save" button.</p>
        <a href="#library" class="btn btn-outline btn-sm">Explore Scheme Library</a>
      </div>`;
    return;
  }

  grid.innerHTML = savedSchemes.map(s => `
    <article class="result-card">
      <div class="card-top-bar">
        <span class="card-ministry-tag">${escapeHtml(s.ministry)}</span>
        <button type="button" class="btn btn-outline btn-sm" onclick="toggleSaveScheme(${s.id})" style="color: var(--gov-red); font-size: 11px;">
          ✕ Remove
        </button>
      </div>

      <h4 class="card-title">${escapeHtml(s.name)}</h4>

      <div class="card-benefit-row">
        <span class="benefit-pill">${escapeHtml(s.benefit_amount)}</span>
      </div>

      <p class="card-description">${escapeHtml(s.description)}</p>

      <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 14px;">
        <strong>Deadline:</strong> ${escapeHtml(s.deadline)} · <strong>Portal:</strong> ${escapeHtml(s.source_name)}
      </div>

      <div class="card-bottom-actions">
        <button type="button" class="btn btn-outline btn-sm" onclick="openSchemeModal(${s.id})">
          View Application Roadmap
        </button>
        <a href="${escapeHtml(s.official_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">
          Open Official Portal ↗
        </a>
      </div>
    </article>
  `).join('');
}

// Print / Export Application Summary
function printApplicationSummary(schemesToPrint) {
  const list = (schemesToPrint && schemesToPrint.length)
    ? schemesToPrint.map(item => item.scheme || item)
    : savedSchemes;

  if (!list.length) {
    showToast('No schemes available to print. Run a check or save schemes first.');
    return;
  }

  const printArea = $('#print-area');
  if (!printArea) return;

  const today = new Date().toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });

  printArea.innerHTML = `
    <div class="print-header">
      <h2>ScholarSetu — Official Student Scholarship Application Summary</h2>
      <p>Generated on: ${today} | System: National Student Funding Desk</p>
      <hr style="margin: 12px 0;">
    </div>

    <h3>Shortlisted / Matched Schemes (${list.length} Schemes)</h3>
    ${list.map((s, idx) => `
      <div class="print-scheme-card">
        <h4>${idx + 1}. ${escapeHtml(s.name)}</h4>
        <p><strong>Ministry / Dept:</strong> ${escapeHtml(s.ministry)}</p>
        <p><strong>Annual Benefit:</strong> ${escapeHtml(s.benefit_amount)}</p>
        <p><strong>Application Deadline:</strong> ${escapeHtml(s.deadline)}</p>
        <p><strong>Official Application Portal:</strong> ${escapeHtml(s.official_url)}</p>
        <div style="margin-top: 8px;">
          <strong>Documents Required for Application:</strong>
          <ul>
            ${(s.documents_required || []).map(d => `<li>[  ] ${escapeHtml(d)}</li>`).join('')}
          </ul>
        </div>
      </div>
    `).join('')}

    <div style="margin-top: 24px; font-size: 11px; border-top: 1px solid #000; padding-top: 12px;">
      <p><strong>Important Note for Student:</strong> Bring this printed summary along with original marksheets, caste & income certificates, and bank passbook to your college scholarship nodal officer for institutional e-verification.</p>
    </div>
  `;

  window.print();
}

const exportShortlistBtn = $('#export-shortlist-btn');
if (exportShortlistBtn) {
  exportShortlistBtn.addEventListener('click', () => {
    printApplicationSummary(savedSchemes);
  });
}

// ==========================================================================
// 9. Quick Search Modal (Ctrl+K)
// ==========================================================================
function initGlobalSearch() {
  const searchModal = $('#search-modal');
  const searchInput = $('#global-search-input');
  const searchResults = $('#global-search-results');
  const searchTrigger = $('#global-search-trigger');
  const closeBtn = $('#search-modal-close');

  const openSearch = () => {
    if (!searchModal) return;
    searchModal.classList.remove('hidden');
    if (searchInput) {
      searchInput.value = '';
      searchInput.focus();
    }
  };

  const closeSearch = () => {
    if (searchModal) searchModal.classList.add('hidden');
  };

  if (searchTrigger) searchTrigger.addEventListener('click', openSearch);
  if (closeBtn) closeBtn.addEventListener('click', closeSearch);

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape') {
      closeSearch();
      $('#scheme-modal')?.classList.add('hidden');
    }
  });

  if (searchModal) {
    searchModal.addEventListener('click', (e) => {
      if (e.target === searchModal) closeSearch();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase().trim();
      if (!q) {
        searchResults.innerHTML = '<div class="search-hint">Type keywords like "AICTE", "Karnataka", "Pragati", "SC", "Engineering"...</div>';
        return;
      }

      const matches = allSchemes.filter(s =>
        (s.name + ' ' + s.description + ' ' + s.category + ' ' + s.ministry + ' ' + s.code).toLowerCase().includes(q)
      );

      if (!matches.length) {
        searchResults.innerHTML = '<div class="search-hint">No schemes found matching your search.</div>';
        return;
      }

      searchResults.innerHTML = matches.slice(0, 8).map(s => `
        <div class="search-result-item" onclick="openSchemeModal(${s.id}); $('#search-modal').classList.add('hidden');">
          <span class="search-result-title">${escapeHtml(s.name)}</span>
          <span class="search-result-meta">${escapeHtml(s.ministry)} · ${escapeHtml(s.benefit_amount)}</span>
        </div>
      `).join('');
    });
  }
}

// ==========================================================================
// 10. Platform Overview Stats
// ==========================================================================
async function updateStats() {
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) return;
    const stats = await res.json();
    if ($('#stat-schemes')) $('#stat-schemes').textContent = stats.total_schemes || 16;
    if ($('#stat-ministries')) $('#stat-ministries').textContent = stats.total_ministries || 8;
    if ($('#stat-max-aid')) $('#stat-max-aid').textContent = formatINR(stats.max_annual_benefit || 250000);
  } catch (e) {
    console.error(e);
  }
}

// ==========================================================================
// 12. AI Scholarship Assistant Chatbot (Saarthi)
// ==========================================================================
function initAIChatbot() {
  const launcher = $('#ai-chat-launcher');
  const windowEl = $('#ai-chat-window');
  const closeBtn = $('#ai-chat-close');
  const form = $('#ai-chat-form');
  const input = $('#ai-chat-input');
  const messages = $('#ai-chat-messages');
  const chipsContainer = $('#ai-chat-chips');

  if (!launcher || !windowEl) return;

  function toggleChat() {
    windowEl.classList.toggle('hidden');
    if (!windowEl.classList.contains('hidden') && input) {
      input.focus();
    }
  }

  launcher.addEventListener('click', toggleChat);
  if (closeBtn) closeBtn.addEventListener('click', toggleChat);

  if (chipsContainer) {
    chipsContainer.addEventListener('click', (e) => {
      const chip = e.target.closest('.ai-chip');
      if (chip && chip.dataset.query) {
        if (input) input.value = chip.dataset.query;
        sendMessage(chip.dataset.query);
      }
    });
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = input ? input.value.trim() : '';
      if (!text) return;
      sendMessage(text);
    });
  }

  async function sendMessage(text) {
    if (input) input.value = '';

    const userMsg = document.createElement('div');
    userMsg.className = 'ai-message user-bubble';
    userMsg.textContent = text;
    messages.appendChild(userMsg);
    messages.scrollTop = messages.scrollHeight;

    const typing = document.createElement('div');
    typing.className = 'ai-message ai-bubble typing-indicator';
    typing.id = 'ai-typing-indicator';
    typing.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      const typingEl = $('#ai-typing-indicator');
      if (typingEl) typingEl.remove();

      if (!res.ok) throw new Error('API error');
      const data = await res.json();

      const botMsg = document.createElement('div');
      botMsg.className = 'ai-message ai-bubble';

      let parsed = (data.reply || '')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/#### (.*?)\n/g, '<h5 style="margin:8px 0 4px; color:#003366;">$1</h5>')
        .replace(/### (.*?)\n/g, '<h4 style="margin:10px 0 6px; color:#003366;">$1</h4>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
        .replace(/\n/g, '<br>');

      botMsg.innerHTML = `<div class="ai-msg-header">🤖 Saarthi</div><div>${parsed}</div>`;
      messages.appendChild(botMsg);
      messages.scrollTop = messages.scrollHeight;

      if (data.suggested_chips && data.suggested_chips.length && chipsContainer) {
        chipsContainer.innerHTML = data.suggested_chips.map(c => 
          `<button class="ai-chip" data-query="${escapeHtml(c)}">${escapeHtml(c)}</button>`
        ).join('');
      }
    } catch (err) {
      const typingEl = $('#ai-typing-indicator');
      if (typingEl) typingEl.remove();

      const errorMsg = document.createElement('div');
      errorMsg.className = 'ai-message ai-bubble';
      errorMsg.innerHTML = `<div class="ai-msg-header">⚠️ Error</div><div>Could not retrieve scholarship details. Please check your network or try again.</div>`;
      messages.appendChild(errorMsg);
      messages.scrollTop = messages.scrollHeight;
    }
  }
}

// ==========================================================================
// 13. Citizen & Nodal Officer Authentication Subsystem
// ==========================================================================
function initAuthModal() {
  const trigger = $('#auth-modal-trigger');
  const modal = $('#auth-modal');
  const closeBtn = $('#auth-modal-close');
  const form = $('#auth-login-form');
  const emailInput = $('#auth-email');
  const passwordInput = $('#auth-password');
  const emailLabel = $('#auth-email-label');
  const togglePass = $('#toggle-auth-password');
  const alertBox = $('#auth-alert');
  const tabStudent = $('#tab-student');
  const tabOfficer = $('#tab-officer');
  const demoStudent = $('#demo-student-fill');
  const demoOfficer = $('#demo-officer-fill');
  const authBtnText = $('#auth-btn-text');

  let currentRole = 'student';

  if (!trigger || !modal) return;

  function openModal() {
    modal.classList.remove('hidden');
    if (alertBox) alertBox.classList.add('hidden');
    if (emailInput) emailInput.focus();
  }

  function closeModal() {
    modal.classList.add('hidden');
  }

  trigger.addEventListener('click', () => {
    const token = localStorage.getItem('scholarsetu_auth_token');
    if (token) {
      if (confirm('Do you want to sign out of your account?')) {
        localStorage.removeItem('scholarsetu_auth_token');
        localStorage.removeItem('scholarsetu_user');
        updateAuthHeader();
      }
      return;
    }
    openModal();
  });

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  if (tabStudent) {
    tabStudent.addEventListener('click', () => {
      currentRole = 'student';
      tabStudent.classList.add('active');
      if (tabOfficer) tabOfficer.classList.remove('active');
      if (emailLabel) emailLabel.textContent = 'Student Email / OTR (One-Time Registration ID)';
      if (emailInput) emailInput.placeholder = 'e.g. student@scholarsetu.gov.in';
    });
  }

  if (tabOfficer) {
    tabOfficer.addEventListener('click', () => {
      currentRole = 'officer';
      tabOfficer.classList.add('active');
      if (tabStudent) tabStudent.classList.remove('active');
      if (emailLabel) emailLabel.textContent = 'College / Nodal Verification Officer Email';
      if (emailInput) emailInput.placeholder = 'e.g. nodal@rnsit.ac.in';
    });
  }

  if (togglePass && passwordInput) {
    togglePass.addEventListener('click', () => {
      const isPass = passwordInput.type === 'password';
      passwordInput.type = isPass ? 'text' : 'password';
      togglePass.textContent = isPass ? 'Hide' : 'Show';
    });
  }

  if (demoStudent) {
    demoStudent.addEventListener('click', () => {
      if (tabStudent) tabStudent.click();
      if (emailInput) emailInput.value = 'student@scholarsetu.gov.in';
      if (passwordInput) passwordInput.value = 'Scholar@2026';
    });
  }

  if (demoOfficer) {
    demoOfficer.addEventListener('click', () => {
      if (tabOfficer) tabOfficer.click();
      if (emailInput) emailInput.value = 'nodal@rnsit.ac.in';
      if (passwordInput) passwordInput.value = 'Officer@2026';
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = emailInput ? emailInput.value.trim() : '';
      const password = passwordInput ? passwordInput.value.trim() : '';

      if (!email || !password) return;

      if (alertBox) {
        alertBox.className = 'auth-alert';
        alertBox.textContent = 'Verifying credentials against National ScholarSetu Vault...';
        alertBox.classList.remove('hidden');
      }

      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || 'Authentication failed');
        }

        localStorage.setItem('scholarsetu_auth_token', data.token);
        localStorage.setItem('scholarsetu_user', JSON.stringify(data.user));

        if (alertBox) {
          alertBox.className = 'auth-alert success';
          alertBox.textContent = `Welcome, ${data.user.full_name}! Authenticated successfully.`;
        }

        setTimeout(() => {
          closeModal();
          updateAuthHeader();
        }, 800);
      } catch (err) {
        if (alertBox) {
          alertBox.className = 'auth-alert error';
          alertBox.textContent = err.message;
        }
      }
    });
  }

  function updateAuthHeader() {
    const rawUser = localStorage.getItem('scholarsetu_user');
    if (rawUser && authBtnText) {
      try {
        const user = JSON.parse(rawUser);
        authBtnText.textContent = user.role === 'nodal_officer' ? 'Officer Portal' : user.full_name.split(' ')[0];
        trigger.title = `Logged in as ${user.full_name}. Click to Sign Out.`;
        trigger.classList.add('btn-success');
      } catch (e) {
        authBtnText.textContent = 'Sign In';
      }
    } else if (authBtnText) {
      authBtnText.textContent = 'Sign In';
      trigger.title = 'Sign In to Student or Officer Desk';
      trigger.classList.remove('btn-success');
    }
  }

  updateAuthHeader();
}

// ==========================================================================
// 11. App Initialization
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  initAccessibility();
  initWizard();
  initLibraryFilters();
  initModalTabs();
  initDocumentReadiness();
  initGlobalSearch();
  initAIChatbot();
  initAuthModal();
  loadLibrary();
});
