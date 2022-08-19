import React from "react";
import { render } from "react-dom";
import Plot from "react-plotly.js";
import "@miljodirektoratet/md-css";
import { MdCheckbox } from "@miljodirektoratet/md-react";

const App = () => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [data, setData] = React.useState([]);

  React.useEffect(() => {
    async function fetchData() {
      const response = await fetch("http://localhost:5000/utslipp/jordbruk");
      const data = await response.json();
      setData(data);
      setIsLoading(false);
    }
    fetchData();
  }, []);

  const [komponenter, setKomponenter] = React.useState([]);
  React.useEffect(() => {
    async function fetchData() {
      const response = await fetch(
        "http://localhost:5000/utslipp/jordbruk/komponenter"
      );
      const data = await response.json();
      setKomponenter(
        data.komponenter.map((komponent) => ({
          komponentNavn: komponent,
          checked: false,
        }))
      );
    }
    fetchData();
  }, [isLoading]);

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
