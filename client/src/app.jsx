import React from "react";
import { render } from "react-dom";

const App = () => {
  const [isLoading, setIsLoading] = React.useState(true);
  const [data, setData] = React.useState([]);

  React.useEffect(() => {
    async function fetchData() {
      const data = await fetch("http://localhost:5000/utslipp/jordbruk");
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

  return <div>{JSON.stringify(data)}</div>;
};

render(<App />, document.getElementById("app"));
