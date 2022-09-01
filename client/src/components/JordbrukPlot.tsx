import React from 'react';
import { getJordbrukData } from '../api';
import Plot from 'react-plotly.js';

const reducer = (state, action) => {
  switch (action.type) {
    case 'ok':
      return {
        ...state,
        utslippsdata: action.utslippsdata,
        hasError: false,
        isLoading: false,
      };
    case 'request_failed':
      return {
        ...state,
        hasError: true,
        isLoading: false,
      };
    case 'pending':
      return {
        ...state,
        hasError: false,
        isLoading: true,
      };
  }
};

const JordbrukPlot = ({ komponenter, nivåer }) => {
  const [state, dispatch] = React.useReducer(reducer, { isLoading: true });

  React.useEffect(() => {
    async function getPlotData() {
      try {
        const data = await getJordbrukData(komponenter, nivåer);
        dispatch({ type: 'ok', utslippsdata: data });
      } catch (error) {
        console.error(error);
        dispatch({
          type: 'request_failed',
        });
      }
    }
    getPlotData();
  }, [komponenter, nivåer]);

  if (state.isLoading) {
    return <p>Henter utslippsdata...</p>;
  }
  if (state.hasError) {
    return <p>Noe gikk galt ved henting av data</p>;
  }

  const { utslippsdata } = state;
  console.log(Plot);
  return (
    <Plot
      data={[
        {
          x: [...utslippsdata.aar],
          y: [...utslippsdata.utslipp],
          type: 'scatter',
          mode: 'lines',
        },
      ]}
    />
  );
};

export default JordbrukPlot;
