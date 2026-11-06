/**
 * CAREER LIST & SEARCH CONTROLLER
 */

document.addEventListener("DOMContentLoaded", async () => {
  const careers = await ApiClient.getCareers();
  renderCareerList(careers);
  initFilters(careers);
});

function renderCareerList(careers) {
  const container = document.getElementById("careerListContainer");
  if (!container) return;

  if (careers.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem;">
        <i class="fas fa-search" style="font-size: 3rem; color: var(--text-light); margin-bottom: 1rem;"></i>
        <h3 style="font-size: 1.25rem;">Không tìm thấy ngành nghề phù hợp</h3>
        <p style="color: var(--text-muted);">Hãy thử tìm kiếm với từ khóa khác hoặc điều chỉnh lại bộ lọc.</p>
      </div>
    `;
    return;
  }

  let html = "";
  careers.forEach(career => {
    const blocksHtml = career.required_blocks
      .map(b => `<span class="block-tag" style="font-size: 0.75rem;">${b}</span>`)
      .join("");

    html += `
      <div class="career-card-item">
        <div>
          <div class="career-header">
            <div class="career-icon-avatar">
              <i class="fas ${career.icon}"></i>
            </div>
            <div>
              <span class="badge badge-primary">${career.category}</span>
              <h4 style="margin-top: 0.5rem; font-size: 1.15rem; font-weight: 700;">${career.name}</h4>
              <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">Mã ngành: ${career.code} | RIASEC: ${career.riasec_code}</span>
            </div>
          </div>
          <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1.25rem;">
            ${career.description}
          </p>
          <div style="margin-bottom: 1rem;">
            <small style="font-weight: 700; color: var(--text-main); display: block; margin-bottom: 0.4rem;">
              <i class="fas fa-book" style="color: var(--primary-600); margin-right: 4px;"></i> Khối xét tuyển:
            </small>
            <div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">
              ${blocksHtml}
            </div>
          </div>
        </div>

        <div style="border-top: 1px solid var(--border-color); padding-top: 1rem; margin-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
          <div class="salary-tag">
            <i class="fas fa-coins"></i>
            <span>${career.average_salary}</span>
          </div>
          <a href="career-detail.html?id=${career.id}" class="btn btn-secondary btn-sm">
            Chi tiết <i class="fas fa-arrow-right"></i>
          </a>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function initFilters(allCareers) {
  const searchInput = document.getElementById("careerSearchInput");
  const catSelect = document.getElementById("categoryFilterSelect");
  const blockSelect = document.getElementById("blockFilterSelect");

  function applyFilter() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
    const selectedCat = catSelect ? catSelect.value : "ALL";
    const selectedBlock = blockSelect ? blockSelect.value : "ALL";

    const filtered = allCareers.filter(c => {
      // Tìm kiếm text
      const matchesText = !query || 
        c.name.toLowerCase().includes(query) || 
        c.code.toLowerCase().includes(query) || 
        c.description.toLowerCase().includes(query);

      // Lĩnh vực
      const matchesCat = selectedCat === "ALL" || c.category === selectedCat;

      // Khối thi
      const matchesBlock = selectedBlock === "ALL" || c.required_blocks.some(b => b.includes(selectedBlock));

      return matchesText && matchesCat && matchesBlock;
    });

    renderCareerList(filtered);
  }

  if (searchInput) searchInput.addEventListener("input", applyFilter);
  if (catSelect) catSelect.addEventListener("change", applyFilter);
  if (blockSelect) blockSelect.addEventListener("change", applyFilter);
}
