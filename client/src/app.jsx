import React from "react";
import { render } from "react-dom";
import Plot from "react-plotly.js";

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

  if (isLoading) {
    return <p>Henter data</p>;
  } else if (data.length == 0) {
    return <p>Har ikke fått data</p>;
  }

  return (
    <div>
      {JSON.stringify(data)}
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
  );
};

render(<App />, document.getElementById("app"));
