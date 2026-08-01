const baseUrl = "http://localhost:8000"

async function createLink(long) {
  const data = {"URL": long}
  try {
    const response = await fetch(`${baseUrl}/link`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error('Failed to create link!!!!!');
    const code = await response.text();
    console.log('Link created:', code);

  } catch (error) {
      console.error('Error:', error);
  }
}


async function deleteLink(short) {
  const data = {"code": short}
  try {
    const response = await fetch(`${baseUrl}/delete/link`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error('Failed to delete link!!!!!');
    console.log('Link deleted:', short);

  } catch (error) {
      console.error('Error:', error);
  }
}

const table = document.getElementById('linksTable'); 
table.addEventListener('click', function(event) {
  const classlist = event.target.classList
  if (classlist.contains('create')) {
    alert("open new link form")
  } else if (classlist.contains('delete')) {
    alert("delete link")
  }
});