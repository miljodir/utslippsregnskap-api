import React from 'react';
import { render } from 'react-dom';
import { getInitialData } from './api';
import ComponentFilter from './components/ComponentFilter';
import LevelFilter from './components/LevelFilter';
import JordbrukPlot from './components/JordbrukPlot';
import '@miljodirektoratet/md-css';

function reducer(state, action) {
  switch (action.type) {
    case 'data_fetch_failed':
      return {
        ...state,
        hasError: true,
        loading: false,
      };
    case 'update_base_data':
      return {
        ...state,
        loading: false,
        komponenter: action.komponenter,
        nivåer: action.nivåer,
        komponentFilter: action.komponenter.map((komponent) => {
          return {
            komponentNavn: komponent,
            checked: false,
          };
        }),
        nivåFilter: action.nivåer.map((nivå) => {
          return {
            nivå: nivå,
            checked: false,
          };
        }),
      };
    case 'update_komponent_filter':
      const komponentIndex = action.indexToToggle;
      const nextKomponentFilter = [...state.komponentFilter];
      nextKomponentFilter[komponentIndex].checked =
        !nextKomponentFilter[komponentIndex].checked;
      return {
        ...state,
        komponentFilter: nextKomponentFilter,
      };
    case 'update_nivå_filter':
      const nivåIndex = action.indexToToggle;
      const nextNivåFilter = [...state.nivåFilter];
      nextNivåFilter[nivåIndex].checked = !nextNivåFilter[nivåIndex].checked;
      return {
        ...state,
        nivåFilter: nextNivåFilter,
      };
  }
}

const App = () => {
  const [state, dispatch] = React.useReducer(reducer, { loading: true });

  React.useEffect(() => {
    async function setupInitialState() {
      try {
        const results = await getInitialData();
        const [komponentHttpResult, nivåHttpResult] = results as any;
        dispatch({
          type: 'update_base_data',
          komponenter: komponentHttpResult.value.komponenter,
          nivåer: nivåHttpResult.value.nivaa3,
        });
      } catch (error) {
        dispatch({
          type: 'data_fetch_failed',
          error,
        });
      }
    }
    setupInitialState();
  }, []);

  const updateKomponentFilter = (index) => {
    dispatch({
      type: 'update_komponent_filter',
      indexToToggle: index,
    });
  };

  const updateNivåFilter = (index) => {
    dispatch({
      type: 'update_nivå_filter',
      indexToToggle: index,
    });
  };

  if (state.hasError) {
    return <h1>Noe gikk galt ved henting av data</h1>;
  }
  if (state.loading) {
    return <h1>Henter data om komponenter og nivåer...</h1>;
  }

  const { komponentFilter, nivåFilter } = state;
  const komponentFilterNames = komponentFilter
    .filter(({ checked }) => checked)
    .map(({ komponentNavn }) => komponentNavn);
  const nivåFilterNames = nivåFilter
    .filter(({ checked }) => checked)
    .map(({ nivå }) => nivå);

  return (
    <div>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <ComponentFilter
          components={komponentFilter}
          onComponentsUpdated={updateKomponentFilter}
        />
      </div>
      <div style={{ display: 'flex', gap: '2rem', marginTop: '1rem' }}>
        <LevelFilter levels={nivåFilter} onLevelsUpdated={updateNivåFilter} />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <JordbrukPlot
          komponenter={komponentFilterNames}
          nivåer={nivåFilterNames}
        />
      </div>
    </div>
  );
};

render(<App />, document.getElementById('app'));
