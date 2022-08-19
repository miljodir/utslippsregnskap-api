import React from "react";
import { render } from "react-dom";
import Plot from "react-plotly.js";
import "@miljodirektoratet/md-css";
import { MdCheckbox } from "@miljodirektoratet/md-react";

const App = () => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [data, setData] = React.useState([]);

  async function fetchJordbrukUtslipp(komponenter) {
    const komponentFilter = komponenter.join(",");
    const response = await fetch(`http://localhost:5000/utslipp/jordbruk?komponenter=${komponentFilter}`);
    const data = await response.json();
    setData(data);
    setIsLoading(false);
  }
  async function fetchKomponenter() {
    const response = await fetch(
        "http://localhost:5000/utslipp/jordbruk/komponenter"
      );
      return await response.json();
  }

  React.useEffect(() => {
    async function initData() {
      const komponentJson =  await fetchKomponenter()
      const komponentListe = komponentJson.komponenter;
      setKomponenter(
        komponentListe.map((komponent) => ({
          komponentNavn: komponent,
          checked: false,
        }))
      );
      await fetchJordbrukUtslipp(komponentListe)
    }
    initData()
  }, [])

  const [komponenter, setKomponenter] = React.useState([]);

  React.useEffect(() => {
    const filter = komponenter.filter((komponent) => { return komponent.checked; })
    let selectedKomponenter = filter.map((f) => f.komponentNavn);
    fetchJordbrukUtslipp(selectedKomponenter);
  }, [komponenter]);

  if (isLoading) {
    return <p>Henter data</p>;
  } else if (data.length === 0) {
    return <p>Har ikke fått data</p>;
  }

  const updateKomponentFilter = (index) => {
    const nextKomponentFilter = [...komponenter];
    nextKomponentFilter[index].checked = !nextKomponentFilter[index].checked;
    setKomponenter(nextKomponentFilter);
  };

  return (
    <div>
      <div style={{ display: "flex", gap: "2rem" }}>
        {komponenter.map((komponent, index) => (
          <MdCheckbox
            label={komponent.komponentNavn}
            checked={komponent.checked}
            onChange={() => updateKomponentFilter(index)}
          />
        ))}
      </div>
      <div style={{ marginTop: "1rem" }}>
        <Plot
          data={[
            {
              x: [...data.aar],
              y: [...data.utslipp],
              type: "scatter",
              mode: "lines",
            },
          ]}
        ></Plot>
      </div>
    </div>
  );
};

render(<App />, document.getElementById("app"));
