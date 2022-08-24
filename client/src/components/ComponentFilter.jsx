import React from 'react';

const ComponentFilter = ({ components, onComponentsUpdated }) => {
  const renderComponentCheckbox = (component, index) => (
    <MdCheckbox
      label={component.komponentNavn}
      checked={component.checked}
      onChange={() => onComponentsUpdated(index)}
      key={component.komponentNavn}
    />
  );

  return <>{components.map(renderComponentCheckbox)}</>;
};

export default ComponentFilter;
