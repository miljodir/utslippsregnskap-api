import React from 'react';

const LevelFilter = ({ levels, onLevelsUpdated }) => {
  const renderLevelCheckbox = (level, index) => (
    <MdCheckbox
      label={level.nivaa}
      checked={level.checked}
      onChange={() => onLevelsUpdated(index)}
      key={level.nivaa}
    />
  );

  return <>{levels.map(renderLevelCheckbox)}</>;
};

export default LevelFilter;