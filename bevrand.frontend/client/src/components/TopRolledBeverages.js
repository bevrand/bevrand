

const getRedisHistory = async (playlist) => {
  let body;
  try {
    const response = await fetch(`/api/redis?user=${playlist.user.toLowerCase()}&list=${playlist.name}`, {
        method: 'POST',
        body: JSON.stringify(playlist),
        headers: new Headers({
          'Content-Type': 'application/json'
        })
      });
    body = await response.json();
  } catch (err) {
    console.error('Error: ', err);
  }
  return body;
}