import React from 'react';
import { MdCheckbox } from '@miljodirektoratet/md-react';
import { KomponentFilter } from '../types';

export interface KomponentFilterProps {
  komponenter: KomponentFilter[];
  onKomponentFilterUpdated: (index: number) => void;
}

const KomponentFilter: React.FunctionComponent<KomponentFilterProps> = ({
  komponenter,
  onKomponentFilterUpdated,
}: KomponentFilterProps) => {
  const renderKomponentCheckbox = (komponent, index) => (
    <MdCheckbox
      label={komponent.komponentNavn}
      checked={komponent.checked}
      onChange={() => onKomponentFilterUpdated(index)}
      key={komponent.komponentNavn}
    />
  );

  return <>{komponenter.map(renderKomponentCheckbox)}</>;
};

export default KomponentFilter;
