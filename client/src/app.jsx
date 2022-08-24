import React from 'react';
import { render } from 'react-dom';
import Plot from 'react-plotly.js';
import '@miljodirektoratet/md-css';
import ComponentFilter from './components/ComponentFilter';
import LevelFilter from './components/LevelFilter';

const App = () => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [jordbrukUtslipp, setJordbrukUtslipp] = React.useState([]);
  const [komponenter, setKomponenter] = React.useState([]);
  const [nivaa3, setNivaa3] = React.useState([]);

  async function fetchJordbrukUtslipp(komponenter, nivaa) {
    const komponentFilter = komponenter.join(',');
    const nivaaFilter = nivaa.join(',');
    const response = await fetch(
      `/utslipp/jordbruk?komponenter=${komponentFilter}&nivaa=${nivaaFilter}`
    );
    const data = await response.json();
    setJordbrukUtslipp(data);

    setIsLoading(false);
  }
  async function fetchKomponenter() {
    const response = await fetch('/utslipp/jordbruk/komponenter');
    return await response.json();
  }
  async function fetchNivaa3() {
    const response = await fetch('/utslipp/jordbruk/nivaa3');
    return await response.json();
  }

  React.useEffect(() => {
    async function initData() {
      const komponentJson = await fetchKomponenter();
      const komponentListe = komponentJson.komponenter;
      setKomponenter(
        komponentListe.map((komponent) => ({
          komponentNavn: komponent,
          checked: false,
        }))
      );
      const nivaaJson = await fetchNivaa3();
      const nivaaListe = nivaaJson.nivaa3;
      setNivaa3(
        nivaaListe.map((nivaa) => ({
          nivaa: nivaa,
          checked: false,
        }))
      );
      await fetchJordbrukUtslipp(komponentListe, nivaaListe);
    }
    initData();
  }, []);

  React.useEffect(() => {
    const filter = komponenter.filter((komponent) => komponent.checked);
    const selectedKomponenter = filter.map((f) => f.komponentNavn);
    const selectedNivaa = nivaa3.filter((nivaa) => nivaa.checked).map((nivaa) => nivaa.nivaa);
    fetchJordbrukUtslipp(selectedKomponenter, selectedNivaa);
  }, [komponenter, nivaa3]);

  if (isLoading) {
    return <p>Henter data</p>;
  } else if (jordbrukUtslipp.length === 0) {
    return <p>Har ikke fått data</p>;
  }

  const updateKomponentFilter = (index) => {
    const nextKomponentFilter = [...komponenter];
    nextKomponentFilter[index].checked = !nextKomponentFilter[index].checked;
    setKomponenter(nextKomponentFilter);
  };

  const updateNivaaFilter = (index) => {
    const nextNivaaFilter = [...nivaa3];
    nextNivaaFilter[index].checked = !nextNivaaFilter[index].checked;
    setNivaa3(nextNivaaFilter);
  };

  return (
    <div>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <ComponentFilter components={komponenter} onComponentsUpdated={updateKomponentFilter} />
      </div>
      <div style={{ display: 'flex', gap: '2rem', marginTop: '1rem' }}>
        <LevelFilter levels={levels} onLevelsUpdated={updateNivaaFilter} />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <Plot
          data={[
            {
              x: [...jordbrukUtslipp.aar],
              y: [...jordbrukUtslipp.utslipp],
              type: 'scatter',
              mode: 'lines',
            },
          ]}
        ></Plot>
      </div>
    </div>
  );
};

render(<App />, document.getElementById('app'));
