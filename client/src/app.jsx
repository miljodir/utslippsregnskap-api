import React from "react";
import { render } from "react-dom";
import Plot from "react-plotly.js";
import "@miljodirektoratet/md-css";
import { MdButton, MdCheckbox, MdChecklist } from "@miljodirektoratet/md-react";

const App = () => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [data, setData] = React.useState([]);
  const [allChecked, setAllChecked] = React.useState(false);
  const [nivaaer, setNivaaer] = React.useState([]);

  React.useEffect(() => {
    async function fetchData() {
      const response = await fetch("http://localhost:5000/utslipp/jordbruk");
      const data = await response.json();
      setData(data);
      setIsLoading(false);
    }
    fetchData();
  }, []);

  React.useEffect(() => {
    async function fetchData() {
      const response = await fetch("http://localhost:5000/utslipp/nivaa");
      const data = await response.json();
      setNivaaer(data);
    }
    fetchData();
  }, [isLoading]);

  if (isLoading) {
    return <p>Henter data</p>;
  } else if (data.length === 0) {
    return <p>Har ikke fått data</p>;
  }

  const renderCheckboxes = (nivå) => {
    if (!nivå.nivaa) {
      return (
        <MdCheckbox
          label={nivå.kategori}
          checked={allChecked}
          onChange={() => setAllChecked(!allChecked)}
        />
      );
    } else {
      return (
        <MdChecklist
          label={nivå.kategori}
          checked={allChecked}
          onChange={() => setAllChecked(!allChecked)}
        >
          {nivå.nivaa.map(renderCheckboxes)}
        </MdChecklist>
      );
    }
  };

  return (
    <div>
      <MdButton>Sylteagurk</MdButton>
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
      {JSON.stringify(nivaaer)}
      {nivaaer.map(renderCheckboxes)}
    </div>
  );
};

render(<App />, document.getElementById("app"));
