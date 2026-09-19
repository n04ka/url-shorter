const baseUrl = "http://localhost:8000";

async function getAllLinks() {
  try {
    const response = await fetch(`${baseUrl}/links`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) throw new Error('Failed to get links');
    const data = await response.json();
    console.log('All links:', data);
    return data;

  } catch (error) {
    console.error('Error fetching links:', error);
    return null;
  }
}

async function createLink(long) {
  const data = { "link": long };
  try {
    const params = new URLSearchParams(data);
    const response = await fetch(`${baseUrl}/link?${params.toString()}`, {
      method: 'POST'
    });

    if (!response.ok) throw new Error('Failed to create link!!!!!');
    const code = await response.text();
    console.log('Link created:', code);
    return code;

  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

async function deleteLink(short) {
  const data = { "code": short };
  try {
    const params = new URLSearchParams(data);
    const response = await fetch(`${baseUrl}/link?${params.toString()}`, {
      method: 'DELETE'
    });

    if (!response.ok) throw new Error('Failed to delete link!!!!!');
    console.log('Link deleted:', short);
    return true;

  } catch (error) {
    console.error('Error:', error);
    return false;
  }
}

// Отрисовка таблицы — принимает массив Link
function renderAllLinks(links) {
  const tbody = document.querySelector('#linksTable tbody');
  tbody.innerHTML = '';

  if (!Array.isArray(links) || links.length === 0) {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td colspan="3" style="text-align: center; padding: 20px;">
        No links found. Create your first link!
      </td>
    `;
    tbody.appendChild(row);
    return;
  }

  for (const link of links) {
    addRowToTable(link);
  }
}

// Добавление строки — принимает объект Link
function addRowToTable(link) {
  const tbody = document.querySelector('#linksTable tbody');

  const noLinksMsg = tbody.querySelector('td[colspan="3"]');
  if (noLinksMsg) tbody.innerHTML = '';

  const newRow = document.createElement('tr');
  newRow.innerHTML = `
    <td class="center">
      <span class="block code">${link.code}</span>
    </td>
    <td>
      <span class="block"><a href="${link.url}" target="_blank">${link.url}</a></span>
    </td>
    <td class="center">
      <button class="action delete" data-code="${link.code}">Delete</button>
    </td>
  `;
  tbody.appendChild(newRow);
}

function removeRowFromTable(code) {
  const rows = document.querySelectorAll('#linksTable tbody tr');
  for (const row of rows) {
    const deleteBtn = row.querySelector('.delete');
    if (deleteBtn && String(deleteBtn.dataset.code) === String(code)) {
      row.remove();
      return true;
    }
  }
  return false;
}

async function refreshLinks() {
  const links = await getAllLinks();
  if (links) {
    renderAllLinks(links);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('createLinkForm');
  const urlInput = document.getElementById('urlInput');

  refreshLinks();

  form.addEventListener('submit', async function(event) {
    event.preventDefault();

    const longUrl = urlInput.value.trim();
    if (!longUrl) {
      alert('Please enter a valid URL');
      return;
    }

    let finalUrl = longUrl;
    if (!finalUrl.startsWith('http://') && !finalUrl.startsWith('https://')) {
      finalUrl = 'https://' + finalUrl;
    }

    const code = await createLink(finalUrl);
    if (code) {
      await refreshLinks();   // ✅ вместо addRowToTable(code, finalUrl)
      urlInput.value = '';
    }
  });
});

const table = document.getElementById('linksTable');
table.addEventListener('click', async function(event) {
  const classlist = event.target.classList;

  if (classlist.contains('delete')) {
    const code = event.target.dataset.code;
    if (!code) {
      console.error('No code found for delete button');
      return;
    }

    if (confirm(`Are you sure you want to delete link with code: ${code}?`)) {
      const success = await deleteLink(code);
      if (success) {
        removeRowFromTable(code);
      }
    }
  }
});