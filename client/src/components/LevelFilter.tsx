import React from 'react';
import { MdCheckbox } from '@miljodirektoratet/md-react';
import { NivåFilter } from '../types';

export interface NivåFilterProps {
  nivåer: NivåFilter[];
  onNivåFilterUpdated: (index: number) => void;
}

const NivåFilter: React.FunctionComponent<NivåFilterProps> = ({
  nivåer,
  onNivåFilterUpdated,
}: NivåFilterProps) => {
  const renderLevelCheckbox = (nivå, index) => (
    <MdCheckbox
      label={nivå.nivå}
      checked={nivå.checked}
      onChange={() => onNivåFilterUpdated(index)}
      key={nivå.nivå}
    />
  );

  return <>{nivåer.map(renderLevelCheckbox)}</>;
};

export default NivåFilter;
