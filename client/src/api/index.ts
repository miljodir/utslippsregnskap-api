export async function fetchKomponenter() {
  const response = await fetch('/utslipp/jordbruk/komponenter');
  const { status } = response;
  if (status == 401 || status == 403) {
    const redirectLocation = response.headers.get('Location');
    if (redirectLocation) {
      window.location.assign(redirectLocation);
    }
  }
  return await response.json();
}

export async function fetchNivaa3() {
  const response = await fetch('/utslipp/jordbruk/nivaa3');
  const { status } = response;
  if (status == 401 || status == 403) {
    const redirectLocation = response.headers.get('Location');
    if (redirectLocation) {
      window.location.assign(redirectLocation);
    }
  }
  return await response.json();
}

export async function getInitialData() {
  return new Promise(async (resolve, reject) => {
    const results = await Promise.allSettled([
      fetchKomponenter(),
      fetchNivaa3(),
    ]);
    const someRequestFailed = results.some(
      ({ status }) => status === 'rejected'
    );
    if (someRequestFailed) {
      reject('A request has failed to fetch initial data');
    } else {
      resolve(results);
    }
  });
}

export async function getJordbrukData(komponenter, nivåer) {
  const komponentFilter = komponenter.join(',');
  const nivåFilter = nivåer.join(',');
  const response = await fetch(
    `/utslipp/jordbruk?komponenter=${komponentFilter}&nivaa=${nivåFilter}`
  );
  const data = await response.json();
  return data;
}
